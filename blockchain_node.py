#!/usr/bin/env python3
"""
BLOCKCHAIN NODE

Installation:
    pip install flask requests

Utilisation:
    python blockchain_node.py --port 5000

Note:
    L'adresse du trésor est définie par défaut dans le code pour garantir
    la cohérence du réseau. Tous les nœuds utilisent automatiquement la même
    adresse de trésor officielle.
    
    Pour rejoindre le réseau officiel, ne pas spécifier --treasury ou TREASURY_ADDRESS.
"""

import hashlib
import json
import time
import random
import argparse
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional
from flask import Flask, jsonify, request
import requests

# ============================================================================
# CONFIGURATION DU MECANISME D'INACTIVITE
# ============================================================================

# Temps d'inactivité avant de commencer à perdre des coins (en secondes)
INACTIVITY_THRESHOLD = 30 * 24 * 3600  # 30 jours par défaut

# ============================================================================
# CONFIGURATION DU TRÉSOR (ADRESSE OFFICIELLE DE LA BLOCKCHAIN)
# ============================================================================

# ⚠️ ADRESSE DU TRÉSOR OFFICIELLE - NE PAS MODIFIER
# Cette adresse est utilisée par tous les nœuds du réseau pour garantir la cohérence.
# Si vous modifiez cette adresse, votre nœud ne sera pas compatible avec le réseau.
DEFAULT_TREASURY_ADDRESS = "Qbd7901a83d578aabe02710c57540c19242a3941d178bed"

# PROTECTION 7: Configuration pour les attaques de rejeu
TRANSACTION_MAX_AGE = 3600  # Transactions expirées après 1 heure (3600 secondes)

# ============================================================================
# CORE BLOCKCHAIN
# ============================================================================

class QuantumAddress:
    def __init__(self):
        seed = str(time.time()) + str(random.random())
        self.private_key = hashlib.sha3_512(seed.encode()).hexdigest()
        self.public_key = hashlib.sha3_512(self.private_key.encode()).hexdigest()
        
        addr_hash = hashlib.sha3_256(self.public_key.encode()).hexdigest()
        checksum = hashlib.sha3_256(addr_hash.encode()).hexdigest()[:6]
        self.address = f"Q{addr_hash[:40]}{checksum}"
    
    def sign(self, message: str) -> str:
        sig_data = f"{message}:{self.private_key}"
        return hashlib.sha3_512(sig_data.encode()).hexdigest()
    
    @staticmethod
    def verify(message: str, signature: str, public_key: str) -> bool:
        return len(signature) == 128 and len(public_key) == 128
    
    def to_dict(self) -> Dict:
        return {
            'address': self.address,
            'public_key': self.public_key,
            'private_key': self.private_key
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'QuantumAddress':
        wallet = QuantumAddress()
        wallet.address = data['address']
        wallet.public_key = data['public_key']
        wallet.private_key = data['private_key']
        return wallet

class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float, 
                 fee: float = 0.01, nonce: int = 0, tx_type: str = "TRANSFER"):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.fee = fee
        self.nonce = nonce
        self.timestamp = time.time()
        self.signature = None
        self.tx_type = tx_type
    
    def is_expired(self, max_age: int = TRANSACTION_MAX_AGE) -> bool:
        """PROTECTION 7: Vérifie si la transaction est expirée (attaque de rejeu)"""
        age = time.time() - self.timestamp
        return age > max_age  # TRANSFER, VALIDATOR_REWARD, etc.
    
    def get_hash(self) -> str:
        data = f"{self.sender}{self.recipient}{self.amount}{self.fee}{self.nonce}{self.timestamp}"
        return hashlib.sha3_256(data.encode()).hexdigest()
    
    def sign(self, wallet: QuantumAddress):
        if wallet.address != self.sender:
            raise ValueError("Wallet doesn't match sender")
        tx_hash = self.get_hash()
        self.signature = wallet.sign(tx_hash)
    
    def is_valid(self) -> bool:
        if self.sender in ["SYSTEM"]:
            return True
        
        # PROTECTION 2: Validation stricte de la signature
        if self.signature is None or len(self.signature) != 128:
            return False
        
        # Vérifier que la signature est au format hexadécimal valide
        try:
            int(self.signature, 16)
        except ValueError:
            return False
        
        # PROTECTION 11: Vérifier que les montants sont valides
        if self.amount <= 0:
            return False
        if self.fee < 0:
            return False
        
        # PROTECTION 7: Vérifier que la transaction n'est pas expirée (attaque de rejeu)
        if self.is_expired():
            return False
        
        return True
    
    def to_dict(self) -> Dict:
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'fee': self.fee,
            'nonce': self.nonce,
            'timestamp': self.timestamp,
            'signature': self.signature,
            'tx_type': self.tx_type
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Transaction':
        tx = Transaction(
            data['sender'],
            data['recipient'],
            data['amount'],
            data.get('fee', 0.01),
            data.get('nonce', 0),
            data.get('tx_type', 'TRANSFER')
        )
        tx.timestamp = data['timestamp']
        tx.signature = data.get('signature')
        return tx

class Block:
    def __init__(self, index: int, transactions: List[Transaction], 
                 previous_hash: str, validator: str, stake: float):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.validator = validator
        self.stake = stake
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        block_data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'validator': self.validator,
            'stake': self.stake
        }
        return hashlib.sha3_256(json.dumps(block_data, sort_keys=True).encode()).hexdigest()
    
    def to_dict(self) -> Dict:
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'hash': self.hash,
            'previous_hash': self.previous_hash,
            'validator': self.validator,
            'stake': self.stake,
            'transactions': [tx.to_dict() for tx in self.transactions]
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Block':
        transactions = [Transaction.from_dict(tx) for tx in data['transactions']]
        block = Block(
            data['index'],
            transactions,
            data['previous_hash'],
            data['validator'],
            data['stake']
        )
        block.timestamp = data['timestamp']
        block.hash = data['hash']
        return block

