#!/usr/bin/env python3
"""
wallet_manager.py - Gestionnaire de wallet pour la blockchain

Usage:
    python wallet_manager.py create
    python wallet_manager.py balance <address>
    python wallet_manager.py send <wallet_file> <recipient> <amount>
    python wallet_manager.py validator <wallet_file> <stake>
    python wallet_manager.py mine
    python wallet_manager.py status
    python wallet_manager.py list
    python wallet_manager.py explorer
"""

import requests
import json
import sys
import os
import glob
from datetime import datetime
from typing import Dict, List

BASE_URL = "http://localhost:5000"

class Colors:
    """Couleurs pour le terminal"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.CYAN}ℹ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")

def create_wallet():
    """Créer un nouveau wallet"""
    try:
        response = requests.post(f"{BASE_URL}/wallet/create")
        wallet = response.json()['wallet']
        
        # Sauvegarder
        filename = f"wallet_{wallet['address'][:10]}.json"
        with open(filename, 'w') as f:
            json.dump(wallet, f, indent=2)
        
        print(f"\n{Colors.BOLD}🎉 Nouveau wallet créé !{Colors.END}\n")
        print(f"{Colors.BOLD}Adresse:{Colors.END}")
        print(f"  {wallet['address']}\n")
        print(f"{Colors.BOLD}Clé publique:{Colors.END}")
        print(f"  {wallet['public_key'][:50]}...\n")
        print(f"{Colors.RED}{Colors.BOLD}⚠️  CLEF PRIVEE (À GARDER SECRETE) :{Colors.END}")
        print(f"  {wallet['private_key']}\n")
        print(f"{Colors.GREEN}Sauvegardé dans: {filename}{Colors.END}\n")
        print_warning("Ne partagez JAMAIS votre clé privée !")
        
    except Exception as e:
        print_error(f"Erreur lors de la création du wallet: {e}")

def get_balance(address):
    """Vérifier le solde"""
    try:
        response = requests.get(f"{BASE_URL}/wallet/balance/{address}")
        data = response.json()
        
        print(f"\n{Colors.BOLD}💰 Solde du wallet{Colors.END}")
        print("="*60)
        print(f"Adresse: {address[:30]}...")
        print(f"Disponible: {Colors.GREEN}{data['balance']}{Colors.END} tokens")
        print(f"Staké: {Colors.YELLOW}{data['staked']}{Colors.END} tokens")
        print(f"Total: {Colors.BOLD}{data['total']}{Colors.END} tokens")
        
        # Afficher les infos d'inactivité si disponibles
        if 'inactive_days' in data:
            print(f"\n{Colors.CYAN}Statut d'activité:{Colors.END}")
            print(f"  Dernière activité: {datetime.fromtimestamp(data['last_activity']).strftime('%Y-%m-%d %H:%M:%S') if data['last_activity'] > 0 else 'Jamais'}")
            print(f"  Inactif depuis: {data['inactive_days']:.1f} jours")
        
        print("="*60 + "\n")
        
    except Exception as e:
        print_error(f"Erreur: {e}")

def send_tokens(wallet_file, recipient, amount, fee=1.0):
    """Envoyer des tokens"""
    try:
        # Charger le wallet
        if not os.path.exists(wallet_file):
            print_error(f"Fichier wallet introuvable: {wallet_file}")
            return
        
        with open(wallet_file, 'r') as f:
            wallet = json.load(f)
        
        print(f"\n{Colors.BOLD}📤 Envoi de tokens{Colors.END}")
        print("="*60)
        print(f"De: {wallet['address'][:30]}...")
        print(f"Vers: {recipient[:30]}...")
        print(f"Montant: {amount} tokens")
        print(f"Frais: {fee} tokens")
        print(f"Total: {amount + fee} tokens")
        print("="*60)
        
        # Confirmer
        confirm = input("\nConfirmer la transaction ? (o/n): ")
        if confirm.lower() != 'o':
            print_info("Transaction annulée")
            return
        
        # Préparer la transaction
        tx_data = {
            "sender": wallet['address'],
            "recipient": recipient,
            "amount": amount,
            "fee": fee,
            "private_key": wallet['private_key']
        }
        
        # Envoyer
        response = requests.post(f"{BASE_URL}/transaction/send", json=tx_data)
        result = response.json()
        
        if result['success']:
            print_success(f"Transaction envoyée avec succès !")
            print_info("La transaction est maintenant dans la pool en attente")
            print_info("Elle sera incluse dans le prochain bloc validé")
        else:
            print_error(f"Transaction échouée: {result.get('error')}")
        
    except Exception as e:
        print_error(f"Erreur: {e}")

def register_validator(wallet_file, stake):
    """S'enregistrer comme validateur"""
    try:
        with open(wallet_file, 'r') as f:
            wallet = json.load(f)
        
        print(f"\n{Colors.BOLD}🛡️  Enregistrement comme validateur{Colors.END}")
        print("="*60)
        print(f"Adresse: {wallet['address'][:30]}...")
        print(f"Stake: {stake} tokens")
        print("="*60)
        
        confirm = input("\nConfirmer l'enregistrement ? (o/n): ")
        if confirm.lower() != 'o':
            print_info("Enregistrement annulé")
            return
        
        data = {
            "address": wallet['address'],
            "stake": stake
        }
        
        response = requests.post(f"{BASE_URL}/validator/register", json=data)
        result = response.json()
        
        if result['success']:
            print_success(f"Enregistré comme validateur avec stake de {stake} tokens")
            print_info("Votre stake est maintenant locké")
            print_info("Vous pouvez maintenant participer à la validation des blocs")
        else:
            print_error(f"Enregistrement échoué: {result.get('error')}")
        
    except Exception as e:
        print_error(f"Erreur: {e}")

