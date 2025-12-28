#!/usr/bin/env python3
"""
BLOCKCHAIN NODE

Installation:
    pip install flask requests

Utilisation:
    python blockchain_node.py --port 5000 --treasury <adresse>
"""

import hashlib
import json
import time
import random
import argparse
import os
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
        self.tx_type = tx_type  # TRANSFER, VALIDATOR_REWARD, etc.
    
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
        return self.signature is not None and len(self.signature) == 128
    
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
    
    def add_transaction(self, tx: Transaction) -> bool:
        if not tx.is_valid():
            return False
        
        if tx.sender in ["SYSTEM"]:
            self.pending_transactions.append(tx)
            return True
        
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
        
        block = Block(
            len(self.chain),
            self.pending_transactions.copy(),
            self.get_latest_block().hash,
            validator,
            validator_stake
        )
        
        for tx in self.pending_transactions:
            if tx.sender not in ["SYSTEM"]:
                self.balances[tx.sender] = self.get_balance(tx.sender) - (tx.amount + tx.fee)
            self.balances[tx.recipient] = self.get_balance(tx.recipient) + tx.amount
        
        total_reward = self.block_reward + self.transaction_fees_pool
        self.balances[validator] = self.get_balance(validator) + total_reward
        self.update_activity(validator)  # Valider = activité
        
        self.chain.append(block)
        self.pending_transactions = []
        self.transaction_fees_pool = 0
        
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
        self.app = Flask(__name__)
        self.setup_routes()
    
    def setup_routes(self):
        
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
            
            tx = Transaction(
                data['sender'],
                data['recipient'],
                float(data['amount']),
                float(data.get('fee', 0.01)),
                int(data.get('nonce', 0))
            )
            tx.sign(wallet)
            
            if self.blockchain.add_transaction(tx):
                self.broadcast_transaction(tx.to_dict())
                return jsonify({
                    'success': True,
                    'transaction': tx.to_dict(),
                    'message': 'Transaction ajoutée à la pool'
                })
            else:
                return jsonify({'success': False, 'error': 'Transaction invalide'}), 400
        
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
                'inactivity_threshold_days': self.blockchain.inactivity_threshold / (24 * 3600)
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
            return jsonify({'peers': self.peers})
        
        @self.app.route('/peers/add', methods=['POST'])
        def add_peer():
            data = request.get_json()
            peer = data.get('peer')
            if peer and peer not in self.peers:
                self.peers.append(peer)
                return jsonify({'success': True, 'peers': self.peers})
            return jsonify({'success': False}), 400
        
        @self.app.route('/sync', methods=['POST'])
        def sync_blockchain():
            data = request.get_json()
            try:
                blockchain_data = data.get('blockchain')
                new_blockchain = SimplePoSBlockchain.from_dict(blockchain_data)
                
                if len(new_blockchain.chain) > len(self.blockchain.chain) and new_blockchain.is_valid():
                    self.blockchain = new_blockchain
                    return jsonify({'success': True, 'message': 'Blockchain synchronisée'})
                
                return jsonify({'success': False, 'message': 'Blockchain locale plus longue ou invalide'})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 400
    
    def broadcast_transaction(self, tx_dict: Dict):
        for peer in self.peers:
            try:
                requests.post(f"{peer}/transaction/receive", json=tx_dict, timeout=2)
            except:
                pass
    
    def broadcast_block(self, block_dict: Dict):
        for peer in self.peers:
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
    
    # Créer le trésor si demandé
    # Le trésor peut venir de l'argument --treasury ou de la variable d'environnement TREASURY_ADDRESS
    treasury_address = args.treasury or os.environ.get('TREASURY_ADDRESS')
    
    if args.init and not treasury_address:
        # Créer automatiquement le trésor
        treasury_wallet = QuantumAddress()
        treasury_address = treasury_wallet.address
        
        # Sauvegarder le wallet du trésor
        treasury_file = f"treasury_node_{args.port}.json"
        with open(treasury_file, 'w') as f:
            json.dump(treasury_wallet.to_dict(), f, indent=2)
        
        print(f"\n🏛️  Trésor créé automatiquement")
        print(f"Adresse: {treasury_address}")
        print(f"Clé privée sauvegardée dans: {treasury_file}\n")
    
    node = Node(args.port, treasury_address)
    
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


