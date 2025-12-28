#!/usr/bin/env python3
"""
Script pour vérifier que tous les nœuds ont le bon TREASURY_ADDRESS configuré

Utilisation:
    python verify_treasury.py <url_node1> [url_node2] ... [url_nodeN]
    
Exemple:
    python verify_treasury.py \
      https://blockchain-node-1.onrender.com \
      https://blockchain-node-2.onrender.com \
      https://blockchain-node-27.onrender.com
"""

import sys
import requests
import json

# Importer l'adresse du trésor officielle depuis le code
try:
    # Essayer d'importer depuis blockchain_node.py
    import blockchain_node
    EXPECTED_TREASURY = blockchain_node.DEFAULT_TREASURY_ADDRESS
except (ImportError, AttributeError):
    # Fallback si l'import échoue
    EXPECTED_TREASURY = "Qbd7901a83d578aabe02710c57540c19242a3941d178bed"

def verify_treasury(node_url, expected_treasury=EXPECTED_TREASURY):
    """Vérifie que le nœud a le trésor configuré correctement"""
    
    node_url = node_url.rstrip('/')
    
    try:
        # Vérifier que le nœud est en ligne
        health_response = requests.get(f"{node_url}/health", timeout=10)
        if health_response.status_code != 200:
            print(f"❌ ERREUR: Le nœud {node_url} n'est pas accessible (HTTP {health_response.status_code})")
            return False
        
        # Récupérer le statut de la blockchain
        response = requests.get(f"{node_url}/blockchain/status", timeout=10)
        
        if response.status_code != 200:
            print(f"❌ ERREUR: Impossible de récupérer le statut (HTTP {response.status_code})")
            return False
        
        data = response.json()
        treasury = data.get('treasury')
        blocks = data.get('blocks', 0)
        validators = data.get('validators', 0)
        
        # Vérifier le trésor
        if treasury is None:
            print(f"❌ ERREUR: Le nœud {node_url} n'a PAS de trésor configuré!")
            print(f"   → Solution: Ajoutez TREASURY_ADDRESS dans les variables d'environnement")
            print(f"   → Valeur attendue: {expected_treasury}")
            return False
        
        elif treasury != expected_treasury:
            print(f"⚠️  ATTENTION: Le nœud {node_url} a un trésor DIFFÉRENT!")
            print(f"   → Trésor attendu: {expected_treasury}")
            print(f"   → Trésor trouvé:   {treasury}")
            print(f"   → Solution: Corrigez TREASURY_ADDRESS dans les variables d'environnement")
            return False
        
        else:
            treasury_balance = data.get('treasury_balance', 0)
            print(f"✅ {node_url}")
            print(f"   Trésor: {treasury[:20]}... (correct)")
            print(f"   Balance: {treasury_balance:,.0f} tokens")
            print(f"   Blocs: {blocks}, Validateurs: {validators}")
            return True
            
    except requests.exceptions.Timeout:
        print(f"❌ TIMEOUT: Le nœud {node_url} ne répond pas (timeout)")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ ERREUR DE CONNEXION: Impossible de se connecter à {node_url}")
        print(f"   → Vérifiez que l'URL est correcte et que le nœud est en ligne")
        return False
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_treasury.py <url_node1> [url_node2] ... [url_nodeN]")
        print("\nExemple:")
        print("  python verify_treasury.py \\")
        print("    https://blockchain-node-1.onrender.com \\")
        print("    https://blockchain-node-2.onrender.com \\")
        print("    https://blockchain-node-27.onrender.com")
        print(f"\nTrésor attendu: {EXPECTED_TREASURY}")
        sys.exit(1)
    
    print(f"\n{'='*70}")
    print("VÉRIFICATION DE LA CONFIGURATION DU TRÉSOR")
    print(f"{'='*70}")
    print(f"\nTrésor attendu: {EXPECTED_TREASURY}")
    print(f"Nœuds à vérifier: {len(sys.argv) - 1}\n")
    print(f"{'='*70}\n")
    
    all_ok = True
    results = []
    
    for i, url in enumerate(sys.argv[1:], 1):
        print(f"[{i}/{len(sys.argv)-1}] Vérification de {url}...")
        result = verify_treasury(url)
        results.append((url, result))
        all_ok = all_ok and result
        print()
    
    # Résumé
    print(f"{'='*70}")
    print("RÉSUMÉ")
    print(f"{'='*70}\n")
    
    ok_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    for url, result in results:
        status = "✅ OK" if result else "❌ ERREUR"
        print(f"{status} - {url}")
    
    print(f"\n{'='*70}")
    if all_ok:
        print(f"✅ SUCCÈS: Tous les nœuds ({total_count}/{total_count}) ont le bon trésor configuré!")
        print(f"{'='*70}\n")
        return 0
    else:
        print(f"❌ ÉCHEC: {total_count - ok_count} nœud(s) sur {total_count} ont des problèmes!")
        print(f"{'='*70}\n")
        print("Actions recommandées:")
        print("  1. Vérifiez les variables d'environnement de chaque nœud")
        print("  2. Ajoutez ou corrigez TREASURY_ADDRESS")
        print("  3. Redéployez les nœuds si nécessaire")
        print("  4. Relancez ce script pour vérifier")
        return 1

if __name__ == '__main__':
    sys.exit(main())