def mine_block():
    """Créer un nouveau bloc"""
    try:
        print(f"\n{Colors.BOLD}⛏️  Création d'un nouveau bloc...{Colors.END}\n")
        
        response = requests.post(f"{BASE_URL}/block/mine")
        result = response.json()
        
        if result['success']:
            block = result['block']
            print_success(f"Bloc #{block['index']} créé avec succès !")
            print(f"\nValidateur: {block['validator'][:30]}...")
            print(f"Hash: {block['hash'][:50]}...")
            print(f"Transactions: {len(block['transactions'])}")
            print(f"Timestamp: {datetime.fromtimestamp(block['timestamp'])}")
        else:
            print_error(f"Erreur: {result.get('error')}")
            print_info("Vérifiez qu'il y a des transactions en attente et des validateurs")
        
    except Exception as e:
        print_error(f"Erreur: {e}")

def show_status():
    """Afficher le statut de la blockchain"""
    try:
        response = requests.get(f"{BASE_URL}/blockchain/status")
        status = response.json()
        
        print(f"\n{Colors.BOLD}📊 STATUT DE LA BLOCKCHAIN{Colors.END}")
        print("="*60)
        print(f"Blocs: {Colors.GREEN}{status['blocks']}{Colors.END}")
        print(f"Transactions en attente: {Colors.YELLOW}{status['pending_transactions']}{Colors.END}")
        print(f"Validateurs actifs: {Colors.CYAN}{status['validators']}{Colors.END}")
        print(f"Récompense par bloc: {status['block_reward']} tokens")
        print(f"Stake minimum: {status['min_stake']} tokens")
        print(f"Blockchain valide: {Colors.GREEN if status['valid'] else Colors.RED}{status['valid']}{Colors.END}")
        
        if status.get('treasury'):
            print(f"\n{Colors.BOLD}Trésor:{Colors.END}")
            print(f"  Adresse: {status['treasury'][:40]}...")
            print(f"  Balance: {status['treasury_balance']} tokens")
        
        print("="*60)
        
        if status['validator_list']:
            print(f"\n{Colors.BOLD}Validateurs:{Colors.END}")
            for i, validator in enumerate(status['validator_list'], 1):
                print(f"  {i}. {validator[:40]}...")
        
        print()
        
    except Exception as e:
        print_error(f"Erreur: {e}")

def list_wallets():
    """Lister tous les wallets locaux"""
    try:
        wallet_files = glob.glob("wallet_*.json") + glob.glob("wallets_*.json") + glob.glob("treasury_*.json")
        
        if not wallet_files:
            print_warning("Aucun wallet trouvé localement")
            print_info("Créez un wallet avec: python wallet_manager.py create")
            return
        
        print(f"\n{Colors.BOLD}👛 Wallets locaux{Colors.END}")
        print("="*60)
        
        for i, filename in enumerate(wallet_files, 1):
            with open(filename, 'r') as f:
                data = json.load(f)
                
                # Si c'est un fichier avec plusieurs wallets
                if 'alice' in data or 'bob' in data:
                    print(f"\n{i}. {Colors.BOLD}{filename}{Colors.END} (Plusieurs wallets)")
                    for name, wallet in data.items():
                        if isinstance(wallet, dict) and 'address' in wallet:
                            print(f"   {name}: {wallet['address'][:30]}...")
                            try:
                                balance_data = requests.get(f"{BASE_URL}/wallet/balance/{wallet['address']}").json()
                                print(f"   Balance: {balance_data['total']} tokens")
                            except:
                                pass
                else:
                    print(f"\n{i}. {Colors.BOLD}{filename}{Colors.END}")
                    print(f"   Adresse: {data['address'][:40]}...")
                    try:
                        balance_data = requests.get(f"{BASE_URL}/wallet/balance/{data['address']}").json()
                        print(f"   Balance: {balance_data['total']} tokens")
                    except:
                        pass
        
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print_error(f"Erreur: {e}")

