# 🏛️ Guide Complet : Configuration du Trésor Blockchain

Ce guide vous explique comment créer et configurer votre adresse trésor pour avoir un contrôle total sur les tokens de votre blockchain.

## 📋 Qu'est-ce qu'une adresse trésor ?

L'adresse trésor est une adresse spéciale qui vous donne :
- ✅ **Accès illimité** aux tokens (via la fonction `mint_tokens`)
- ✅ **Contrôle total** sur la distribution des tokens
- ✅ **Pouvoir de distribuer** des tokens à n'importe quelle adresse
- ✅ **Statut privilégié** dans la blockchain

**⚠️ Important :** Vous serez le seul à avoir accès à cette adresse grâce à votre clé privée.

---

## 🚀 Étape 1 : Créer votre adresse trésor

### Sur Windows (PowerShell) :

```powershell
cd C:\Users\moi\Desktop\simplequantumresistantblockchain
python create_treasury.py
```

### Sur macOS/Linux :

```bash
cd ~/simplequantumresistantblockchain
python3 create_treasury.py
```

### Ce qui va se passer :

Le script va :
1. ✅ Générer une nouvelle adresse trésor unique
2. ✅ Créer une clé privée sécurisée
3. ✅ Sauvegarder tout dans `treasury_wallet.json`
4. ✅ Afficher vos informations

### Exemple de sortie :

```
======================================================================
🏛️  CRÉATION D'UNE ADRESSE TRÉSOR
======================================================================

Cette adresse vous donnera un contrôle total sur les tokens.
⚠️  IMPORTANT : Gardez votre clé privée SECRÈTE et SÉCURISÉE !

✅ Adresse trésor créée avec succès !

======================================================================
📋 INFORMATIONS DU TRÉSOR
======================================================================

Adresse (TREASURY_ADDRESS) :
  Q7a8f3c9d2e1b4f5a6c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9

Clé publique :
  abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567abc890def123...

⚠️  CLEF PRIVÉE (À GARDER SECRÈTE) :
  def456ghi789jkl012mno345pqr678stu901vwx234yz567abc890def123ghi456...

======================================================================
💾 SAUVEGARDE
======================================================================
Les informations sont sauvegardées dans : treasury_wallet.json

⚠️  SÉCURITÉ :
  1. Ne partagez JAMAIS votre clé privée
  2. Sauvegardez ce fichier dans un endroit sûr (clé USB, cloud chiffré)
  3. Ne commitez JAMAIS ce fichier dans Git
  4. Vous pouvez supprimer le fichier après avoir noté les informations

======================================================================
☁️  CONFIGURATION POUR RENDER
======================================================================

Dans Render, ajoutez cette variable d'environnement :

  Nom de la variable : TREASURY_ADDRESS
  Valeur : Q7a8f3c9d2e1b4f5a6c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9

======================================================================

✅ Votre adresse trésor est prête à être utilisée !
```

---

## 🔐 Étape 2 : Sauvegarder votre clé privée en sécurité

**⚠️ CRITIQUE :** Votre clé privée est la seule preuve que vous êtes le propriétaire du trésor.

### Actions à faire :

1. **Notez votre clé privée** dans un endroit sûr :
   - 📝 Dans un fichier texte chiffré
   - 💾 Sur une clé USB sécurisée
   - 🔒 Dans un gestionnaire de mots de passe (1Password, LastPass, etc.)
   - ☁️ Dans un cloud chiffré (si vous faites confiance)

2. **Ne faites JAMAIS :**
   - ❌ Ne commitez pas `treasury_wallet.json` dans Git
   - ❌ Ne partagez pas votre clé privée
   - ❌ Ne la stockez pas en clair dans le cloud
   - ❌ Ne l'envoyez pas par email

3. **Ajoutez à `.gitignore` :**
   ```
   treasury_wallet.json
   *.json
   !requirements.txt
   ```

---

## ☁️ Étape 3 : Configurer Render avec votre adresse trésor

### Dans l'interface Render :

1. **Allez dans la section "Environment Variables"**

2. **Cliquez sur "Add Environment Variable"**

3. **Ajoutez ces variables :**

   **Variable 1 :**
   - **NAME_OF_VARIABLE** : `TREASURY_ADDRESS`
   - **value** : `Q7a8f3c9d2e1b4f5a6c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9`
     *(Remplacez par VOTRE adresse trésor)*

   **Variable 2 (optionnel) :**
   - **NAME_OF_VARIABLE** : `INACTIVITY_DAYS`
   - **value** : `30`
     *(Nombre de jours avant inactivité, défaut: 30)*

   **Variable 3 (optionnel) :**
   - **NAME_OF_VARIABLE** : `TREASURY_INITIAL_AMOUNT`
   - **value** : `1000000`
     *(Montant initial de tokens pour le trésor, défaut: 1000000)*

