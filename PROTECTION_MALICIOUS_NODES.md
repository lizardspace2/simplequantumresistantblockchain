# 🛡️ Protection contre les Nœuds Malveillants

## 🎯 Vue d'ensemble

Le système implémente maintenant une **protection automatique** contre les nœuds qui utilisent une adresse de trésor différente de l'adresse officielle. Ces nœuds sont considérés comme **malveillants** et sont **automatiquement exclus du consensus**.

## 🔒 Mécanisme de Protection

### Adresse Officielle du Trésor

L'adresse officielle du trésor est **codée directement dans le code** :

```python
DEFAULT_TREASURY_ADDRESS = "Qbd7901a83d578aabe02710c57540c19242a3941d178bed"
```

Tous les nœuds du réseau officiel **doivent** utiliser cette adresse.

### Vérifications Automatiques

Le système effectue plusieurs vérifications pour détecter et exclure les nœuds malveillants :

#### 1. Vérification lors de l'ajout d'un peer (`/peers/add`)

Quand un nœud essaie de se connecter :

1. Le nœud vérifie l'adresse du trésor du peer via `/blockchain/status`
2. Si l'adresse est différente ou absente → **REJET IMMÉDIAT**
3. Le peer est ajouté à la liste des nœuds malveillants
4. Un message d'erreur HTTP 403 est retourné

**Exemple de réponse :**
```json
{
  "success": false,
  "error": "Nœud malveillant détecté",
  "message": "Ce nœud utilise une adresse de trésor différente de l'adresse officielle et est exclu du consensus",
  "official_treasury": "Qbd7901a83d578aabe02710c57540c19242a3941d178bed"
}
```

#### 2. Vérification lors de la synchronisation (`/sync`)

Quand un nœud essaie de synchroniser sa blockchain :

1. Le système vérifie que le trésor de la blockchain reçue correspond à l'adresse officielle
2. Si différent → **REJET IMMÉDIAT** avec erreur HTTP 403
3. La synchronisation est refusée

**Exemple de réponse :**
```json
{
  "success": false,
  "error": "Blockchain malveillante rejetée",
  "message": "Cette blockchain utilise une adresse de trésor différente et est exclue du consensus",
  "received_treasury": "Qautre123...",
  "official_treasury": "Qbd7901a83d578aabe02710c57540c19242a3941d178bed"
}
```

#### 3. Exclusion des broadcasts

Les nœuds malveillants sont **automatiquement exclus** de :
- La diffusion de transactions (`broadcast_transaction`)
- La diffusion de blocs (`broadcast_block`)

Les nœuds valides ne communiquent **jamais** avec les nœuds malveillants.

## 📊 Liste des Nœuds Malveillants

Chaque nœud maintient une liste interne des nœuds malveillants détectés :

```python
self.malicious_peers: List[str] = []
```

Cette liste est consultable via l'endpoint `/peers` :

```bash
curl https://votre-node.onrender.com/peers
```

**Réponse :**
```json
{
  "peers": [
    "https://node-1.onrender.com",
    "https://node-2.onrender.com"
  ],
  "malicious_peers": [
    "https://malicious-node.onrender.com"
  ],
  "total_peers": 2,
  "total_malicious": 1
}
```

## 🚨 Messages d'Avertissement

### Au démarrage d'un nœud avec trésor non officiel

Si quelqu'un démarre un nœud avec une adresse de trésor différente :

```
======================================================================
🚨 ATTENTION : TRÉSOR NON OFFICIEL
======================================================================
Adresse utilisée : Qautre123...
Adresse officielle : Qbd7901a83d578aabe02710c57540c19242a3941d178bed
⚠️  Votre nœud sera considéré comme MALVEILLANT par le réseau
⚠️  Vous serez EXCLU du consensus
⚠️  Les autres nœuds refuseront de se connecter à vous
======================================================================
```

### Lors de la détection d'un nœud malveillant

Quand un nœud valide détecte un nœud malveillant :

```
======================================================================
🚨 NOEUD MALVEILLANT DÉTECTÉ
======================================================================
Peer rejeté: https://malicious-node.onrender.com
Raison: Adresse de trésor différente de l'adresse officielle
Adresse officielle: Qbd7901a83d578aabe02710c57540c19242a3941d178bed
Ce nœud est exclu du consensus et ne sera pas connecté.
======================================================================
```

