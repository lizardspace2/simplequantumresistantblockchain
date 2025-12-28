# 🚀 Guide : Déployer un Deuxième Nœud Blockchain

Ce guide vous explique comment déployer un deuxième nœud blockchain et le connecter à votre premier nœud.

## 📋 Prérequis

1. ✅ Votre premier nœud est déployé et fonctionne (ex: `https://blockchain-node-uu6y.onrender.com`)
2. ✅ Vous avez accès à votre compte Render (ou la plateforme utilisée)
3. ✅ Votre code est dans un dépôt Git (GitHub/GitLab)

## 🎯 Option 1 : Déployer sur Render (Recommandé)

### Étape 1 : Créer un nouveau service

1. Allez sur **https://dashboard.render.com**
2. Cliquez sur **"New +"** en haut à droite
3. Sélectionnez **"Web Service"**
4. Connectez votre dépôt GitHub/GitLab (si pas déjà fait)
5. Sélectionnez le même dépôt que votre premier nœud

### Étape 2 : Configurer le deuxième nœud

**Paramètres à remplir :**

- **Name** : `blockchain-node-2` (ou un nom différent de votre premier nœud)
- **Environment** : `Python 3`
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `python blockchain_node.py --port $PORT`
- **Plan** : **Free** (gratuit)

**Variables d'environnement :**

**✅ BONNE NOUVELLE :** L'adresse du trésor est maintenant **codée directement dans le code** !

- **Vous n'avez PAS besoin** de définir `TREASURY_ADDRESS` - elle est automatique
- Tous les nœuds utilisent automatiquement la même adresse officielle : `Qbd7901a83d578aabe02710c57540c19242a3941d178bed`
- Cela garantit que tous les nœuds sont compatibles avec le réseau

**⚠️ Si vous définissez TREASURY_ADDRESS avec une valeur différente :**
- Votre nœud ne sera PAS compatible avec le réseau officiel
- Un avertissement sera affiché au démarrage
- Les autres nœuds rejetteront vos transactions de trésor

**⚠️ Autres notes importantes :** 
- Ne définissez PAS la variable `PORT` - Render la définit automatiquement
- Tous les nœuds partagent automatiquement la même blockchain grâce au trésor officiel

### Étape 3 : Déployer

1. Cliquez sur **"Create Web Service"**
2. Attendez 2-3 minutes pour le déploiement
3. Notez l'URL de votre deuxième nœud (ex: `https://blockchain-node-2.onrender.com`)

### Étape 4 : Connecter les deux nœuds

Une fois les deux nœuds déployés, connectez-les ensemble :

**URLs de vos nœuds :**
- Nœud 1 : `https://blockchain-node-uu6y.onrender.com`
- Nœud 2 : `https://blockchain-node-2.onrender.com` (remplacez par votre URL)

**Connecter le nœud 2 au nœud 1 :**

**Windows (PowerShell) :**
```powershell
$node2Url = "https://blockchain-node-2.onrender.com"
$node1Url = "https://blockchain-node-uu6y.onrender.com"

Invoke-RestMethod -Uri "$node2Url/peers/add" -Method POST -ContentType "application/json" -Body (@{peer=$node1Url} | ConvertTo-Json)
```

**macOS/Linux :**
```bash
NODE1_URL="https://blockchain-node-uu6y.onrender.com"
NODE2_URL="https://blockchain-node-2.onrender.com"

curl -X POST "$NODE2_URL/peers/add" \
  -H "Content-Type: application/json" \
  -d "{\"peer\": \"$NODE1_URL\"}"
```

**Connecter le nœud 1 au nœud 2 (pour une connexion bidirectionnelle) :**

**Windows (PowerShell) :**
```powershell
Invoke-RestMethod -Uri "$node1Url/peers/add" -Method POST -ContentType "application/json" -Body (@{peer=$node2Url} | ConvertTo-Json)
```

**macOS/Linux :**
```bash
curl -X POST "$NODE1_URL/peers/add" \
  -H "Content-Type: application/json" \
  -d "{\"peer\": \"$NODE2_URL\"}"
```

### Étape 5 : Vérifier la configuration du trésor

**⚠️ IMPORTANT :** Vérifiez que les deux nœuds ont le bon `TREASURY_ADDRESS` configuré :

**Option A : Utiliser le script de vérification (Recommandé)**
```bash
python verify_treasury.py \
  https://blockchain-node-uu6y.onrender.com \
  https://blockchain-node-2.onrender.com
```

**Option B : Vérifier manuellement**
```bash
# Vérifier le trésor du nœud 1
curl https://blockchain-node-uu6y.onrender.com/blockchain/status | jq .treasury

# Vérifier le trésor du nœud 2
curl https://blockchain-node-2.onrender.com/blockchain/status | jq .treasury
```

**Réponse attendue :** `"Qbd7901a83d578aabe02710c57540c19242a3941d178bed"`

Si vous voyez `null`, le nœud n'a pas `TREASURY_ADDRESS` configuré. Consultez [TREASURY_ADDRESS_IMPORTANCE.md](TREASURY_ADDRESS_IMPORTANCE.md) pour savoir comment corriger.

### Étape 6 : Vérifier la connexion

**Vérifier les peers du nœud 1 :**
```bash
curl https://blockchain-node-uu6y.onrender.com/peers
```

**Vérifier les peers du nœud 2 :**
```bash
curl https://blockchain-node-2.onrender.com/peers
```

**Réponse attendue :**
```json
{
  "peers": [
    "https://blockchain-node-2.onrender.com"
  ]
}
```