4. **Cliquez sur "Deploy web service"**

### Visualisation dans Render :

```
Environment Variables
┌─────────────────────┬──────────────────────────────────────────────┐
│ NAME_OF_VARIABLE    │ value                                        │
├─────────────────────┼──────────────────────────────────────────────┤
│ TREASURY_ADDRESS    │ Q7a8f3c9d2e1b4f5a6c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9 │
│ INACTIVITY_DAYS     │ 30                                           │
└─────────────────────┴──────────────────────────────────────────────┘
```

---

## 🎯 Étape 4 : Initialiser le nœud avec des tokens

Une fois votre nœud déployé sur Render, le trésor sera **automatiquement initialisé** avec 1 million de tokens au premier démarrage si `TREASURY_ADDRESS` est défini.

### Option A : Initialisation automatique (Recommandé) ✅

Le nœud détecte automatiquement si :
- `TREASURY_ADDRESS` est défini dans les variables d'environnement
- Le trésor n'a pas encore de tokens (solde = 0)

Dans ce cas, il initialise automatiquement le trésor avec **1 million de tokens** au démarrage.

**Pour changer le montant initial**, ajoutez une variable d'environnement dans Render :
- **NAME_OF_VARIABLE** : `TREASURY_INITIAL_AMOUNT`
- **value** : `1000000` (ou le montant de votre choix)

### Option B : Initialisation manuelle via l'API

Si vous préférez initialiser manuellement, utilisez l'endpoint `/treasury/init` :

```bash
# Remplacer par votre URL Render
curl -X POST https://blockchain-node.onrender.com/treasury/init \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1000000
  }'
```

**Réponse attendue :**
```json
{
  "success": true,
  "message": "Trésor initialisé avec 1000000 tokens",
  "treasury_address": "Q7a8f3c9d2e1b4f5a6c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9",
  "balance": 1000000.0
}
```

**⚠️ Note :** Cet endpoint ne fonctionne qu'une seule fois. Si le trésor a déjà des tokens, il retournera une erreur.

---

## 💰 Étape 5 : Utiliser votre trésor

Une fois configuré, vous pouvez :

### 1. Vérifier le solde du trésor

```bash
curl https://blockchain-node.onrender.com/wallet/balance/Q7a8f3c9d2e1b4f5a6c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9
```

### 2. Distribuer des tokens

Utilisez le script `distribute_treasury.py` ou l'API `/treasury/distribute` :

```bash
curl -X POST https://blockchain-node.onrender.com/treasury/distribute \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": ["Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6"],
    "amount": 100,
    "private_key": "VOTRE_CLE_PRIVEE_DU_TRESOR"
  }'
```

**⚠️ Attention :** Ne partagez JAMAIS votre clé privée dans les requêtes publiques. Utilisez cette méthode uniquement depuis un environnement sécurisé.

---

## 🔒 Sécurité Avancée

### Pour une sécurité maximale :

1. **Ne stockez JAMAIS la clé privée dans Render**
   - L'adresse trésor (`TREASURY_ADDRESS`) est publique, c'est OK
   - La clé privée doit rester sur votre machine locale uniquement

2. **Utilisez un script local pour les distributions**
   - Gardez `distribute_treasury.py` sur votre machine
   - Utilisez-le pour distribuer des tokens via l'API

3. **Activez l'authentification** (optionnel, nécessite modification du code)
   - Ajoutez une authentification API pour protéger les endpoints sensibles

---

## 📝 Résumé des étapes

1. ✅ Exécutez `python create_treasury.py` localement
2. ✅ Notez votre adresse trésor et votre clé privée
3. ✅ Sauvegardez la clé privée en sécurité
4. ✅ Ajoutez `TREASURY_ADDRESS` dans Render (variable d'environnement)
5. ✅ Déployez votre nœud sur Render
6. ✅ Initialisez le trésor avec des tokens
7. ✅ Utilisez votre trésor pour distribuer des tokens

---

## 🆘 Dépannage

### "Je n'ai pas accès au trésor"

- Vérifiez que `TREASURY_ADDRESS` est bien définie dans Render
- Vérifiez que l'adresse correspond à celle dans `treasury_wallet.json`
- Redéployez le service si nécessaire

### "Le trésor n'a pas de tokens"

- Le trésor doit être initialisé avec des tokens
- Utilisez la fonction `mint_tokens` ou l'endpoint d'initialisation
- Vérifiez le solde avec `/wallet/balance/<treasury_address>`

### "J'ai perdu ma clé privée"

- ⚠️ **CRITIQUE** : Sans la clé privée, vous ne pouvez plus contrôler le trésor
- Créez une nouvelle adresse trésor si nécessaire
- Sauvegardez toujours votre clé privée en plusieurs endroits

---

**Besoin d'aide ?** Consultez le README.md ou ouvrez une issue sur GitHub.