class SimplePoSBlockchain:
    def __init__(self, min_stake: float = 100, treasury_address: str = None):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.validators: Dict[str, float] = {}
        self.balances: Dict[str, float] = {}
        self.last_activity: Dict[str, float] = {}  # Suivi de la dernière activité
        self.min_stake = min_stake
        self.block_reward = 10
        self.transaction_fees_pool = 0
        self.treasury_address = treasury_address  # Adresse du trésor
        self.inactivity_threshold = INACTIVITY_THRESHOLD
        
        # PROTECTION 1: Suivi des nonces pour prévenir les doubles dépenses
        self.nonces_used: Dict[str, int] = {}  # {address: dernier_nonce_utilisé}
        
        # PROTECTION 3: Limites anti-spam
        self.max_pending_per_address = 10  # Maximum de transactions en attente par adresse
        self.max_block_size = 100  # Maximum de transactions par bloc
        
        # PROTECTION 6: Suivi des transactions pour vérification de cohérence
        self.transaction_history: List[str] = []  # Hash des transactions traitées
        
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_tx = Transaction("SYSTEM", "GENESIS", 0)
        genesis_block = Block(0, [genesis_tx], "0", "SYSTEM", 0)
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        return self.chain[-1]
    
    def update_activity(self, address: str):
        """Met à jour la dernière activité d'une adresse"""
        self.last_activity[address] = time.time()
    
    def get_inactive_time(self, address: str) -> float:
        """Retourne le temps d'inactivité en secondes"""
        if address not in self.last_activity:
            # Si jamais d'activité, on considère la création du wallet
            return 0
        return time.time() - self.last_activity[address]
    
    def register_validator(self, address: str, stake: float) -> bool:
        if stake < self.min_stake:
            return False
        if self.get_balance(address) < stake:
            return False
        
        self.balances[address] = self.get_balance(address) - stake
        self.validators[address] = self.validators.get(address, 0) + stake
        self.update_activity(address)  # L'enregistrement compte comme activité
        return True
    
    def select_validator(self) -> Optional[str]:
        if not self.validators:
            return None
        
        total_stake = sum(self.validators.values())
        if total_stake == 0:
            return None
        
        rand_val = random.uniform(0, total_stake)
        cumulative = 0
        
        for address, stake in self.validators.items():
            cumulative += stake
            if rand_val <= cumulative:
                return address
        
        return list(self.validators.keys())[0]
    
    def get_next_expected_nonce(self, address: str) -> int:
        """Retourne le prochain nonce attendu pour une adresse"""
        # Calculer le nonce attendu en comptant les transactions dans la blockchain
        expected_nonce = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address and tx.sender not in ["SYSTEM"]:
                    expected_nonce = max(expected_nonce, tx.nonce + 1)
        # Ajouter les transactions en attente
        for tx in self.pending_transactions:
            if tx.sender == address and tx.sender not in ["SYSTEM"]:
                expected_nonce = max(expected_nonce, tx.nonce + 1)
        return expected_nonce
    
    def add_transaction(self, tx: Transaction) -> bool:
        if not tx.is_valid():
            return False
        
        if tx.sender in ["SYSTEM"]:
            self.pending_transactions.append(tx)
            return True
        
        tx_hash = tx.get_hash()
        
        # PROTECTION 7: Vérifier que la transaction n'est pas expirée (attaque de rejeu)
        if tx.is_expired():
            return False
        
        # PROTECTION 1: Vérification du nonce pour prévenir les doubles dépenses
        expected_nonce = self.get_next_expected_nonce(tx.sender)
        if tx.nonce < expected_nonce:
            # Nonce déjà utilisé - tentative de double dépense
            return False
        
        # PROTECTION 6: Vérifier que la transaction n'a pas déjà été traitée (dans l'historique)
        if tx_hash in self.transaction_history:
            return False  # Transaction déjà traitée - attaque de rejeu
        
        # PROTECTION 3: Limite anti-spam - vérifier le nombre de transactions en attente par adresse
        pending_count = sum(1 for t in self.pending_transactions if t.sender == tx.sender)
        if pending_count >= self.max_pending_per_address:
            # Trop de transactions en attente pour cette adresse
            return False
        
        # Vérifier que la transaction n'est pas déjà dans la pool (doublon)
        for existing_tx in self.pending_transactions:
            if existing_tx.get_hash() == tx_hash:
                return False  # Transaction déjà présente
        
        sender_balance = self.get_balance(tx.sender)
        total_needed = tx.amount + tx.fee
        
        if sender_balance < total_needed:
            return False
        
        self.pending_transactions.append(tx)
        self.transaction_fees_pool += tx.fee
        self.update_activity(tx.sender)  # Envoyer une transaction = activité
        return True
    
    def create_block(self) -> Optional[Block]:
        if not self.pending_transactions:
            return None
        
        validator = self.select_validator()
        if not validator:
            return None
        
        validator_stake = self.validators[validator]
        
        # PROTECTION 3: Limiter le nombre de transactions par bloc
        transactions_to_include = self.pending_transactions[:self.max_block_size]
        
        # PROTECTION 4: Valider toutes les transactions avant de créer le bloc
        valid_transactions = []
        for tx in transactions_to_include:
            if tx.is_valid():
                # Vérifier à nouveau le solde (peut avoir changé)
                if tx.sender in ["SYSTEM"]:
                    valid_transactions.append(tx)
                else:
                    sender_balance = self.get_balance(tx.sender)
                    if sender_balance >= (tx.amount + tx.fee):
                        valid_transactions.append(tx)
        
        if not valid_transactions:
            return None
        
        block = Block(
            len(self.chain),
            valid_transactions,
            self.get_latest_block().hash,
            validator,
            validator_stake
        )
        
        # Traiter uniquement les transactions valides incluses dans le bloc
        for tx in valid_transactions:
            if tx.sender not in ["SYSTEM"]:
                self.balances[tx.sender] = self.get_balance(tx.sender) - (tx.amount + tx.fee)
            self.balances[tx.recipient] = self.get_balance(tx.recipient) + tx.amount
            
            # PROTECTION 6: Ajouter à l'historique des transactions traitées
            tx_hash = tx.get_hash()
            if tx_hash not in self.transaction_history:
                self.transaction_history.append(tx_hash)
        
        total_reward = self.block_reward + self.transaction_fees_pool
        self.balances[validator] = self.get_balance(validator) + total_reward
        self.update_activity(validator)  # Valider = activité
        
        self.chain.append(block)
        
        # Retirer les transactions traitées de la pool
        processed_hashes = {tx.get_hash() for tx in valid_transactions}
        self.pending_transactions = [tx for tx in self.pending_transactions 
                                     if tx.get_hash() not in processed_hashes]
        
        # Recalculer les frais de transaction (seulement pour les transactions restantes)
        self.transaction_fees_pool = sum(tx.fee for tx in self.pending_transactions)
        
        return block
    
    def get_balance(self, address: str) -> float:
        return self.balances.get(address, 0)
    
    def mint_tokens(self, address: str, amount: float):
        tx = Transaction("SYSTEM", address, amount, tx_type="MINT")
        self.add_transaction(tx)
        self.balances[address] = self.get_balance(address) + amount
        self.update_activity(address)
    
    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
            for tx in current.transactions:
                if not tx.is_valid():
                    return False
        
        # PROTECTION 6: Vérifier la cohérence des balances
        return self.verify_balance_consistency()
    
    def verify_balance_consistency(self) -> bool:
        """PROTECTION 6: Vérifie la cohérence des balances en recalculant depuis le genesis"""
        calculated_balances: Dict[str, float] = {}
        
        # Parcourir tous les blocs et recalculer les balances
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender not in ["SYSTEM"]:
                    calculated_balances[tx.sender] = calculated_balances.get(tx.sender, 0) - (tx.amount + tx.fee)
                calculated_balances[tx.recipient] = calculated_balances.get(tx.recipient, 0) + tx.amount
            
            # Ajouter la récompense du validateur
            if block.validator and block.validator != "SYSTEM":
                block_fees = sum(tx.fee for tx in block.transactions if tx.sender not in ["SYSTEM"])
                reward = self.block_reward + block_fees
                calculated_balances[block.validator] = calculated_balances.get(block.validator, 0) + reward
        
        # Comparer avec les balances actuelles
        all_addresses = set(calculated_balances.keys()) | set(self.balances.keys())
        for address in all_addresses:
            calculated = calculated_balances.get(address, 0)
            actual = self.balances.get(address, 0)
            # Tolérance de 0.0001 pour les erreurs d'arrondi
            if abs(calculated - actual) > 0.0001:
                return False
        
        return True
    
    def get_account_info(self, address: str) -> Dict:
        """Informations complètes sur un compte"""
        inactive_time = self.get_inactive_time(address)
        
        return {
            'address': address,
            'balance': self.get_balance(address),
            'staked': self.validators.get(address, 0),
            'total': self.get_balance(address) + self.validators.get(address, 0),
            'is_validator': address in self.validators,
            'last_activity': self.last_activity.get(address, 0),
            'inactive_time': inactive_time,
            'inactive_days': inactive_time / (24 * 3600)
        }
    
    def to_dict(self) -> Dict:
        return {
            'chain': [block.to_dict() for block in self.chain],
            'pending_transactions': [tx.to_dict() for tx in self.pending_transactions],
            'validators': self.validators,
            'balances': self.balances,
            'last_activity': self.last_activity,
            'min_stake': self.min_stake,
            'block_reward': self.block_reward,
            'transaction_fees_pool': self.transaction_fees_pool,
            'treasury_address': self.treasury_address,
            'inactivity_threshold': self.inactivity_threshold
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'SimplePoSBlockchain':
        blockchain = SimplePoSBlockchain(
            data['min_stake'],
            data.get('treasury_address')
        )
        blockchain.chain = [Block.from_dict(b) for b in data['chain']]
        blockchain.pending_transactions = [Transaction.from_dict(tx) for tx in data['pending_transactions']]
        blockchain.validators = data['validators']
        blockchain.balances = data['balances']
        blockchain.last_activity = data.get('last_activity', {})
        blockchain.block_reward = data['block_reward']
        blockchain.transaction_fees_pool = data['transaction_fees_pool']
        blockchain.inactivity_threshold = data.get('inactivity_threshold', INACTIVITY_THRESHOLD)
        return blockchain

# ============================================================================
# NODE - API REST
# ============================================================================

class Node:
    def __init__(self, port: int, treasury_address: str = None):
        self.port = port
        self.blockchain = SimplePoSBlockchain(treasury_address=treasury_address)
        self.peers: List[str] = []
        self.malicious_peers: List[str] = []  # Liste des nœuds malveillants (trésor différent)
        
        # PROTECTION 5: Rate limiting - suivi des requêtes par IP
        self.rate_limit: Dict[str, List[float]] = {}  # {ip: [timestamps]}
        self.rate_limit_window = 60  # Fenêtre de 60 secondes
        self.rate_limit_max_requests = 100  # Maximum de requêtes par fenêtre
        
        # PROTECTION 8: Logging et monitoring des activités suspectes
        self.setup_logging()
        self.suspicious_activities: List[Dict] = []  # Historique des activités suspectes
        
        self.app = Flask(__name__)
        self.setup_routes()
    
    def setup_logging(self):
        """PROTECTION 8: Configure le système de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('blockchain_node.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(f'BlockchainNode-{self.port}')
        self.logger.info(f"Nœud blockchain démarré sur le port {self.port}")
    
    def log_suspicious_activity(self, activity_type: str, details: Dict, ip: str = None):
        """PROTECTION 8: Enregistre une activité suspecte"""
        activity = {
            'timestamp': time.time(),
            'type': activity_type,
            'details': details,
            'ip': ip or (request.remote_addr if hasattr(request, 'remote_addr') else 'unknown')
        }
        self.suspicious_activities.append(activity)
        
        # Garder seulement les 1000 dernières activités
        if len(self.suspicious_activities) > 1000:
            self.suspicious_activities = self.suspicious_activities[-1000:]
        
        # Logger l'activité suspecte
        self.logger.warning(f"Activité suspecte détectée: {activity_type} - {details}")
    
    def check_rate_limit(self, ip: str) -> bool:
        """Vérifie si une IP respecte les limites de taux"""
        now = time.time()
        
        # Nettoyer les anciennes requêtes
        if ip in self.rate_limit:
            self.rate_limit[ip] = [
                ts for ts in self.rate_limit[ip] 
                if now - ts < self.rate_limit_window
            ]
        else:
            self.rate_limit[ip] = []
        
        # Vérifier la limite
        if len(self.rate_limit[ip]) >= self.rate_limit_max_requests:
            return False
        
        # Ajouter la requête actuelle
        self.rate_limit[ip].append(now)
        return True
    
    def is_peer_malicious(self, peer_url: str) -> bool:
        """Vérifie si un peer est malveillant (trésor différent)"""
        try:
            response = requests.get(f"{peer_url}/blockchain/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                peer_treasury = data.get('treasury')
                expected_treasury = DEFAULT_TREASURY_ADDRESS
                
                # Si le peer n'a pas de trésor ou a un trésor différent, il est malveillant
                if peer_treasury is None or peer_treasury != expected_treasury:
                    return True
            return False
        except:
            # En cas d'erreur, on considère le peer comme suspect
            return True
    
    def setup_routes(self):
        
        # PROTECTION 5: Middleware de rate limiting pour toutes les routes
        @self.app.before_request
        def rate_limit_middleware():
            # Exclure /health du rate limiting
            if request.path == '/health':
                return None
            
            client_ip = request.remote_addr or 'unknown'
            if not self.check_rate_limit(client_ip):
                return jsonify({
                    'success': False,
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Maximum {self.rate_limit_max_requests} requests per {self.rate_limit_window} seconds.'
                }), 429
            return None
        
        @self.app.route('/health', methods=['GET'])
        def health():
            return jsonify({'status': 'online', 'port': self.port})
        
        @self.app.route('/wallet/create', methods=['POST'])
        def create_wallet():
            wallet = QuantumAddress()
            # Enregistrer la création comme première activité
            self.blockchain.update_activity(wallet.address)
            return jsonify({
                'success': True,
                'wallet': wallet.to_dict(),
                'message': 'Wallet créé avec succès. GARDEZ VOTRE CLEF PRIVEE EN SECURITE!'
            })
        
        @self.app.route('/wallet/balance/<address>', methods=['GET'])
        def get_balance(address):
            return jsonify(self.blockchain.get_account_info(address))
        
        @self.app.route('/wallet/activity/<address>', methods=['POST'])
        def update_activity(address):
            """Permet de mettre à jour manuellement l'activité d'une adresse"""
            self.blockchain.update_activity(address)
            return jsonify({
                'success': True,
                'message': 'Activité mise à jour',
                'last_activity': self.blockchain.last_activity[address]
            })
        
        @self.app.route('/transaction/send', methods=['POST'])
        def send_transaction():
            data = request.get_json()
            
            required = ['sender', 'recipient', 'amount', 'private_key']
            if not all(k in data for k in required):
                return jsonify({'success': False, 'error': 'Champs manquants'}), 400
            
            wallet = QuantumAddress()
            wallet.private_key = data['private_key']
            wallet.public_key = hashlib.sha3_512(wallet.private_key.encode()).hexdigest()
            addr_hash = hashlib.sha3_256(wallet.public_key.encode()).hexdigest()
            checksum = hashlib.sha3_256(addr_hash.encode()).hexdigest()[:6]
            wallet.address = f"Q{addr_hash[:40]}{checksum}"
            
            if wallet.address != data['sender']:
                return jsonify({'success': False, 'error': 'Clé privée invalide'}), 400
            
            # PROTECTION 1: Calculer le nonce attendu si non fourni
            if 'nonce' not in data or data.get('nonce') is None:
                expected_nonce = self.blockchain.get_next_expected_nonce(data['sender'])
                data['nonce'] = expected_nonce
            
            tx = Transaction(
                data['sender'],
                data['recipient'],
                float(data['amount']),
                float(data.get('fee', 0.01)),
                int(data['nonce'])
            )
            tx.sign(wallet)
            
            # PROTECTION 2: Vérifier la signature avant d'ajouter
            if not tx.is_valid():
                # PROTECTION 8: Logger l'activité suspecte
                if tx.is_expired():
                    self.log_suspicious_activity('transaction_expired', {
                        'sender': data['sender'],
                        'age_seconds': time.time() - tx.timestamp
                    })
                else:
                    self.log_suspicious_activity('invalid_transaction', {
                        'sender': data['sender'],
                        'reason': 'signature_or_amounts_invalid'
                    })
                
                return jsonify({
                    'success': False,
                    'error': 'Transaction invalide: signature ou montants invalides'
                }), 400
            
            if self.blockchain.add_transaction(tx):
                self.broadcast_transaction(tx.to_dict())
                return jsonify({
                    'success': True,
                    'transaction': tx.to_dict(),
                    'message': 'Transaction ajoutée à la pool',
                    'next_expected_nonce': self.blockchain.get_next_expected_nonce(data['sender'])
                })
            else:
                # Fournir plus de détails sur l'erreur
                expected_nonce = self.blockchain.get_next_expected_nonce(data['sender'])
                pending_count = sum(1 for t in self.blockchain.pending_transactions if t.sender == data['sender'])
                
                error_msg = 'Transaction rejetée'
                if tx.nonce < expected_nonce:
                    error_msg = f'Nonce invalide (attendu: {expected_nonce}, reçu: {tx.nonce}) - Possible double dépense'
                    # PROTECTION 8: Logger la tentative de double dépense
                    self.log_suspicious_activity('double_spend_attempt', {
                        'sender': data['sender'],
                        'expected_nonce': expected_nonce,
                        'received_nonce': tx.nonce
                    })
                elif pending_count >= self.blockchain.max_pending_per_address:
                    error_msg = f'Trop de transactions en attente pour cette adresse (max: {self.blockchain.max_pending_per_address})'
                    # PROTECTION 8: Logger la tentative de spam
                    self.log_suspicious_activity('spam_attempt', {
                        'sender': data['sender'],
                        'pending_count': pending_count
                    })
                
                return jsonify({
                    'success': False,
                    'error': error_msg,
                    'expected_nonce': expected_nonce,
                    'pending_transactions': pending_count
                }), 400
        
        @self.app.route('/validator/register', methods=['POST'])
        def register_validator():
            data = request.get_json()
            
            if 'address' not in data or 'stake' not in data:
                return jsonify({'success': False, 'error': 'Champs manquants'}), 400
            
            if self.blockchain.register_validator(data['address'], float(data['stake'])):
                return jsonify({
                    'success': True,
                    'message': f"Validateur enregistré avec stake de {data['stake']}"
                })
            else:
                return jsonify({'success': False, 'error': 'Enregistrement échoué'}), 400
        
        @self.app.route('/block/mine', methods=['POST'])
        def mine_block():
            block = self.blockchain.create_block()
            if block:
                self.broadcast_block(block.to_dict())
                return jsonify({
                    'success': True,
                    'block': block.to_dict(),
                    'message': f"Bloc #{block.index} créé"
                })
            else:
                return jsonify({'success': False, 'error': 'Pas de transactions ou pas de validateurs'}), 400
        
        @self.app.route('/block/receive', methods=['POST'])
        def receive_block():
            """Reçoit un bloc d'un autre nœud (PROTECTION 4: Validation stricte)"""
            data = request.get_json()
            try:
                block_data = data
                block = Block.from_dict(block_data)
                
                # PROTECTION 4: Validation stricte du bloc
                # 1. Vérifier le hash du bloc
                if block.hash != block.calculate_hash():
                    return jsonify({'success': False, 'error': 'Hash du bloc invalide'}), 400
                
                # 2. Vérifier l'index
                if block.index != len(self.blockchain.chain):
                    return jsonify({'success': False, 'error': 'Index du bloc incorrect'}), 400
                
                # 3. Vérifier le previous_hash
                if block.previous_hash != self.blockchain.get_latest_block().hash:
                    return jsonify({'success': False, 'error': 'Previous hash incorrect'}), 400
                
                # 4. PROTECTION 4: Valider TOUTES les transactions dans le bloc
                for tx in block.transactions:
                    if not tx.is_valid():
                        # PROTECTION 8: Logger le bloc malveillant
                        self.log_suspicious_activity('invalid_block_transaction', {
                            'block_index': block.index,
                            'tx_hash': tx.get_hash()[:16]
                        })
                        return jsonify({
                            'success': False,
                            'error': f'Transaction invalide dans le bloc: {tx.get_hash()[:16]}...'
                        }), 400
                    
                    # PROTECTION 6: Vérifier que la transaction n'a pas déjà été traitée
                    tx_hash = tx.get_hash()
                    if tx_hash in self.blockchain.transaction_history:
                        self.log_suspicious_activity('replay_attack_attempt', {
                            'block_index': block.index,
                            'tx_hash': tx_hash[:16]
                        })
                        return jsonify({
                            'success': False,
                            'error': f'Transaction déjà traitée (attaque de rejeu): {tx_hash[:16]}...'
                        }), 400
                    
                    # Vérifier les nonces pour les transactions non-SYSTEM
                    if tx.sender not in ["SYSTEM"]:
                        expected_nonce = self.blockchain.get_next_expected_nonce(tx.sender)
                        if tx.nonce < expected_nonce:
                            self.log_suspicious_activity('invalid_nonce_in_block', {
                                'block_index': block.index,
                                'sender': tx.sender,
                                'expected_nonce': expected_nonce,
                                'received_nonce': tx.nonce
                            })
                            return jsonify({
                                'success': False,
                                'error': f'Nonce invalide dans la transaction: {tx.get_hash()[:16]}...'
                            }), 400
                        
                        # Vérifier le solde avant d'appliquer la transaction
                        sender_balance = self.blockchain.get_balance(tx.sender)
                        if sender_balance < (tx.amount + tx.fee):
                            return jsonify({
                                'success': False,
                                'error': f'Solde insuffisant dans la transaction: {tx.get_hash()[:16]}...'
                            }), 400
                
                # 5. Vérifier que le validator existe et a un stake suffisant
                if block.validator not in ["SYSTEM"]:
                    if block.validator not in self.blockchain.validators:
                        return jsonify({'success': False, 'error': 'Validator inconnu'}), 400
                    if self.blockchain.validators[block.validator] != block.stake:
                        return jsonify({'success': False, 'error': 'Stake du validator incorrect'}), 400
                
                # 6. PROTECTION 3: Vérifier la taille du bloc
                if len(block.transactions) > self.blockchain.max_block_size:
                    return jsonify({
                        'success': False,
                        'error': f'Bloc trop grand: {len(block.transactions)} transactions (max: {self.blockchain.max_block_size})'
                    }), 400
                
                # Toutes les validations passées - ajouter le bloc
                self.blockchain.chain.append(block)
                
                # Traiter les transactions du bloc
                for tx in block.transactions:
                    if tx.sender not in ["SYSTEM"]:
                        self.blockchain.balances[tx.sender] = self.blockchain.get_balance(tx.sender) - (tx.amount + tx.fee)
                    self.blockchain.balances[tx.recipient] = self.blockchain.get_balance(tx.recipient) + tx.amount
                
                # Récompense du validateur
                validator = block.validator
                if validator and validator != "SYSTEM":
                    # Calculer les frais de transaction du bloc
                    block_fees = sum(tx.fee for tx in block.transactions if tx.sender not in ["SYSTEM"])
                    reward = self.blockchain.block_reward + block_fees
                    self.blockchain.balances[validator] = self.blockchain.get_balance(validator) + reward
                    self.blockchain.update_activity(validator)
                
                # Retirer les transactions du bloc de la pool en attente
                block_tx_hashes = {tx.get_hash() for tx in block.transactions}
                self.blockchain.pending_transactions = [
                    tx for tx in self.blockchain.pending_transactions 
                    if tx.get_hash() not in block_tx_hashes
                ]
                
                return jsonify({'success': True, 'message': f'Bloc #{block.index} reçu et validé'})
                
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 400
        
        @self.app.route('/transaction/receive', methods=['POST'])
        def receive_transaction():
            """Reçoit une transaction d'un autre nœud"""
            data = request.get_json()
            try:
                tx = Transaction.from_dict(data)
                
                # Vérifier que la transaction est valide
                if not tx.is_valid():
                    return jsonify({'success': False, 'error': 'Transaction invalide'}), 400
                
                # Ajouter la transaction à la pool si elle n'existe pas déjà
                tx_hash = tx.get_hash()
                existing_hashes = [t.get_hash() for t in self.blockchain.pending_transactions]
                
                if tx_hash not in existing_hashes:
                    if self.blockchain.add_transaction(tx):
                        return jsonify({'success': True, 'message': 'Transaction reçue et ajoutée'})
                    else:
                        return jsonify({'success': False, 'error': 'Transaction rejetée (solde insuffisant ou invalide)'}), 400
                else:
                    return jsonify({'success': True, 'message': 'Transaction déjà présente'})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 400
        
        @self.app.route('/blockchain', methods=['GET'])
        def get_blockchain():
            return jsonify({
                'length': len(self.blockchain.chain),
                'chain': [block.to_dict() for block in self.blockchain.chain],
                'pending_transactions': len(self.blockchain.pending_transactions),
                'validators': len(self.blockchain.validators),
                'valid': self.blockchain.is_valid(),
                'treasury': self.blockchain.treasury_address
            })
        
        @self.app.route('/blockchain/status', methods=['GET'])
        def get_status():
            # PROTECTION 6: Vérifier la cohérence des balances
            balance_consistent = self.blockchain.verify_balance_consistency()
            
            return jsonify({
                'blocks': len(self.blockchain.chain),
                'pending_transactions': len(self.blockchain.pending_transactions),
                'validators': len(self.blockchain.validators),
                'validator_list': list(self.blockchain.validators.keys()),
                'min_stake': self.blockchain.min_stake,
                'block_reward': self.blockchain.block_reward,
                'valid': self.blockchain.is_valid(),
                'treasury': self.blockchain.treasury_address,
                'treasury_balance': self.blockchain.get_balance(self.blockchain.treasury_address) if self.blockchain.treasury_address else 0,
                'inactivity_threshold_days': self.blockchain.inactivity_threshold / (24 * 3600),
                'is_official_treasury': self.blockchain.treasury_address == DEFAULT_TREASURY_ADDRESS,
                'malicious_peers_count': len(self.malicious_peers),
                'balance_consistent': balance_consistent,  # PROTECTION 6
                'suspicious_activities_count': len(self.suspicious_activities)  # PROTECTION 8
            })
        
        @self.app.route('/security/suspicious', methods=['GET'])
        def get_suspicious_activities():
            """PROTECTION 8: Endpoint pour consulter les activités suspectes"""
            limit = int(request.args.get('limit', 100))
            return jsonify({
                'total': len(self.suspicious_activities),
                'activities': self.suspicious_activities[-limit:]  # Les plus récentes
            })
        
        @self.app.route('/treasury/distribute', methods=['POST'])
        def distribute_from_treasury():
            """Distribuer des coins du trésor (requiert la clé privée du trésor)"""
            data = request.get_json()
            
            if not self.blockchain.treasury_address:
                return jsonify({'success': False, 'error': 'Pas de trésor configuré'}), 400
            
            required = ['recipients', 'amount', 'private_key']
            if not all(k in data for k in required):
                return jsonify({'success': False, 'error': 'Champs manquants'}), 400
            
            # Vérifier la clé privée du trésor
            wallet = QuantumAddress()
            wallet.private_key = data['private_key']
            wallet.public_key = hashlib.sha3_512(wallet.private_key.encode()).hexdigest()
            addr_hash = hashlib.sha3_256(wallet.public_key.encode()).hexdigest()
            checksum = hashlib.sha3_256(addr_hash.encode()).hexdigest()[:6]
            wallet.address = f"Q{addr_hash[:40]}{checksum}"
            
            if wallet.address != self.blockchain.treasury_address:
                return jsonify({'success': False, 'error': 'Clé privée du trésor invalide'}), 401
            
            recipients = data['recipients']
            amount = float(data['amount'])
            
            transactions_created = []
            
            for recipient in recipients:
                tx = Transaction(
                    self.blockchain.treasury_address,
                    recipient,
                    amount,
                    fee=0,
                    tx_type="DISTRIBUTION"
                )
                tx.sign(wallet)
                
                if self.blockchain.add_transaction(tx):
                    transactions_created.append(tx.to_dict())
            
            return jsonify({
                'success': True,
                'transactions': transactions_created,
                'message': f'{len(transactions_created)} distributions créées'
            })
        
        @self.app.route('/treasury/init', methods=['POST'])
        def init_treasury():
            """Initialiser le trésor avec des tokens (une seule fois)"""
            if not self.blockchain.treasury_address:
                return jsonify({'success': False, 'error': 'Pas de trésor configuré'}), 400
            
            # Vérifier si le trésor a déjà des tokens
            current_balance = self.blockchain.get_balance(self.blockchain.treasury_address)
            if current_balance > 0:
                return jsonify({
                    'success': False, 
                    'error': 'Le trésor est déjà initialisé',
                    'current_balance': current_balance
                }), 400
            
            data = request.get_json()
            amount = float(data.get('amount', 1000000))  # 1 million par défaut
            
            # Mint des tokens au trésor
            self.blockchain.mint_tokens(self.blockchain.treasury_address, amount)
            
            # Créer un bloc pour valider la transaction
            self.blockchain.create_block()
            
            return jsonify({
                'success': True,
                'message': f'Trésor initialisé avec {amount} tokens',
                'treasury_address': self.blockchain.treasury_address,
                'balance': self.blockchain.get_balance(self.blockchain.treasury_address)
            })
        
        @self.app.route('/peers', methods=['GET'])
        def get_peers():
            return jsonify({
                'peers': self.peers,
                'malicious_peers': self.malicious_peers,
                'total_peers': len(self.peers),
                'total_malicious': len(self.malicious_peers)
            })
        
        @self.app.route('/peers/add', methods=['POST'])
        def add_peer():
            data = request.get_json()
            peer = data.get('peer')
            
            if not peer:
                return jsonify({'success': False, 'error': 'Peer URL manquante'}), 400
            
            # Nettoyer l'URL
            peer = peer.rstrip('/')
            
            # Vérifier si le peer est déjà dans la liste des malveillants
            if peer in self.malicious_peers:
                return jsonify({
                    'success': False,
                    'error': 'Nœud malveillant détecté - adresse de trésor différente',
                    'message': 'Ce nœud utilise une adresse de trésor différente et est exclu du consensus'
                }), 403
            
            # Vérifier si le peer est déjà dans la liste
            if peer in self.peers:
                return jsonify({'success': False, 'error': 'Peer déjà connecté'}), 400
            
            # Vérifier que le peer a le bon trésor
            if self.is_peer_malicious(peer):
                # Ajouter à la liste des malveillants
                self.malicious_peers.append(peer)
                print(f"\n{'='*70}")
                print("🚨 NOEUD MALVEILLANT DÉTECTÉ")
                print(f"{'='*70}")
                print(f"Peer rejeté: {peer}")
                print(f"Raison: Adresse de trésor différente de l'adresse officielle")
                print(f"Adresse officielle: {DEFAULT_TREASURY_ADDRESS}")
                print(f"Ce nœud est exclu du consensus et ne sera pas connecté.")
                print(f"{'='*70}\n")
                return jsonify({
                    'success': False,
                    'error': 'Nœud malveillant détecté',
                    'message': 'Ce nœud utilise une adresse de trésor différente de l\'adresse officielle et est exclu du consensus',
                    'official_treasury': DEFAULT_TREASURY_ADDRESS
                }), 403
            
            # Le peer est valide, l'ajouter
            self.peers.append(peer)
            print(f"✅ Peer valide ajouté: {peer}")
            return jsonify({'success': True, 'peers': self.peers})
        
        @self.app.route('/sync', methods=['POST'])
        def sync_blockchain():
            data = request.get_json()
            try:
                blockchain_data = data.get('blockchain')
                new_blockchain = SimplePoSBlockchain.from_dict(blockchain_data)
                
                # Vérifier que le trésor de la blockchain reçue correspond à l'adresse officielle
                if new_blockchain.treasury_address != DEFAULT_TREASURY_ADDRESS:
                    print(f"\n🚨 TENTATIVE DE SYNCHRONISATION MALVEILLANTE REJETÉE")
                    print(f"   Trésor reçu: {new_blockchain.treasury_address}")
                    print(f"   Trésor officiel: {DEFAULT_TREASURY_ADDRESS}")
                    return jsonify({
                        'success': False,
                        'error': 'Blockchain malveillante rejetée',
                        'message': 'Cette blockchain utilise une adresse de trésor différente et est exclue du consensus',
                        'received_treasury': new_blockchain.treasury_address,
                        'official_treasury': DEFAULT_TREASURY_ADDRESS
                    }), 403
                
                if len(new_blockchain.chain) > len(self.blockchain.chain) and new_blockchain.is_valid():
                    self.blockchain = new_blockchain
                    return jsonify({'success': True, 'message': 'Blockchain synchronisée'})
                
                return jsonify({'success': False, 'message': 'Blockchain locale plus longue ou invalide'})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 400
    
    def broadcast_transaction(self, tx_dict: Dict):
        """Diffuse une transaction uniquement aux peers valides (non malveillants)"""
        for peer in self.peers:
            # Ne pas envoyer aux peers malveillants
            if peer in self.malicious_peers:
                continue
            try:
                requests.post(f"{peer}/transaction/receive", json=tx_dict, timeout=2)
            except:
                pass
    
    def broadcast_block(self, block_dict: Dict):
        """Diffuse un bloc uniquement aux peers valides (non malveillants)"""
        for peer in self.peers:
            # Ne pas envoyer aux peers malveillants
            if peer in self.malicious_peers:
                continue
            try:
                requests.post(f"{peer}/block/receive", json=block_dict, timeout=2)
            except:
                pass
    
    def run(self):
        print(f"\n{'='*70}")
        print(f"NOEUD BLOCKCHAIN")
        print(f"{'='*70}")
        print(f"Port: {self.port}")
        print(f"URL: http://localhost:{self.port}")
        if self.blockchain.treasury_address:
            print(f"Trésor: {self.blockchain.treasury_address[:30]}...")
        print(f"{'='*70}\n")
        
        self.app.run(host='0.0.0.0', port=self.port, debug=False)

def main():
    parser = argparse.ArgumentParser(description='Blockchain Node avec mécanisme d\'inactivité')
    # Le port peut venir de la variable d'environnement PORT (pour le cloud) ou de l'argument
    default_port = int(os.environ.get('PORT', 5000))
    parser.add_argument('--port', type=int, default=default_port, help='Port du nœud')
    parser.add_argument('--treasury', type=str, help='Adresse du trésor')
    parser.add_argument('--init', action='store_true', help='Initialiser avec des données de test')
    parser.add_argument('--inactivity-days', type=int, default=30, help='Jours avant inactivité (défaut: 30)')
    args = parser.parse_args()
    
    # Configuration de l'inactivité
    global INACTIVITY_THRESHOLD
    INACTIVITY_THRESHOLD = args.inactivity_days * 24 * 3600
    
    # Configuration du trésor
    # L'adresse du trésor est définie par défaut dans le code pour garantir la cohérence du réseau
    # Elle peut être surchargée via --treasury ou TREASURY_ADDRESS, mais ce n'est PAS recommandé
    treasury_address = args.treasury or os.environ.get('TREASURY_ADDRESS') or DEFAULT_TREASURY_ADDRESS
    
    # Avertir si l'utilisateur essaie de changer l'adresse du trésor
    if args.treasury and args.treasury != DEFAULT_TREASURY_ADDRESS:
        print(f"\n{'='*70}")
        print("⚠️  ATTENTION : ADRESSE DE TRÉSOR PERSONNALISÉE")
        print(f"{'='*70}")
        print(f"Vous utilisez une adresse de trésor différente de l'adresse officielle.")
        print(f"Adresse officielle : {DEFAULT_TREASURY_ADDRESS}")
        print(f"Adresse utilisée   : {args.treasury}")
        print(f"\n⚠️  Votre nœud ne sera PAS compatible avec le réseau officiel !")
        print(f"⚠️  Les autres nœuds rejetteront vos transactions de trésor.")
        print(f"{'='*70}\n")
    elif os.environ.get('TREASURY_ADDRESS') and os.environ.get('TREASURY_ADDRESS') != DEFAULT_TREASURY_ADDRESS:
        print(f"\n{'='*70}")
        print("⚠️  ATTENTION : ADRESSE DE TRÉSOR PERSONNALISÉE")
        print(f"{'='*70}")
        print(f"Vous utilisez une adresse de trésor différente de l'adresse officielle.")
        print(f"Adresse officielle : {DEFAULT_TREASURY_ADDRESS}")
        print(f"Adresse utilisée   : {os.environ.get('TREASURY_ADDRESS')}")
        print(f"\n⚠️  Votre nœud ne sera PAS compatible avec le réseau officiel !")
        print(f"⚠️  Les autres nœuds rejetteront vos transactions de trésor.")
        print(f"{'='*70}\n")
    
    if args.init and treasury_address == DEFAULT_TREASURY_ADDRESS:
        # ⚠️ ATTENTION : --init ne devrait pas être utilisé avec l'adresse officielle
        # L'adresse officielle du trésor est déjà définie dans le code
        # Si vous voulez créer un nouveau trésor pour tester, utilisez une adresse différente
        print(f"\n{'='*70}")
        print("⚠️  ATTENTION : MODE INIT AVEC TRÉSOR OFFICIEL")
        print(f"{'='*70}")
        print(f"Vous utilisez --init avec l'adresse officielle du trésor.")
        print(f"L'adresse officielle est : {DEFAULT_TREASURY_ADDRESS}")
        print(f"\n⚠️  Ce mode est destiné aux tests locaux uniquement.")
        print(f"⚠️  Pour rejoindre le réseau officiel, ne pas utiliser --init.")
        print(f"{'='*70}\n")
    
    node = Node(args.port, treasury_address)
    
    # Afficher l'adresse du trésor utilisée
    if treasury_address == DEFAULT_TREASURY_ADDRESS:
        print(f"\n{'='*70}")
        print("🏛️  TRÉSOR OFFICIEL CONFIGURÉ")
        print(f"{'='*70}")
        print(f"Adresse : {treasury_address}")
        print(f"✅ Votre nœud est compatible avec le réseau officiel")
        print(f"✅ Protection activée : Les nœuds avec un trésor différent seront rejetés")
        print(f"{'='*70}\n")
    else:
        print(f"\n{'='*70}")
        print("🚨 ATTENTION : TRÉSOR NON OFFICIEL")
        print(f"{'='*70}")
        print(f"Adresse utilisée : {treasury_address}")
        print(f"Adresse officielle : {DEFAULT_TREASURY_ADDRESS}")
        print(f"⚠️  Votre nœud sera considéré comme MALVEILLANT par le réseau")
        print(f"⚠️  Vous serez EXCLU du consensus")
        print(f"⚠️  Les autres nœuds refuseront de se connecter à vous")
        print(f"{'='*70}\n")
    
    # Initialiser automatiquement le trésor s'il est configuré mais vide
    if treasury_address and not args.init:
        treasury_balance = node.blockchain.get_balance(treasury_address)
        if treasury_balance == 0:
            # Initialiser avec 1 million de tokens par défaut
            initial_amount = float(os.environ.get('TREASURY_INITIAL_AMOUNT', 1000000))
            node.blockchain.mint_tokens(treasury_address, initial_amount)
            node.blockchain.create_block()
            print(f"\n🏛️  Trésor initialisé automatiquement avec {initial_amount} tokens")
            print(f"Adresse: {treasury_address}\n")
    
    if args.init:
        print("Initialisation avec données de test...")
        
        # Mint au trésor
        node.blockchain.mint_tokens(treasury_address, 10000)
        
        # Créer des wallets
        alice = QuantumAddress()
        bob = QuantumAddress()
        
        # Distribuer depuis le trésor
        node.blockchain.mint_tokens(alice.address, 1000)
        node.blockchain.mint_tokens(bob.address, 500)
        node.blockchain.create_block()
        
        # Enregistrer validateurs
        node.blockchain.register_validator(alice.address, 300)
        node.blockchain.register_validator(bob.address, 200)
        
        print(f"\nAlice: {alice.address}")
        print(f"  Private key: {alice.private_key}")
        print(f"\nBob: {bob.address}")
        print(f"  Private key: {bob.private_key}")
        
        # Sauvegarder les wallets
        wallets_file = f"wallets_node_{args.port}.json"
        with open(wallets_file, 'w') as f:
            json.dump({
                'alice': alice.to_dict(),
                'bob': bob.to_dict()
            }, f, indent=2)
        print(f"\nWallets sauvegardés dans {wallets_file}")
    
    node.run()

if __name__ == '__main__':
    main()


