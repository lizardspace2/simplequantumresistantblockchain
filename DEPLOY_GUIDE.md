# 🚀 Guide de Déploiement Rapide - Premier Nœud Blockchain

Ce guide vous aide à déployer votre premier nœud blockchain sur un service cloud gratuit.

## 📋 Prérequis

1. ✅ Votre code est dans un dépôt Git (GitHub, GitLab, ou Bitbucket)
2. ✅ Tous les fichiers sont commités et poussés sur le dépôt
3. ✅ Vous avez un compte sur la plateforme choisie

## ⭐ Option Recommandée : Render (Le Plus Simple)

Render est la solution la plus simple pour déployer rapidement votre nœud blockchain.

### Étape 1 : Créer un compte Render

1. Allez sur **https://render.com**
2. Cliquez sur **"Get Started for Free"**
3. Connectez-vous avec **GitHub**, **GitLab** ou votre **email**

### Étape 2 : Connecter votre dépôt

1. Dans le dashboard Render, cliquez sur **"New +"**
2. Sélectionnez **"Web Service"**
3. Connectez votre dépôt GitHub/GitLab
4. Sélectionnez le dépôt `simplequantumresistantblockchain`

### Étape 3 : Configurer le service

**Paramètres à remplir :**

- **Name** : `blockchain-node` (ou le nom de votre choix)
- **Environment** : `Python 3`
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `python blockchain_node.py --port $PORT`
- **Plan** : **Free** (gratuit)

**Variables d'environnement (optionnel) :**

Vous pouvez ajouter des variables d'environnement si nécessaire :
- `TREASURY_ADDRESS` : Adresse du trésor (si vous en avez une)
- `INACTIVITY_DAYS` : Nombre de jours avant inactivité (défaut: 30)

**⚠️ Important :** Ne définissez PAS la variable `PORT` - Render la définit automatiquement.

### Étape 4 : Déployer

1. Cliquez sur **"Create Web Service"**
2. Attendez 2-3 minutes pour le déploiement
3. Render affichera l'URL de votre nœud (ex: `https://blockchain-node.onrender.com`)

### Étape 5 : Tester votre nœud

Une fois déployé, testez votre nœud avec ces commandes :

```bash
# Vérifier que le nœud est en ligne
curl https://votre-app.onrender.com/health

# Créer un wallet
curl -X POST https://votre-app.onrender.com/wallet/create

# Vérifier le statut de la blockchain
curl https://votre-app.onrender.com/blockchain/status
```

**Réponse attendue pour `/health` :**
```json
{
  "status": "online",
  "port": 10000
}
```

### ⚠️ Note importante sur le plan gratuit

- Le service s'endort après **15 minutes d'inactivité**
- La première requête après le sommeil prendra **30-60 secondes** pour redémarrer
- C'est normal et gratuit ! Pour un service toujours actif, utilisez Railway ou Fly.io

---

## 🚂 Alternative : Railway (Service Toujours Actif)

Railway offre 5$ de crédits gratuits par mois et ne s'endort pas.

### Étape 1 : Créer un compte

1. Allez sur **https://railway.app**
2. Cliquez sur **"Start a New Project"**
3. Connectez-vous avec **GitHub**

### Étape 2 : Déployer

1. Cliquez sur **"Deploy from GitHub repo"**
2. Sélectionnez votre dépôt
3. Railway détecte automatiquement Python et installe les dépendances

### Étape 3 : Configurer

1. Dans les **Settings** du service :
   - **Start Command** : `python blockchain_node.py --port $PORT`
2. Railway définit automatiquement la variable `PORT`

### Étape 4 : Obtenir l'URL

1. Cliquez sur l'onglet **"Settings"**
2. Cliquez sur **"Generate Domain"**
3. Votre URL sera : `https://votre-app.up.railway.app`

**💡 Astuce :** Surveillez votre utilisation de crédits dans le dashboard.

---

## ✈️ Alternative : Fly.io (Avec Docker)

Fly.io offre 3 machines virtuelles gratuites et ne s'endort pas.

### Étape 1 : Installer Fly CLI