### Étape 7 : Synchroniser la blockchain

Si votre premier nœud a déjà des blocs, synchronisez le deuxième nœud :

**Windows (PowerShell) :**
```powershell
# Récupérer la blockchain du nœud 1
$blockchain = Invoke-RestMethod -Uri "$node1Url/blockchain"

# Synchroniser le nœud 2
$syncData = @{
    blockchain = $blockchain
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "$node2Url/sync" -Method POST -ContentType "application/json" -Body $syncData
```

**macOS/Linux :**
```bash
# Récupérer la blockchain du nœud 1
BLOCKCHAIN=$(curl -s "$NODE1_URL/blockchain")

# Synchroniser le nœud 2
curl -X POST "$NODE2_URL/sync" \
  -H "Content-Type: application/json" \
  -d "{\"blockchain\": $BLOCKCHAIN}"
```

## 🎯 Option 2 : Déployer sur une autre plateforme

### Railway

1. Créez un nouveau projet sur **https://railway.app**
2. Cliquez sur **"Deploy from GitHub repo"**
3. Sélectionnez le même dépôt
4. Dans les **Settings** :
   - **Start Command** : `python blockchain_node.py --port $PORT`
   - Ajoutez `TREASURY_ADDRESS` si nécessaire
5. Générez un domaine
6. Connectez les nœuds comme expliqué ci-dessus

### Fly.io

1. Dans le dossier de votre projet :
```bash
fly launch --name blockchain-node-2
```
2. Répondez aux questions
3. Déployez : `fly deploy`
4. Connectez les nœuds comme expliqué ci-dessus

## 🔄 Comment fonctionne la synchronisation

Une fois connectés, les nœuds :

1. **Diffusent les transactions** : Quand une transaction est créée sur un nœud, elle est automatiquement envoyée aux autres nœuds
2. **Diffusent les blocs** : Quand un bloc est créé, il est envoyé à tous les peers
3. **Synchronisent automatiquement** : Les nœuds peuvent synchroniser leur blockchain via `/sync`

## 🧪 Tester votre réseau multi-nœuds

### Test 1 : Créer une transaction sur le nœud 1

```bash
curl -X POST https://blockchain-node-uu6y.onrender.com/transaction/send \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "VOTRE_ADRESSE",
    "recipient": "ADRESSE_DESTINATAIRE",
    "amount": 10,
    "private_key": "VOTRE_CLE_PRIVEE"
  }'
```

### Test 2 : Vérifier que la transaction apparaît sur le nœud 2

```bash
curl https://blockchain-node-2.onrender.com/blockchain/status
```

Vous devriez voir la transaction dans `pending_transactions`.

### Test 3 : Créer un bloc sur le nœud 1

```bash
curl -X POST https://blockchain-node-uu6y.onrender.com/block/mine
```

### Test 4 : Vérifier que le bloc apparaît sur le nœud 2

```bash
curl https://blockchain-node-2.onrender.com/blockchain
```

Le nouveau bloc devrait apparaître dans la chaîne du nœud 2.

## 📊 Vérifier le statut des deux nœuds

**Nœud 1 :**
```bash
curl https://blockchain-node-uu6y.onrender.com/blockchain/status
```

**Nœud 2 :**
```bash
curl https://blockchain-node-2.onrender.com/blockchain/status
```

Les deux nœuds devraient avoir le même nombre de blocs (après synchronisation).

## 🐛 Dépannage

### Les nœuds ne se connectent pas

1. **Vérifiez que les deux nœuds sont en ligne :**
   ```bash
   curl https://blockchain-node-uu6y.onrender.com/health
   curl https://blockchain-node-2.onrender.com/health
   ```

2. **Vérifiez les URLs** : Assurez-vous d'utiliser les bonnes URLs (avec `https://`)

3. **Vérifiez les logs** : Regardez les logs dans le dashboard Render pour voir les erreurs

### La synchronisation ne fonctionne pas

1. **Vérifiez que les nœuds sont connectés :**
   ```bash
   curl https://blockchain-node-2.onrender.com/peers
   ```

2. **Synchronisez manuellement** : Utilisez la commande de synchronisation ci-dessus

3. **Vérifiez que le nœud 1 a des blocs :**
   ```bash
   curl https://blockchain-node-uu6y.onrender.com/blockchain/status
   ```

### Les transactions ne se propagent pas

1. **Vérifiez la connexion des peers** : Les nœuds doivent être connectés bidirectionnellement
2. **Vérifiez les logs** : Les erreurs de broadcast apparaissent dans les logs
3. **Testez manuellement** : Créez une transaction et vérifiez qu'elle apparaît sur les deux nœuds

## 💡 Astuces

1. **Même trésor** : Si vous utilisez la même adresse de trésor (`TREASURY_ADDRESS`), les deux nœuds partageront la même blockchain
2. **Connexion bidirectionnelle** : Connectez les nœuds dans les deux sens pour une meilleure synchronisation
3. **Surveillance** : Utilisez `/blockchain/status` régulièrement pour vérifier que les nœuds sont synchronisés
4. **Backup** : Gardez une sauvegarde de vos wallets et de votre trésor

## 🎉 Félicitations !

Vous avez maintenant un réseau blockchain avec deux nœuds connectés ! 

**Prochaines étapes :**
- Déployer un troisième nœud pour plus de redondance
- Configurer un système de monitoring
- Implémenter la synchronisation automatique

---

**Besoin d'aide ?** Consultez le [README.md](README.md) ou ouvrez une issue sur GitHub.