## ✅ Comportement des Nœuds Valides

### Nœud avec trésor officiel

```
======================================================================
🏛️  TRÉSOR OFFICIEL CONFIGURÉ
======================================================================
Adresse : Qbd7901a83d578aabe02710c57540c19242a3941d178bed
✅ Votre nœud est compatible avec le réseau officiel
✅ Protection activée : Les nœuds avec un trésor différent seront rejetés
======================================================================
```

### Vérification du statut

L'endpoint `/blockchain/status` inclut maintenant :

```json
{
  "blocks": 10,
  "treasury": "Qbd7901a83d578aabe02710c57540c19242a3941d178bed",
  "is_official_treasury": true,
  "malicious_peers_count": 0
}
```

## 🔍 Comment Vérifier

### Vérifier qu'un nœud est valide

```bash
curl https://votre-node.onrender.com/blockchain/status | jq .is_official_treasury
```

**Résultat attendu :** `true`

### Vérifier les nœuds malveillants détectés

```bash
curl https://votre-node.onrender.com/peers | jq .malicious_peers
```

### Utiliser le script de vérification

```bash
python verify_treasury.py \
  https://node-1.onrender.com \
  https://node-2.onrender.com \
  https://node-27.onrender.com
```

## 🛡️ Avantages de cette Protection

1. **Cohérence garantie** : Tous les nœuds valides utilisent la même adresse de trésor
2. **Protection automatique** : Aucune action manuelle nécessaire
3. **Exclusion immédiate** : Les nœuds malveillants sont rejetés dès la tentative de connexion
4. **Pas de contamination** : Les nœuds valides ne communiquent jamais avec les malveillants
5. **Transparence** : Les nœuds malveillants sont listés et visibles

## ⚠️ Conséquences pour les Nœuds Malveillants

Si quelqu'un essaie d'utiliser une adresse de trésor différente :

1. ❌ **Impossible de se connecter** aux nœuds valides
2. ❌ **Impossible de synchroniser** la blockchain
3. ❌ **Aucune communication** avec le réseau officiel
4. ❌ **Exclusion complète** du consensus
5. ⚠️ **Isolation totale** - le nœud fonctionne seul

## 📝 Exemple de Scénario

### Scénario 1 : Tentative de connexion d'un nœud malveillant

**Nœud malveillant essaie de se connecter :**
```bash
curl -X POST https://valid-node.onrender.com/peers/add \
  -H "Content-Type: application/json" \
  -d '{"peer": "https://malicious-node.onrender.com"}'
```

**Réponse du nœud valide :**
```json
{
  "success": false,
  "error": "Nœud malveillant détecté",
  "message": "Ce nœud utilise une adresse de trésor différente de l'adresse officielle et est exclu du consensus",
  "official_treasury": "Qbd7901a83d578aabe02710c57540c19242a3941d178bed"
}
```

**Code HTTP :** `403 Forbidden`

### Scénario 2 : Tentative de synchronisation malveillante

**Nœud malveillant essaie de synchroniser :**
```bash
curl -X POST https://valid-node.onrender.com/sync \
  -H "Content-Type: application/json" \
  -d '{"blockchain": {...}}'
```

**Réponse du nœud valide :**
```json
{
  "success": false,
  "error": "Blockchain malveillante rejetée",
  "message": "Cette blockchain utilise une adresse de trésor différente et est exclue du consensus",
  "received_treasury": "Qautre123...",
  "official_treasury": "Qbd7901a83d578aabe02710c57540c19242a3941d178bed"
}
```

**Code HTTP :** `403 Forbidden`

## 🔧 Implémentation Technique

### Vérification d'un peer

```python
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
```

### Exclusion des broadcasts

```python
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
```

## 📚 Références

- [CHANGELOG_TREASURY.md](CHANGELOG_TREASURY.md) - Changement de l'adresse du trésor
- [TREASURY_ADDRESS_IMPORTANCE.md](TREASURY_ADDRESS_IMPORTANCE.md) - Importance de l'adresse du trésor
- [DEPLOY_SECOND_NODE.md](DEPLOY_SECOND_NODE.md) - Guide de déploiement

---

**Date d'implémentation :** 2025-12-28  
**Version :** 2.1

