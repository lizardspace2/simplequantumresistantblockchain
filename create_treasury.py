#!/usr/bin/env python3
"""
Script pour créer une adresse trésor (Treasury Address)
Cette adresse vous donnera un accès illimité aux tokens de la blockchain.
"""

import hashlib
import json
import time
import random
import os
from datetime import datetime

class QuantumAddress:
    def __init__(self):
        seed = str(time.time()) + str(random.random())
        self.private_key = hashlib.sha3_512(seed.encode()).hexdigest()
        self.public_key = hashlib.sha3_512(self.private_key.encode()).hexdigest()
        
        addr_hash = hashlib.sha3_256(self.public_key.encode()).hexdigest()
        checksum = hashlib.sha3_256(addr_hash.encode()).hexdigest()[:6]
        self.address = f"Q{addr_hash[:40]}{checksum}"
    
    def to_dict(self):
        return {
            'address': self.address,
            'public_key': self.public_key,
            'private_key': self.private_key,
            'created_at': datetime.now().isoformat(),
            'type': 'treasury'
        }

def main():
    print("=" * 70)
    print("🏛️  CRÉATION D'UNE ADRESSE TRÉSOR")
    print("=" * 70)
    print()
    print("Cette adresse vous donnera un contrôle total sur les tokens.")
    print("⚠️  IMPORTANT : Gardez votre clé privée SECRÈTE et SÉCURISÉE !")
    print()
    
    # Créer le wallet trésor
    treasury_wallet = QuantumAddress()
    
    # Sauvegarder dans un fichier
    treasury_file = "treasury_wallet.json"
    with open(treasury_file, 'w') as f:
        json.dump(treasury_wallet.to_dict(), f, indent=2)
    
    print("✅ Adresse trésor créée avec succès !")
    print()
    print("=" * 70)
    print("📋 INFORMATIONS DU TRÉSOR")
    print("=" * 70)
    print()
    print(f"Adresse (TREASURY_ADDRESS) :")
    print(f"  {treasury_wallet.address}")
    print()
    print(f"Clé publique :")
    print(f"  {treasury_wallet.public_key}")
    print()
    print("⚠️  CLEF PRIVÉE (À GARDER SECRÈTE) :")
    print(f"  {treasury_wallet.private_key}")
    print()
    print("=" * 70)
    print("💾 SAUVEGARDE")
    print("=" * 70)
    print(f"Les informations sont sauvegardées dans : {treasury_file}")
    print()
    print("⚠️  SÉCURITÉ :")
    print("  1. Ne partagez JAMAIS votre clé privée")
    print("  2. Sauvegardez ce fichier dans un endroit sûr (clé USB, cloud chiffré)")
    print("  3. Ne commitez JAMAIS ce fichier dans Git")
    print("  4. Vous pouvez supprimer le fichier après avoir noté les informations")
    print()
    print("=" * 70)
    print("☁️  CONFIGURATION POUR RENDER")
    print("=" * 70)
    print()
    print("Dans Render, ajoutez cette variable d'environnement :")
    print()
    print("  Nom de la variable : TREASURY_ADDRESS")
    print(f"  Valeur : {treasury_wallet.address}")
    print()
    print("=" * 70)
    print()
    print("✅ Votre adresse trésor est prête à être utilisée !")
    print()

if __name__ == '__main__':
    main()