**Windows (PowerShell) :**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**macOS/Linux :**
```bash
curl -L https://fly.io/install.sh | sh
```

### Étape 2 : Créer un compte

```bash
fly auth signup
```

Ou via le site : https://fly.io

### Étape 3 : Déployer

```bash
# Dans le dossier de votre projet
fly launch

# Répondez aux questions :
# - App name : blockchain-node (ou votre choix)
# - Region : choisissez le plus proche (ex: iad pour Washington)
# - Postgres/Redis : Non
```

### Étape 4 : Vérifier

```bash
# Voir l'URL de votre app
fly status

# Ouvrir dans le navigateur
fly open
```

**Le fichier `fly.toml` est déjà configuré pour vous !**

---

## 🧪 Tester votre nœud déployé

Une fois votre nœud déployé, vous pouvez le tester avec ces commandes :

### 1. Vérifier la santé du nœud

```bash
curl https://votre-url/health
```

### 2. Créer un wallet

```bash
curl -X POST https://votre-url/wallet/create
```

### 3. Vérifier le statut de la blockchain

```bash
curl https://votre-url/blockchain/status
```

### 4. Créer une transaction (exemple)

```bash
curl -X POST https://votre-url/transaction/send \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "VOTRE_ADRESSE",
    "recipient": "ADRESSE_DESTINATAIRE",
    "amount": 10,
    "private_key": "VOTRE_CLE_PRIVEE"
  }'
```

---

## 📊 Comparaison des plateformes

| Plateforme | Gratuit | Sommeil | Performance | Difficulté |
|------------|---------|---------|-------------|-----------|
| **Render** | ✅ Oui | ⚠️ Oui (15 min) | ⭐⭐ | ⭐ Facile |
| **Railway** | ✅ Oui (crédits) | ❌ Non | ⭐⭐⭐ | ⭐ Facile |
| **Fly.io** | ✅ Oui | ❌ Non | ⭐⭐⭐ | ⭐⭐ Moyen |

**Recommandation :**
- **Pour débuter rapidement** : **Render** (le plus simple)
- **Pour un service toujours actif** : **Railway** ou **Fly.io**

---

## 🐛 Dépannage

### Le nœud ne démarre pas

1. Vérifiez les logs dans le dashboard de votre plateforme
2. Vérifiez que la commande de démarrage est correcte : `python blockchain_node.py --port $PORT`
3. Vérifiez que `requirements.txt` contient bien `flask` et `requests`

### Le nœud s'endort (Render uniquement)

- C'est normal avec le plan gratuit
- La première requête après le sommeil prendra 30-60 secondes
- Pour éviter cela, utilisez Railway ou Fly.io

### Erreur de port

- Ne définissez PAS la variable `PORT` manuellement
- Les plateformes la définissent automatiquement
- Le code lit `$PORT` depuis l'environnement

### Le nœud ne répond pas

1. Vérifiez que le service est bien déployé (statut "Live" ou "Running")
2. Vérifiez l'URL dans le dashboard
3. Testez avec `curl` ou un navigateur web

---

## 🔐 Sécurité

Quand vous déployez dans le cloud :

1. **Ne partagez JAMAIS votre clé privée** dans le code ou les variables d'environnement
2. **Utilisez HTTPS** (automatique sur toutes les plateformes)
3. **Sauvegardez vos wallets** localement dans un endroit sûr
4. **Ne commitez JAMAIS** les fichiers de wallet (`.json`) dans Git

---

## 📝 Prochaines étapes

Une fois votre nœud déployé :

1. ✅ Testez les endpoints de l'API
2. ✅ Créez des wallets
3. ✅ Effectuez des transactions
4. ✅ Enregistrez des validateurs
5. ✅ **Déployez un deuxième nœud** : Consultez [DEPLOY_SECOND_NODE.md](DEPLOY_SECOND_NODE.md)
6. ✅ Connectez d'autres nœuds (peers)

Pour plus de détails, consultez le [README.md](README.md) complet.

---

**Besoin d'aide ?** Consultez la section "Dépannage" du README.md ou ouvrez une issue sur GitHub.

