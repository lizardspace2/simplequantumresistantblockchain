#!/usr/bin/env python3
"""
Script pour connecter deux nœuds blockchain ensemble

Utilisation:
    python connect_nodes.py <url_node1> <url_node2>
    
Exemple:
    python connect_nodes.py https://blockchain-node-uu6y.onrender.com https://blockchain-node-2.onrender.com
"""

import sys
import requests
import json

def connect_nodes(node1_url: str, node2_url: str):
    """Connecte deux nœuds ensemble (bidirectionnel)"""
    
    print(f"\n{'='*70}")
    print("CONNEXION DE DEUX NŒUDS BLOCKCHAIN")
    print(f"{'='*70}\n")
    
    # Nettoyer les URLs (enlever le slash final)
    node1_url = node1_url.rstrip('/')
    node2_url = node2_url.rstrip('/')
    
    print(f"Nœud 1: {node1_url}")
    print(f"Nœud 2: {node2_url}\n")
    
    # Vérifier que les nœuds sont en ligne
    print("Vérification de la santé des nœuds...")
    try:
        response = requests.get(f"{node1_url}/health", timeout=10)
        if response.status_code == 200:
            print(f"✓ Nœud 1 est en ligne")
        else:
            print(f"✗ Nœud 1 ne répond pas correctement (code: {response.status_code})")
            return False
    except Exception as e:
        print(f"✗ Nœud 1 n'est pas accessible: {e}")
        return False
    
    try:
        response = requests.get(f"{node2_url}/health", timeout=10)
        if response.status_code == 200:
            print(f"✓ Nœud 2 est en ligne")
        else:
            print(f"✗ Nœud 2 ne répond pas correctement (code: {response.status_code})")
            return False
    except Exception as e:
        print(f"✗ Nœud 2 n'est pas accessible: {e}")
        return False
    
    print()
    
    # Connecter le nœud 2 au nœud 1
    print(f"Connexion du nœud 2 au nœud 1...")
    try:
        response = requests.post(
            f"{node2_url}/peers/add",
            json={"peer": node1_url},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✓ Nœud 2 connecté au nœud 1")
                print(f"  Peers du nœud 2: {data.get('peers', [])}")
            else:
                print(f"✗ Échec de la connexion: {data.get('error', 'Erreur inconnue')}")
        else:
            print(f"✗ Erreur HTTP {response.status_code}")
    except Exception as e:
        print(f"✗ Erreur lors de la connexion: {e}")
        return False
    
    # Connecter le nœud 1 au nœud 2
    print(f"\nConnexion du nœud 1 au nœud 2...")
    try:
        response = requests.post(
            f"{node1_url}/peers/add",
            json={"peer": node2_url},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✓ Nœud 1 connecté au nœud 2")
                print(f"  Peers du nœud 1: {data.get('peers', [])}")
            else:
                print(f"✗ Échec de la connexion: {data.get('error', 'Erreur inconnue')}")
        else:
            print(f"✗ Erreur HTTP {response.status_code}")
    except Exception as e:
        print(f"✗ Erreur lors de la connexion: {e}")
        return False
    
    # Vérifier les connexions
    print(f"\n{'='*70}")
    print("VÉRIFICATION DES CONNEXIONS")
    print(f"{'='*70}\n")
    
    try:
        response = requests.get(f"{node1_url}/peers", timeout=10)
        if response.status_code == 200:
            peers1 = response.json().get('peers', [])
            print(f"Nœud 1 - Peers connectés: {len(peers1)}")
            for peer in peers1:
                print(f"  - {peer}")
    except Exception as e:
        print(f"✗ Erreur lors de la vérification du nœud 1: {e}")
    
    try:
        response = requests.get(f"{node2_url}/peers", timeout=10)
        if response.status_code == 200:
            peers2 = response.json().get('peers', [])
            print(f"\nNœud 2 - Peers connectés: {len(peers2)}")
            for peer in peers2:
                print(f"  - {peer}")
    except Exception as e:
        print(f"✗ Erreur lors de la vérification du nœud 2: {e}")
    
    # Synchroniser la blockchain si nécessaire
    print(f"\n{'='*70}")
    print("SYNCHRONISATION DE LA BLOCKCHAIN")
    print(f"{'='*70}\n")
    
    try:
        # Récupérer le statut des deux nœuds
        status1 = requests.get(f"{node1_url}/blockchain/status", timeout=10).json()
        status2 = requests.get(f"{node2_url}/blockchain/status", timeout=10).json()
        
        blocks1 = status1.get('blocks', 0)
        blocks2 = status2.get('blocks', 0)
        
        print(f"Nœud 1: {blocks1} blocs")
        print(f"Nœud 2: {blocks2} blocs")
        
        if blocks1 > blocks2:
            print(f"\nSynchronisation du nœud 2 avec le nœud 1...")
            blockchain = requests.get(f"{node1_url}/blockchain", timeout=30).json()
            response = requests.post(
                f"{node2_url}/sync",
                json={"blockchain": blockchain},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✓ Blockchain synchronisée")
                else:
                    print(f"✗ Échec de la synchronisation: {data.get('message', 'Erreur inconnue')}")
        elif blocks2 > blocks1:
            print(f"\nSynchronisation du nœud 1 avec le nœud 2...")
            blockchain = requests.get(f"{node2_url}/blockchain", timeout=30).json()
            response = requests.post(
                f"{node1_url}/sync",
                json={"blockchain": blockchain},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✓ Blockchain synchronisée")
                else:
                    print(f"✗ Échec de la synchronisation: {data.get('message', 'Erreur inconnue')}")
        else:
            print(f"\n✓ Les deux nœuds ont le même nombre de blocs")
    except Exception as e:
        print(f"✗ Erreur lors de la synchronisation: {e}")
    
    print(f"\n{'='*70}")
    print("CONNEXION TERMINÉE")
    print(f"{'='*70}\n")
    
    return True

def main():
    if len(sys.argv) != 3:
        print("Usage: python connect_nodes.py <url_node1> <url_node2>")
        print("\nExemple:")
        print("  python connect_nodes.py https://blockchain-node-uu6y.onrender.com https://blockchain-node-2.onrender.com")
        sys.exit(1)
    
    node1_url = sys.argv[1]
    node2_url = sys.argv[2]
    
    success = connect_nodes(node1_url, node2_url)
    
    if success:
        print("✅ Les nœuds sont maintenant connectés !")
        print("\nVous pouvez maintenant:")
        print("  - Créer des transactions sur un nœud et elles seront propagées à l'autre")
        print("  - Créer des blocs et ils seront synchronisés")
        print("  - Vérifier le statut avec: curl <url>/blockchain/status")
    else:
        print("❌ Échec de la connexion. Vérifiez les URLs et que les nœuds sont en ligne.")
        sys.exit(1)

if __name__ == '__main__':
    main()

