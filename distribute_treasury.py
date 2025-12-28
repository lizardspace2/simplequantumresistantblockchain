#!/usr/bin/env python3
"""
Script pour distribuer des coins depuis le trésor
Utile pour distribuer gratuitement des coins initiaux aux participants du réseau
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def distribute_from_treasury(treasury_file, recipients_file, amount_per_recipient):
    """Distribuer des coins du trésor à plusieurs adresses"""
    
    # Charger le wallet du trésor
    with open(treasury_file, 'r') as f:
        treasury = json.load(f)
    
    # Charger les adresses des bénéficiaires
    with open(recipients_file, 'r') as f:
        recipients_data = json.load(f)
    
    recipients = recipients_data.get('addresses', [])
    
    if not recipients:
        print("❌ Aucune adresse trouvée dans le fichier recipients.json")
        return
    
    print(f"\n💰 Distribution depuis le trésor")
    print("="*60)
    print(f"Trésor: {treasury['address'][:40]}...")
    print(f"Bénéficiaires: {len(recipients)}")
    print(f"Montant par bénéficiaire: {amount_per_recipient} tokens")
    print(f"Total à distribuer: {len(recipients) * amount_per_recipient} tokens")
    print("="*60)
    
    confirm = input("\nConfirmer la distribution ? (o/n): ")
    if confirm.lower() != 'o':
        print("Distribution annulée")
        return
    
    # Préparer la requête
    data = {
        "recipients": recipients,
        "amount": amount_per_recipient,
        "private_key": treasury['private_key']
    }
    
    # Envoyer
    try:
        response = requests.post(f"{BASE_URL}/treasury/distribute", json=data)
        result = response.json()
        
        if result['success']:
            print(f"\n✅ {len(result['transactions'])} distributions créées avec succès !")
            print("\nLes transactions sont maintenant dans la pool.")
            print("Créez un bloc pour les valider : python wallet_manager.py mine")
        else:
            print(f"\n❌ Erreur: {result.get('error')}")
    
    except Exception as e:
        print(f"\n❌ Erreur lors de la distribution: {e}")

def create_recipients_template():
    """Créer un fichier template pour les bénéficiaires"""
    template = {
        "addresses": [
            "Q1234567890abcdef1234567890abcdef12345678",
            "Qabcdef1234567890abcdef1234567890abcdef12",
            # Ajoutez d'autres adresses ici
        ]
    }
    
    with open('recipients.json', 'w') as f:
        json.dump(template, f, indent=2)
    
    print("✅ Fichier recipients.json créé")
    print("Ajoutez les adresses des bénéficiaires dans ce fichier")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""
Usage:
  # Créer un template de bénéficiaires
  python distribute_treasury.py template
  
  # Distribuer des coins
  python distribute_treasury.py <treasury_file> <recipients_file> <amount>
  
Exemple:
  python distribute_treasury.py treasury_node_5000.json recipients.json 100
        """)
        sys.exit(1)
    
    if sys.argv[1] == 'template':
        create_recipients_template()
    else:
        if len(sys.argv) < 4:
            print("Usage: python distribute_treasury.py <treasury_file> <recipients_file> <amount>")
            sys.exit(1)
        
        treasury_file = sys.argv[1]
        recipients_file = sys.argv[2]
        amount = float(sys.argv[3])
        
        distribute_from_treasury(treasury_file, recipients_file, amount)