def explorer():
    """Mini explorateur de blocs"""
    try:
        response = requests.get(f"{BASE_URL}/blockchain")
        data = response.json()
        
        print(f"\n{Colors.BOLD}🔍 EXPLORATEUR DE BLOCS{Colors.END}")
        print("="*60)
        print(f"Nombre de blocs: {data['length']}")
        print(f"Transactions en attente: {data['pending_transactions']}")
        print(f"Chaîne valide: {Colors.GREEN if data['valid'] else Colors.RED}{data['valid']}{Colors.END}")
        print("="*60)
        
        # Afficher les derniers blocs
        print(f"\n{Colors.BOLD}Derniers blocs:{Colors.END}\n")
        
        for block in reversed(data['chain'][-5:]):  # 5 derniers blocs
            print(f"{Colors.BOLD}Bloc #{block['index']}{Colors.END}")
            print(f"  Hash: {block['hash'][:50]}...")
            print(f"  Validateur: {block['validator'][:30]}...")
            print(f"  Timestamp: {datetime.fromtimestamp(block['timestamp'])}")
            print(f"  Transactions: {len(block['transactions'])}")
            
            if block['transactions']:
                print(f"  {Colors.CYAN}Transactions:{Colors.END}")
                for tx in block['transactions']:
                    sender = tx['sender'][:15] if tx['sender'] != 'SYSTEM' else 'SYSTEM'
                    recipient = tx['recipient'][:15]
                    tx_type = tx.get('tx_type', 'TRANSFER')
                    print(f"    • [{tx_type}] {sender}... → {recipient}...: {tx['amount']} tokens")
            print()
        
    except Exception as e:
        print_error(f"Erreur: {e}")

def show_help():
    """Afficher l'aide"""
    print(f"""
{Colors.BOLD}🔗 Gestionnaire de Wallet - Blockchain Quantum-Résistante{Colors.END}

{Colors.BOLD}COMMANDES:{Colors.END}

  {Colors.CYAN}create{Colors.END}
      Créer un nouveau wallet quantum-résistant
      Exemple: python wallet_manager.py create

  {Colors.CYAN}balance <address>{Colors.END}
      Vérifier le solde d'une adresse
      Exemple: python wallet_manager.py balance Q7a8f3c9d2e1b4f5...

  {Colors.CYAN}send <wallet_file> <recipient> <amount> [fee]{Colors.END}
      Envoyer des tokens à une autre adresse
      Exemple: python wallet_manager.py send wallet_Q7a8f3c9d2.json Q8b9c0d1... 50
      Exemple avec fee: python wallet_manager.py send wallet_Q7a8f3c9d2.json Q8b9c0d1... 50 2

  {Colors.CYAN}validator <wallet_file> <stake>{Colors.END}
      S'enregistrer comme validateur
      Exemple: python wallet_manager.py validator wallet_Q7a8f3c9d2.json 200

  {Colors.CYAN}mine{Colors.END}
      Créer un nouveau bloc (validation PoS)
      Exemple: python wallet_manager.py mine

  {Colors.CYAN}status{Colors.END}
      Afficher le statut de la blockchain
      Exemple: python wallet_manager.py status

  {Colors.CYAN}list{Colors.END}
      Lister tous les wallets locaux
      Exemple: python wallet_manager.py list

  {Colors.CYAN}explorer{Colors.END}
      Afficher les derniers blocs de la chaîne
      Exemple: python wallet_manager.py explorer

  {Colors.CYAN}help{Colors.END}
      Afficher cette aide
      Exemple: python wallet_manager.py help

{Colors.BOLD}CONFIGURATION:{Colors.END}
  URL du nœud: {BASE_URL}
  (Modifiez BASE_URL dans le script pour changer)

{Colors.BOLD}NOTES:{Colors.END}
  • Gardez vos clés privées en sécurité !
  • Les wallets sont sauvegardés localement en JSON
  • Un nœud doit être en cours d'exécution sur {BASE_URL}
""")

def main():
    if len(sys.argv) < 2 or sys.argv[1] == "help":
        show_help()
        return
    
    command = sys.argv[1]
    
    try:
        if command == "create":
            create_wallet()
        
        elif command == "balance":
            if len(sys.argv) < 3:
                print_error("Usage: python wallet_manager.py balance <address>")
                return
            get_balance(sys.argv[2])
        
        elif command == "send":
            if len(sys.argv) < 5:
                print_error("Usage: python wallet_manager.py send <wallet_file> <recipient> <amount> [fee]")
                return
            wallet_file = sys.argv[2]
            recipient = sys.argv[3]
            amount = float(sys.argv[4])
            fee = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
            send_tokens(wallet_file, recipient, amount, fee)
        
        elif command == "validator":
            if len(sys.argv) < 4:
                print_error("Usage: python wallet_manager.py validator <wallet_file> <stake>")
                return
            register_validator(sys.argv[2], float(sys.argv[3]))
        
        elif command == "mine":
            mine_block()
        
        elif command == "status":
            show_status()
        
        elif command == "list":
            list_wallets()
        
        elif command == "explorer":
            explorer()
        
        else:
            print_error(f"Commande inconnue: {command}")
            print_info("Utilisez 'python wallet_manager.py help' pour voir les commandes disponibles")
    
    except KeyboardInterrupt:
        print_info("\nOpération annulée par l'utilisateur")
    except Exception as e:
        print_error(f"Erreur inattendue: {e}")

if __name__ == '__main__':
    main()


