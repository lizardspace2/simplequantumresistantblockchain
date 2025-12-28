# Blockchain Quantum-Résistante PoS - Guide Complet

Une blockchain simple avec Proof-of-Stake et adresses quantum-résistantes, incluant un mécanisme d'inactivité pour encourager la participation au réseau.

## 📋 Table des matières

1. [Caractéristiques](#-caractéristiques)
2. [Installation complète de Python](#-installation-complète-de-python)
3. [Mettre à jour Python](#-mettre-à-jour-python)
4. [Installation du projet](#-installation-du-projet)
5. [Premier démarrage - Guide pas à pas](#-premier-démarrage---guide-pas-à-pas)
6. [Guide d'utilisation détaillé](#-guide-dutilisation-détaillé)
7. [API REST - Documentation complète](#-api-rest---documentation-complète)
8. [Mécanisme d'inactivité expliqué](#-mécanisme-dinactivité-expliqué)
9. [Distribution depuis le trésor](#-distribution-depuis-le-trésor)
10. [Créer un réseau multi-nœuds](#-créer-un-réseau-multi-nœuds)
11. [Déployer dans le Cloud (Gratuit)](#️-déployer-dans-le-cloud-gratuit)
12. [Dépannage détaillé](#-dépannage-détaillé)
13. [Sécurité](#-sécurité)

---

## 🚀 Caractéristiques

- ✅ **Adresses quantum-résistantes** : Utilise SHA3-256 et SHA3-512 (résistants aux attaques quantiques)
- ✅ **Proof-of-Stake** : Validation par stake au lieu de mining
- ✅ **Mécanisme d'inactivité** : Suivi de l'activité des wallets
- ✅ **API REST complète** : Contrôle total via API HTTP
- ✅ **CLI user-friendly** : Interface en ligne de commande avec couleurs
- ✅ **Multi-nœuds P2P** : Support pour réseau distribué

---

## 🐍 Installation complète de Python

### Windows

#### Étape 1 : Télécharger Python

1. Allez sur le site officiel : https://www.python.org/downloads/
2. Cliquez sur le bouton **"Download Python 3.x.x"** (la dernière version)
3. Le fichier d'installation se télécharge (ex: `python-3.11.5-amd64.exe`)

#### Étape 2 : Installer Python

1. **Double-cliquez** sur le fichier téléchargé
2. **IMPORTANT** : Cochez la case **"Add Python to PATH"** en bas de la fenêtre
   - Cette étape est cruciale pour pouvoir utiliser Python depuis n'importe où
3. Cliquez sur **"Install Now"**
4. Attendez la fin de l'installation
5. Cliquez sur **"Close"**

#### Étape 3 : Vérifier l'installation

1. Ouvrez **PowerShell** ou **Invite de commandes** (cmd)
   - Appuyez sur `Windows + R`, tapez `powershell` et appuyez sur Entrée
2. Tapez la commande suivante :
   ```powershell
   python --version
   ```
3. Vous devriez voir quelque chose comme : `Python 3.11.5`
4. Vérifiez aussi pip :
   ```powershell
   pip --version
   ```
5. Vous devriez voir : `pip 23.x.x from ...`

**Si Python n'est pas reconnu :**
- Réinstallez Python en cochant "Add Python to PATH"
- Ou ajoutez manuellement Python au PATH système

### macOS

#### Étape 1 : Vérifier si Python est déjà installé

1. Ouvrez **Terminal** (Applications > Utilitaires > Terminal)
2. Tapez :
   ```bash
   python3 --version
   ```
3. Si vous voyez une version (ex: `Python 3.11.5`), passez à l'étape 2
4. Si vous voyez "command not found", installez Python

#### Étape 2 : Installer Python (si nécessaire)

**Option A : Via Homebrew (recommandé)**
```bash
# Installer Homebrew si vous ne l'avez pas
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installer Python
brew install python3
```

**Option B : Via le site officiel**
1. Allez sur https://www.python.org/downloads/macos/
2. Téléchargez le fichier `.pkg`
3. Double-cliquez et suivez l'installation

#### Étape 3 : Vérifier l'installation

```bash
python3 --version
pip3 --version
```

### Linux (Ubuntu/Debian)

#### Étape 1 : Mettre à jour les paquets

```bash
sudo apt update
sudo apt upgrade -y
```

#### Étape 2 : Installer Python et pip

```bash
sudo apt install python3 python3-pip -y
```

#### Étape 3 : Vérifier l'installation

```bash
python3 --version
pip3 --version
```

**Note pour Linux/macOS :** Utilisez `python3` et `pip3` au lieu de `python` et `pip`

---

## 🔄 Mettre à jour Python

### Vérifier votre version actuelle

Avant de mettre à jour, vérifiez quelle version vous avez :

**Windows :**
```powershell
python --version
```

**macOS/Linux :**
```bash
python3 --version
```

### Windows

#### Méthode 1 : Installation par-dessus (Recommandé)

1. **Téléchargez la nouvelle version** depuis https://www.python.org/downloads/
2. **Lancez l'installateur** de la nouvelle version
3. **IMPORTANT** : Cochez **"Add Python to PATH"**
4. **IMPORTANT** : Cliquez sur **"Install Now"** (pas "Upgrade Now")
   - L'ancienne version sera remplacée automatiquement
5. Attendez la fin de l'installation
6. **Redémarrez votre terminal** (fermez et rouvrez PowerShell)
7. **Vérifiez la nouvelle version** :
   ```powershell
   python --version
   ```

#### Méthode 2 : Désinstaller puis réinstaller

1. **Désinstaller l'ancienne version** :
   - Ouvrez "Paramètres" > "Applications"
   - Cherchez "Python" dans la liste
   - Cliquez sur "Désinstaller"
2. **Installer la nouvelle version** (suivez les étapes de la section Installation)
3. **Vérifier** :
   ```powershell
   python --version
   ```

#### Mettre à jour pip après la mise à jour de Python

**Windows :**
```powershell
python -m pip install --upgrade pip
```

**Vérifier :**
```powershell
pip --version
```

### macOS

#### Méthode 1 : Via Homebrew (Recommandé)

**Si vous avez installé Python via Homebrew :**

```bash
# Mettre à jour Homebrew
brew update

# Mettre à jour Python
brew upgrade python3

# Vérifier la nouvelle version
python3 --version
```

**Si vous avez installé Python depuis le site officiel :**

1. **Téléchargez la nouvelle version** depuis https://www.python.org/downloads/macos/
2. **Lancez le fichier `.pkg`**
3. **Suivez l'installation** (l'ancienne version sera remplacée)
4. **Vérifiez** :
   ```bash
   python3 --version
   ```

#### Méthode 2 : Installer une nouvelle version côte à côte

Si vous voulez garder plusieurs versions de Python :

```bash
# Installer une version spécifique
brew install python@3.11

# Ou installer la dernière version
brew install python@3.12

# Utiliser une version spécifique
python3.11 --version
python3.12 --version
```

#### Mettre à jour pip

**macOS :**
```bash
python3 -m pip install --upgrade pip
```

**Vérifier :**
```bash
pip3 --version
```

### Linux (Ubuntu/Debian)

#### Méthode 1 : Via le gestionnaire de paquets (Recommandé)

**Pour Ubuntu/Debian :**

```bash
# Mettre à jour la liste des paquets
sudo apt update

# Mettre à jour Python
sudo apt upgrade python3 python3-pip

# Vérifier la version
python3 --version
```

**Si une version plus récente est disponible dans les dépôts :**

```bash
# Ajouter le dépôt deadsnakes (pour Ubuntu)
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Installer une version spécifique (ex: Python 3.12)
sudo apt install python3.12 python3.12-pip

# Utiliser cette version
python3.12 --version
```

#### Méthode 2 : Compiler depuis les sources (Avancé)

Si vous avez besoin de la toute dernière version :

```bash
# Installer les dépendances de compilation
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev

# Télécharger Python (remplacez 3.12.0 par la version souhaitée)
cd /tmp
wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz

# Extraire
tar -xf Python-3.12.0.tgz
cd Python-3.12.0

# Configurer et compiler
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall

# Vérifier
python3.12 --version
```

#### Mettre à jour pip

**Linux :**
```bash
python3 -m pip install --upgrade pip
```

**Vérifier :**
```bash
pip3 --version
```

### Vérifier que tout fonctionne après la mise à jour

Après avoir mis à jour Python, vérifiez que tout fonctionne :

1. **Vérifier Python :**
   ```bash
   # Windows
   python --version
   
   # macOS/Linux
   python3 --version
   ```

2. **Vérifier pip :**
   ```bash
   # Windows
   pip --version
   
   # macOS/Linux
   pip3 --version
   ```

3. **Réinstaller les dépendances du projet** (recommandé) :
   ```bash
   # Windows
   pip install -r requirements.txt --upgrade
   
   # macOS/Linux
   pip3 install -r requirements.txt --upgrade
   ```

4. **Tester le projet :**
   ```bash
   # Windows
   python blockchain_node.py --help
   
   # macOS/Linux
   python3 blockchain_node.py --help
   ```

### Problèmes courants après mise à jour

#### Problème 1 : "python n'est pas reconnu" après mise à jour

**Solution Windows :**
1. Redémarrez votre terminal (fermez et rouvrez)
2. Vérifiez le PATH :
   ```powershell
   $env:PATH
   ```
3. Si Python n'est pas dans le PATH, réinstallez en cochant "Add Python to PATH"

**Solution macOS/Linux :**
```bash
# Vérifier où Python est installé
which python3

# Si nécessaire, ajouter au PATH dans ~/.bashrc ou ~/.zshrc
export PATH="/usr/local/bin:$PATH"
```

#### Problème 2 : Les modules ne sont plus trouvés

**Solution :** Réinstallez les dépendances :
```bash
# Windows
pip install -r requirements.txt

# macOS/Linux
pip3 install -r requirements.txt
```

#### Problème 3 : Conflit entre plusieurs versions

**Windows :**
```powershell
# Voir toutes les versions installées
py -0

# Utiliser une version spécifique
py -3.11 blockchain_node.py
```

**macOS/Linux :**
```bash
# Utiliser une version spécifique
python3.11 blockchain_node.py
python3.12 blockchain_node.py
```

### Quand mettre à jour Python ?

- ✅ **Mise à jour de sécurité** : Toujours mettre à jour immédiatement
- ✅ **Nouvelle fonctionnalité** : Si vous en avez besoin pour votre projet
- ✅ **Version obsolète** : Si votre version n'est plus supportée
- ⚠️ **Stabilité** : Si votre projet fonctionne bien, pas besoin de mettre à jour immédiatement

**Vérifier si votre version est toujours supportée :**
- https://www.python.org/downloads/
- Les versions marquées "End of Life" ne reçoivent plus de mises à jour de sécurité

---

## 📦 Installation du projet

### Étape 1 : Télécharger ou cloner le projet

**Option A : Si vous avez déjà les fichiers**
- Assurez-vous que tous les fichiers sont dans le même dossier

**Option B : Si vous clonez depuis Git**
```bash
git clone <url-du-repo>
cd simplequantumresistantblockchain
```

### Étape 2 : Ouvrir un terminal dans le dossier du projet

**Windows :**
1. Ouvrez l'Explorateur de fichiers
2. Naviguez vers le dossier du projet
3. Dans la barre d'adresse, tapez `powershell` et appuyez sur Entrée
   - Ou faites clic droit > "Ouvrir PowerShell ici"

**macOS/Linux :**
```bash
cd /chemin/vers/simplequantumresistantblockchain
```

### Étape 3 : Installer les dépendances

**Windows :**
```powershell
pip install -r requirements.txt
```

**macOS/Linux :**
```bash
pip3 install -r requirements.txt
```

**Sortie attendue :**
```
Collecting flask>=2.3.0
  Downloading flask-2.3.0-py3-none-any.whl
Collecting requests>=2.31.0
  Downloading requests-2.31.0-py3-none-any.whl
...
Successfully installed flask-2.3.0 requests-2.31.0
```

### Étape 4 : Vérifier que tout est installé

**Windows :**
```powershell
python blockchain_node.py --help
```

**macOS/Linux :**
```bash
python3 blockchain_node.py --help
```

Vous devriez voir l'aide du programme s'afficher.

---

## 🎯 Premier démarrage - Guide pas à pas

### Scénario complet : De zéro à première transaction

#### Étape 1 : Lancer le nœud blockchain

**Ouvrez un premier terminal :**

**Windows :**
```powershell
cd C:\Users\moi\Desktop\simplequantumresistantblockchain
python blockchain_node.py --port 5000 --init
```

**macOS/Linux :**
```bash
cd ~/simplequantumresistantblockchain
python3 blockchain_node.py --port 5000 --init
```

**Ce qui se passe :**
- Le nœud démarre sur le port 5000
- Un wallet trésor est créé automatiquement
- Deux wallets de test (Alice et Bob) sont créés
- Des tokens sont distribués
- Des validateurs sont enregistrés
- Les fichiers sont sauvegardés

**Sortie attendue :**
```
🏛️  Trésor créé automatiquement
Adresse: Q7a8f3c9d2e1b4f5a6c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9
Clé privée sauvegardée dans: treasury_node_5000.json

Initialisation avec données de test...

Alice: Q8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8
  Private key: abc123def456...

Bob: Q9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9
  Private key: def456ghi789...

Wallets sauvegardés dans wallets_node_5000.json

======================================================================
NOEUD BLOCKCHAIN AVEC MECANISME D'INACTIVITE
======================================================================
Port: 5000
URL: http://localhost:5000
Trésor: Q7a8f3c9d2e1b4f5a6c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9
======================================================================

 * Running on http://0.0.0.0:5000
```

**⚠️ IMPORTANT :** Laissez ce terminal ouvert ! Le nœud doit rester en cours d'exécution.

#### Étape 2 : Ouvrir un deuxième terminal

**Windows :**
- Appuyez sur `Windows + R`
- Tapez `powershell` et appuyez sur Entrée
- Naviguez vers le dossier :
  ```powershell
  cd C:\Users\moi\Desktop\simplequantumresistantblockchain
  ```

**macOS/Linux :**
- Ouvrez un nouveau terminal
- Naviguez vers le dossier :
  ```bash
  cd ~/simplequantumresistantblockchain
  ```

#### Étape 3 : Vérifier que le nœud fonctionne

**Windows :**
```powershell
python wallet_manager.py status
```

**macOS/Linux :**
```bash
python3 wallet_manager.py status
```

**Sortie attendue :**
```
📊 STATUT DE LA BLOCKCHAIN
============================================================
Blocs: 1
Transactions en attente: 0
Validateurs actifs: 2
Récompense par bloc: 10 tokens
Stake minimum: 100 tokens
Blockchain valide: True

Trésor:
  Adresse: Q7a8f3c9d2e1b4f5a6c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9
  Balance: 10000 tokens
============================================================

Validateurs:
  1. Q8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8
  2. Q9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9
```

✅ Si vous voyez cela, le nœud fonctionne correctement !

#### Étape 4 : Créer votre premier wallet

**Dans le même terminal (le deuxième) :**

**Windows :**
```powershell
python wallet_manager.py create
```

**macOS/Linux :**
```bash
python3 wallet_manager.py create
```

**Sortie attendue :**
```
🎉 Nouveau wallet créé !

Adresse:
  Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6

Clé publique:
  abc123def456ghi789jkl012mno345pqr678stu901vwx234yz...

⚠️  CLEF PRIVEE (À GARDER SECRETE) :
  def456ghi789jkl012mno345pqr678stu901vwx234yz567abc890def123ghi456jkl789...

Sauvegardé dans: wallet_Q1a2b3c4d5.json

⚠ Ne partagez JAMAIS votre clé privée !
```

**📝 Notez votre adresse et votre clé privée !** Vous en aurez besoin.

#### Étape 5 : Vérifier le solde de votre wallet

**Copiez l'adresse de votre wallet** (celle qui commence par `Q`) et exécutez :

**Windows :**
```powershell
python wallet_manager.py balance Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6
```

**macOS/Linux :**
```bash
python3 wallet_manager.py balance Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6
```

**Sortie attendue :**
```
💰 Solde du wallet
============================================================
Adresse: Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6
Disponible: 0 tokens
Staké: 0 tokens
Total: 0 tokens

Statut d'activité:
  Dernière activité: 2024-01-15 14:30:00
  Inactif depuis: 0.0 jours
============================================================
```

Votre wallet est vide pour l'instant, c'est normal !

#### Étape 6 : Recevoir des tokens depuis le trésor

Pour recevoir des tokens, vous devez utiliser le script de distribution. Mais d'abord, créons un fichier avec votre adresse.

**Créer le fichier `recipients.json` :**

**Windows (PowerShell) :**
```powershell
@"
{
  "addresses": [
    "Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6"
  ]
}
"@ | Out-File -Encoding utf8 recipients.json
```

**macOS/Linux :**
```bash
cat > recipients.json << EOF
{
  "addresses": [
    "Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6"
  ]
}
EOF
```

**Ou créez-le manuellement :**
1. Créez un fichier nommé `recipients.json`
2. Collez ce contenu (remplacez par votre adresse) :
```json
{
  "addresses": [
    "Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6"
  ]
}
```

**Distribuer 100 tokens depuis le trésor :**

**Windows :**
```powershell
python distribute_treasury.py treasury_node_5000.json recipients.json 100
```

**macOS/Linux :**
```bash
python3 distribute_treasury.py treasury_node_5000.json recipients.json 100
```

**Sortie attendue :**
```
💰 Distribution depuis le trésor
============================================================
Trésor: Q7a8f3c9d2e1b4f5a6c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9
Bénéficiaires: 1
Montant par bénéficiaire: 100 tokens
Total à distribuer: 100 tokens
============================================================

Confirmer la distribution ? (o/n): o

✅ 1 distributions créées avec succès !

Les transactions sont maintenant dans la pool.
Créez un bloc pour les valider : python wallet_manager.py mine
```

#### Étape 7 : Créer un bloc pour valider la transaction

**Windows :**
```powershell
python wallet_manager.py mine
```

**macOS/Linux :**
```bash
python3 wallet_manager.py mine
```

**Sortie attendue :**
```
⛏️  Création d'un nouveau bloc...

✓ Bloc #1 créé avec succès !

Validateur: Q8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8
Hash: abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567abc890def123...
Transactions: 1
Timestamp: 2024-01-15 14:35:00
```

#### Étape 8 : Vérifier que vous avez reçu les tokens

**Windows :**
```powershell
python wallet_manager.py balance Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6
```

**macOS/Linux :**
```bash
python3 wallet_manager.py balance Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6
```

**Sortie attendue :**
```
💰 Solde du wallet
============================================================
Adresse: Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6
Disponible: 100 tokens
Staké: 0 tokens
Total: 100 tokens
============================================================
```

🎉 **Félicitations ! Vous avez reçu vos premiers tokens !**

#### Étape 9 : Envoyer des tokens à quelqu'un

Pour envoyer des tokens, vous avez besoin :
1. Du fichier wallet (ex: `wallet_Q1a2b3c4d5.json`)
2. De l'adresse du destinataire (ex: l'adresse d'Alice dans `wallets_node_5000.json`)

**Lister les wallets disponibles :**

**Windows :**
```powershell
python wallet_manager.py list
```

**macOS/Linux :**
```bash
python3 wallet_manager.py list
```

**Sortie attendue :**
```
👛 Wallets locaux
============================================================

1. wallet_Q1a2b3c4d5.json
   Adresse: Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6
   Balance: 100 tokens

2. wallets_node_5000.json (Plusieurs wallets)
   alice: Q8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8
   Balance: 1000 tokens
   bob: Q9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9
   Balance: 500 tokens
```

**Envoyer 50 tokens à Alice :**

**Windows :**
```powershell
python wallet_manager.py send wallet_Q1a2b3c4d5.json Q8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8 50
```

**macOS/Linux :**
```bash
python3 wallet_manager.py send wallet_Q1a2b3c4d5.json Q8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8 50
```

**Sortie attendue :**
```
📤 Envoi de tokens
============================================================
De: Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6
Vers: Q8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8
Montant: 50 tokens
Frais: 1 tokens
Total: 51 tokens
============================================================

Confirmer la transaction ? (o/n): o

✓ Transaction envoyée avec succès !
ℹ La transaction est maintenant dans la pool en attente
ℹ Elle sera incluse dans le prochain bloc validé
```

**Créer un bloc pour valider la transaction :**

**Windows :**
```powershell
python wallet_manager.py mine
```

**macOS/Linux :**
```bash
python3 wallet_manager.py mine
```

**Vérifier votre nouveau solde :**

**Windows :**
```powershell
python wallet_manager.py balance Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6
```

**macOS/Linux :**
```bash
python3 wallet_manager.py balance Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6
```

Vous devriez maintenant avoir **49 tokens** (100 - 50 - 1 de frais).

---

## 📖 Guide d'utilisation détaillé

### Commandes du Wallet Manager

#### 1. Créer un wallet

**Commande :**
```bash
python wallet_manager.py create
# ou
python3 wallet_manager.py create
```

**Ce qui se passe :**
- Un nouveau wallet est créé avec une adresse quantum-résistante
- Une clé privée et une clé publique sont générées
- Le wallet est sauvegardé dans un fichier JSON
- L'adresse est enregistrée comme "active"

**Fichier créé :** `wallet_Q[40caractères].json`

**Contenu du fichier :**
```json
{
  "address": "Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6",
  "public_key": "abc123...",
  "private_key": "def456..."
}
```

**⚠️ IMPORTANT :** Gardez votre clé privée secrète ! Ne la partagez jamais !

#### 2. Vérifier le solde

**Commande :**
```bash
python wallet_manager.py balance <adresse>
```

**Exemple :**
```bash
python wallet_manager.py balance Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6
```

**Informations affichées :**
- Solde disponible (tokens non stakés)
- Solde staké (tokens utilisés pour valider)
- Total (disponible + staké)
- Dernière activité
- Temps d'inactivité

#### 3. Envoyer des tokens

**Commande :**
```bash
python wallet_manager.py send <fichier_wallet> <adresse_destinataire> <montant> [frais]
```

**Exemple :**
```bash
python wallet_manager.py send wallet_Q1a2b3c4d5.json Q8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8 50
```

**Avec frais personnalisés :**
```bash
python wallet_manager.py send wallet_Q1a2b3c4d5.json Q8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8 50 2
```

**Ce qui se passe :**
1. Le wallet est chargé depuis le fichier
2. La transaction est préparée
3. Vous devez confirmer
4. La transaction est signée avec votre clé privée
5. La transaction est envoyée au nœud
6. La transaction est ajoutée à la pool en attente
7. Vous devez créer un bloc pour la valider

**Conditions :**
- Vous devez avoir suffisamment de tokens (montant + frais)
- Le wallet doit être valide
- Le nœud doit être en ligne

#### 4. Devenir validateur

**Commande :**
```bash
python wallet_manager.py validator <fichier_wallet> <stake>
```

**Exemple :**
```bash
python wallet_manager.py validator wallet_Q1a2b3c4d5.json 200
```

**Ce qui se passe :**
- Les tokens sont "lockés" (retirés du solde disponible)
- Vous êtes enregistré comme validateur
- Vous pouvez maintenant être sélectionné pour créer des blocs
- Plus votre stake est élevé, plus vous avez de chances d'être sélectionné

**Conditions :**
- Stake minimum : 100 tokens (par défaut)
- Vous devez avoir suffisamment de tokens disponibles

**Avantages :**
- Vous recevez les récompenses de blocs (10 tokens + frais de transaction)
- Vous ne perdez jamais de coins par inactivité
- Vous participez activement au réseau

#### 5. Créer un bloc (Validation)

**Commande :**
```bash
python wallet_manager.py mine
```

**Ce qui se passe :**
1. Un validateur est sélectionné aléatoirement (pondéré par stake)
2. Toutes les transactions en attente sont validées
3. Un nouveau bloc est créé
4. Les transactions sont exécutées (transferts de tokens)
5. Le validateur reçoit la récompense (10 tokens + frais)

**Conditions :**
- Il doit y avoir au moins une transaction en attente
- Il doit y avoir au moins un validateur enregistré

### 📊 Répartition des récompenses (Proof-of-Stake)

#### Comment fonctionne la sélection des validateurs

La blockchain utilise un système **Proof-of-Stake (PoS)** où les validateurs sont sélectionnés de manière aléatoire, mais **pondérée par leur stake**.

**Mécanisme de sélection :**
1. Un nombre aléatoire est généré entre 0 et le stake total
2. Les validateurs sont parcourus dans l'ordre
3. Le premier validateur dont le stake cumulé dépasse la valeur aléatoire est sélectionné
4. **Plus votre stake est élevé, plus vous avez de chances d'être sélectionné**

**Exemple de probabilités :**
- **Validateur A** : 200 tokens de stake (20% du total) → 20% de chances
- **Validateur B** : 300 tokens de stake (30% du total) → 30% de chances
- **Validateur C** : 500 tokens de stake (50% du total) → 50% de chances

#### Montant des récompenses

**Composition de la récompense :**
- **Récompense fixe** : 10 tokens par bloc
- **Frais de transaction** : Tous les frais collectés dans la pool de transactions en attente
- **Total** = 10 tokens + frais de transaction

**Exemple :**
- Si 5 transactions avec 1 token de frais chacune sont dans la pool
- Récompense totale = 10 + 5 = **15 tokens**

#### Répartition des récompenses

⚠️ **Important : Système "Winner-Takes-All"**

- **Un seul validateur** reçoit la récompense totale à chaque bloc
- **Pas de partage** entre tous les validateurs
- Le validateur sélectionné reçoit **100% de la récompense** (10 tokens + tous les frais)
- Les autres validateurs reçoivent **0 token**

**Exemple concret :**

Supposons 3 validateurs :
- Validateur A : stake 200 tokens (20% de chances)
- Validateur B : stake 300 tokens (30% de chances)
- Validateur C : stake 500 tokens (50% de chances)
- Frais collectés : 5 tokens

**Scénario 1 : Validateur C est sélectionné**
- ✅ Validateur C reçoit : **15 tokens** (10 + 5)
- ❌ Validateur A reçoit : **0 token**
- ❌ Validateur B reçoit : **0 token**

**Scénario 2 : Validateur A est sélectionné**
- ✅ Validateur A reçoit : **15 tokens** (10 + 5)
- ❌ Validateur B reçoit : **0 token**
- ❌ Validateur C reçoit : **0 token**

#### Stratégie pour maximiser vos récompenses

1. **Augmenter votre stake** : Plus vous stakez, plus vos chances augmentent
2. **Être actif** : Plus vous créez de blocs, plus vous avez de chances d'être sélectionné
3. **Comprendre les probabilités** : Avec 10% du stake total, vous gagnerez environ 10% des blocs sur le long terme

**Calcul de probabilité :**
```
Probabilité = (Votre stake / Stake total) × 100%
```

**Exemple :**
- Stake total du réseau : 1000 tokens
- Votre stake : 250 tokens
- Votre probabilité : (250 / 1000) × 100% = **25% de chances par bloc**

#### 6. Voir le statut de la blockchain

**Commande :**
```bash
python wallet_manager.py status
```

**Informations affichées :**
- Nombre de blocs
- Transactions en attente
- Nombre de validateurs
- Récompense par bloc
- Stake minimum
- État de validité de la blockchain
- Informations sur le trésor (si configuré)

#### 7. Lister les wallets locaux

**Commande :**
```bash
python wallet_manager.py list
```

**Ce qui se passe :**
- Tous les fichiers `wallet_*.json`, `wallets_*.json` et `treasury_*.json` sont listés
- Pour chaque wallet, l'adresse et le solde sont affichés

#### 8. Explorer la blockchain

**Commande :**
```bash
python wallet_manager.py explorer
```

**Ce qui se passe :**
- Les 5 derniers blocs sont affichés
- Pour chaque bloc : index, hash, validateur, timestamp, transactions

---

## 🌐 API REST - Documentation complète

### Base URL

Par défaut : `http://localhost:5000`

### Endpoints

#### 1. Santé du nœud

**GET** `/health`

**Description :** Vérifie si le nœud est en ligne

**Exemple avec curl (Windows PowerShell) :**
```powershell
curl http://localhost:5000/health
```

**Exemple avec curl (macOS/Linux) :**
```bash
curl http://localhost:5000/health
```

**Réponse :**
```json
{
  "status": "online",
  "port": 5000
}
```

#### 2. Créer un wallet

**POST** `/wallet/create`

**Description :** Crée un nouveau wallet

**Exemple avec curl :**
```bash
curl -X POST http://localhost:5000/wallet/create
```

**Réponse :**
```json
{
  "success": true,
  "wallet": {
    "address": "Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6",
    "public_key": "abc123...",
    "private_key": "def456..."
  },
  "message": "Wallet créé avec succès. GARDEZ VOTRE CLEF PRIVEE EN SECURITE!"
}
```

#### 3. Obtenir le solde

**GET** `/wallet/balance/<adresse>`

**Description :** Obtient le solde et les informations d'un compte

**Exemple :**
```bash
curl http://localhost:5000/wallet/balance/Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6
```

**Réponse :**
```json
{
  "address": "Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6",
  "balance": 100,
  "staked": 0,
  "total": 100,
  "is_validator": false,
  "last_activity": 1705329000,
  "inactive_time": 0,
  "inactive_days": 0
}
```

#### 4. Envoyer une transaction

**POST** `/transaction/send`

**Description :** Envoie une transaction

**Body (JSON) :**
```json
{
  "sender": "Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6",
  "recipient": "Q8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8",
  "amount": 50,
  "fee": 1,
  "private_key": "votre_cle_privee_ici"
}
```

**Exemple avec curl :**
```bash
curl -X POST http://localhost:5000/transaction/send \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6",
    "recipient": "Q8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8",
    "amount": 50,
    "fee": 1,
    "private_key": "def456..."
  }'
```

**Réponse :**
```json
{
  "success": true,
  "transaction": {
    "sender": "Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6",
    "recipient": "Q8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8",
    "amount": 50,
    "fee": 1,
    "nonce": 0,
    "timestamp": 1705329000,
    "signature": "abc123...",
    "tx_type": "TRANSFER"
  },
  "message": "Transaction ajoutée à la pool"
}
```

#### 5. S'enregistrer comme validateur

**POST** `/validator/register`

**Description :** S'enregistre comme validateur

**Body (JSON) :**
```json
{
  "address": "Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6",
  "stake": 200
}
```

**Exemple avec curl :**
```bash
curl -X POST http://localhost:5000/validator/register \
  -H "Content-Type: application/json" \
  -d '{
    "address": "Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6",
    "stake": 200
  }'
```

**Réponse :**
```json
{
  "success": true,
  "message": "Validateur enregistré avec stake de 200"
}
```

#### 6. Créer un bloc

**POST** `/block/mine`

**Description :** Crée un nouveau bloc

**Exemple avec curl :**
```bash
curl -X POST http://localhost:5000/block/mine
```

**Réponse :**
```json
{
  "success": true,
  "block": {
    "index": 1,
    "timestamp": 1705329000,
    "hash": "abc123...",
    "previous_hash": "0",
    "validator": "Q8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8",
    "stake": 300,
    "transactions": [...]
  },
  "message": "Bloc #1 créé"
}
```

#### 7. Obtenir la blockchain

**GET** `/blockchain`

**Description :** Obtient toute la blockchain

**Exemple avec curl :**
```bash
curl http://localhost:5000/blockchain
```

#### 8. Statut de la blockchain

**GET** `/blockchain/status`

**Description :** Obtient le statut de la blockchain

**Exemple avec curl :**
```bash
curl http://localhost:5000/blockchain/status
```

#### 9. Distribuer depuis le trésor

**POST** `/treasury/distribute`

**Description :** Distribue des coins depuis le trésor

**Body (JSON) :**
```json
{
  "recipients": [
    "Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6",
    "Q8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8"
  ],
  "amount": 100,
  "private_key": "cle_privee_du_tresor"
}
```

---

## 🔒 Mécanisme d'inactivité expliqué

### Comment ça marche

1. **Suivi d'activité** : Chaque transaction ou validation met à jour la dernière activité
2. **Temps d'inactivité** : Le système suit le temps depuis la dernière activité de chaque wallet

### Configurer le mécanisme

**Lancer le nœud avec paramètres personnalisés :**

```bash
python blockchain_node.py --port 5000 \
  --inactivity-days 30
```

**Paramètres :**
- `--inactivity-days` : Seuil d'inactivité en jours (défaut: 30)

---

## 💰 Distribution depuis le trésor

### Méthode 1 : Via le script Python

#### Étape 1 : Créer le fichier des bénéficiaires

**Windows (PowerShell) :**
```powershell
@"
{
  "addresses": [
    "Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6",
    "Q8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8"
  ]
}
"@ | Out-File -Encoding utf8 recipients.json
```

**macOS/Linux :**
```bash
cat > recipients.json << EOF
{
  "addresses": [
    "Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6",
    "Q8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8"
  ]
}
EOF
```

#### Étape 2 : Distribuer

**Windows :**
```powershell
python distribute_treasury.py treasury_node_5000.json recipients.json 100
```

**macOS/Linux :**
```bash
python3 distribute_treasury.py treasury_node_5000.json recipients.json 100
```

### Méthode 2 : Via l'API REST

**Avec curl :**
```bash
curl -X POST http://localhost:5000/treasury/distribute \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": [
      "Q1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6"
    ],
    "amount": 100,
    "private_key": "cle_privee_du_tresor"
  }'
```

---

## 🌍 Créer un réseau multi-nœuds

### 📘 Guide de déploiement d'un deuxième nœud

**Pour déployer un deuxième nœud sur Render ou une autre plateforme cloud, consultez le guide détaillé :**
👉 **[DEPLOY_SECOND_NODE.md](DEPLOY_SECOND_NODE.md)**

Ce guide vous explique comment :
- Déployer un deuxième nœud sur Render, Railway, ou Fly.io
- Connecter les nœuds ensemble
- Synchroniser la blockchain entre les nœuds
- Tester votre réseau multi-nœuds

**Script automatique de connexion :**
```bash
python connect_nodes.py <url_node1> <url_node2>
```

### Scénario : 3 nœuds connectés (local)

#### Étape 1 : Lancer le nœud principal

**Terminal 1 :**
```bash
python blockchain_node.py --port 5000 --init
```

#### Étape 2 : Lancer le deuxième nœud

**Terminal 2 :**
```bash
python blockchain_node.py --port 5001
```

#### Étape 3 : Lancer le troisième nœud

**Terminal 3 :**
```bash
python blockchain_node.py --port 5002
```

#### Étape 4 : Connecter les nœuds

**Option A : Utiliser le script automatique**
```bash
python connect_nodes.py http://localhost:5000 http://localhost:5001
python connect_nodes.py http://localhost:5000 http://localhost:5002
```

**Option B : Connecter manuellement**

**Connecter le nœud 2 au nœud 1 :**

**Windows (PowerShell) :**
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/peers/add" -Method POST -ContentType "application/json" -Body '{"peer": "http://localhost:5000"}'
```

**macOS/Linux :**
```bash
curl -X POST http://localhost:5001/peers/add \
  -H "Content-Type: application/json" \
  -d '{"peer": "http://localhost:5000"}'
```

**Connecter le nœud 3 au nœud 1 :**
```bash
curl -X POST http://localhost:5002/peers/add \
  -H "Content-Type: application/json" \
  -d '{"peer": "http://localhost:5000"}'
```

**Vérifier les connexions :**
```bash
curl http://localhost:5001/peers
curl http://localhost:5002/peers
```

---

## 🐛 Dépannage détaillé

### Problème 1 : "python n'est pas reconnu"

**Symptômes :**
```
'python' n'est pas reconnu en tant que commande interne ou externe
```

**Solutions :**

**Windows :**
1. Réinstallez Python en cochant "Add Python to PATH"
2. Ou utilisez `py` au lieu de `python` :
   ```powershell
   py blockchain_node.py --port 5000
   ```
3. Ou ajoutez Python au PATH manuellement :
   - Cherchez où Python est installé (ex: `C:\Python311`)
   - Ajoutez `C:\Python311` et `C:\Python311\Scripts` au PATH système

**macOS/Linux :**
- Utilisez `python3` au lieu de `python`

### Problème 2 : Le port est déjà utilisé

**Symptômes :**
```
Address already in use
```

**Solutions :**

**Windows :**
```powershell
# Vérifier quel processus utilise le port
netstat -ano | findstr :5000

# Tuer le processus (remplacez PID par le numéro trouvé)
taskkill /PID <PID> /F

# Ou utiliser un autre port
python blockchain_node.py --port 5555
```

**macOS/Linux :**
```bash
# Vérifier quel processus utilise le port
lsof -i :5000

# Tuer le processus
kill -9 <PID>

# Ou utiliser un autre port
python3 blockchain_node.py --port 5555
```

### Problème 3 : Transaction échoue

**Symptômes :**
```
Transaction échouée: Transaction invalide
```

**Solutions :**
1. Vérifier le solde :
   ```bash
   python wallet_manager.py balance <adresse>
   ```
2. Vérifier que vous avez assez de tokens (montant + frais)
3. Vérifier que le nœud est en ligne :
   ```bash
   curl http://localhost:5000/health
   ```
4. Vérifier que la clé privée correspond à l'adresse

### Problème 4 : Pas de validateurs

**Symptômes :**
```
Erreur: Pas de transactions ou pas de validateurs
```

**Solutions :**
1. Enregistrer au moins un validateur :
   ```bash
   python wallet_manager.py validator wallet_XXX.json 200
   ```
2. Vérifier qu'il y a des validateurs :
   ```bash
   python wallet_manager.py status
   ```

### Problème 5 : Module non trouvé

**Symptômes :**
```
ModuleNotFoundError: No module named 'flask'
```

**Solutions :**
1. Réinstaller les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
2. Vérifier que vous utilisez le bon Python :
   ```bash
   python --version
   which python  # macOS/Linux
   where python  # Windows
   ```

### Problème 6 : Le wallet n'est pas trouvé

**Symptômes :**
```
Fichier wallet introuvable: wallet_XXX.json
```

**Solutions :**
1. Lister les wallets disponibles :
   ```bash
   python wallet_manager.py list
   ```
2. Vérifier que vous êtes dans le bon dossier
3. Vérifier le nom exact du fichier (sensible à la casse)

---

## 🛡️ Sécurité

### ⚠️ Points importants

1. **Clé privée** : Ne JAMAIS la partager ou la publier
2. **Sauvegarde** : Sauvegardez vos wallets dans un endroit sûr (clé USB, cloud chiffré)
3. **Production** : Cette implémentation est éducative, pas prête pour la production
4. **HTTPS** : En production, utiliser HTTPS pour l'API
5. **Firewall** : Configurer un firewall pour limiter l'accès au nœud
6. **Environnement** : Ne pas exposer le nœud sur Internet sans protection

### Bonnes pratiques

- Ne jamais commiter les fichiers `wallet_*.json` dans Git
- Utiliser des mots de passe forts si vous chiffrez vos wallets
- Faire des sauvegardes régulières
- Vérifier les adresses avant d'envoyer des tokens
- Tester avec de petites quantités d'abord

---

## 📝 Structure des fichiers

```
simplequantumresistantblockchain/
├── blockchain_node.py          # Nœud blockchain avec API REST
├── wallet_manager.py           # Gestionnaire de wallet CLI
├── distribute_treasury.py      # Script de distribution depuis le trésor
├── requirements.txt             # Dépendances Python
├── README.md                    # Ce fichier
├── .gitignore                   # Fichiers à ignorer par Git
├── wallet_*.json                # Wallets créés (NE PAS COMMITER)
├── wallets_*.json               # Wallets de test (NE PAS COMMITER)
└── treasury_*.json              # Wallet du trésor (NE PAS COMMITER)
```

---

## ☁️ Déployer dans le Cloud (Gratuit)

Cette section vous montre comment déployer votre nœud blockchain sur différentes plateformes cloud gratuites.

### 📋 Préparation

Avant de déployer, assurez-vous que :
1. ✅ Votre code est dans un dépôt Git (GitHub, GitLab, etc.)
2. ✅ Tous les fichiers sont commités
3. ✅ Vous avez un compte sur la plateforme choisie

### Option 1 : Render (Recommandé - Gratuit) ⭐

**Avantages :**
- ✅ Gratuit pour toujours (avec limitations)
- ✅ Déploiement automatique depuis GitHub
- ✅ HTTPS automatique
- ✅ Facile à configurer

**Limitations gratuites :**
- Le service s'endort après 15 minutes d'inactivité
- Redémarre automatiquement à la première requête

#### Étape 1 : Créer un compte

1. Allez sur https://render.com
2. Cliquez sur **"Get Started for Free"**
3. Connectez-vous avec GitHub, GitLab ou email

#### Étape 2 : Créer un nouveau service

1. Dans le dashboard, cliquez sur **"New +"**
2. Sélectionnez **"Web Service"**
3. Connectez votre dépôt GitHub/GitLab
4. Sélectionnez le dépôt contenant votre code

#### Étape 3 : Configurer le service

**Paramètres :**
- **Name** : `blockchain-node` (ou le nom de votre choix)
- **Environment** : `Python 3`
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `python blockchain_node.py --port $PORT`
- **Plan** : **Free**

**Variables d'environnement :**
- `PORT` : Laissé vide (Render le définit automatiquement)
- ⚠️ **Note importante** : L'adresse du trésor est maintenant codée directement dans le code. Vous n'avez **PAS besoin** de définir `TREASURY_ADDRESS` - elle est automatique !

#### Étape 4 : Déployer

1. Cliquez sur **"Create Web Service"**
2. Attendez 2-3 minutes pour le déploiement
3. Votre nœud sera disponible à l'URL fournie (ex: `https://blockchain-node.onrender.com`)

#### Étape 5 : Tester

```bash
# Vérifier que le nœud est en ligne
curl https://votre-app.onrender.com/health

# Créer un wallet
curl -X POST https://votre-app.onrender.com/wallet/create
```

**⚠️ Note :** Le service gratuit s'endort après 15 minutes. La première requête après le sommeil prendra 30-60 secondes pour redémarrer.

---

### Option 2 : Railway (Gratuit avec crédits)

**Avantages :**
- ✅ 5$ de crédits gratuits par mois
- ✅ Déploiement très rapide
- ✅ Pas de sommeil automatique
- ✅ Support Docker

**Limitations :**
- Crédits limités (environ 100 heures/mois gratuits)
- Peut nécessiter une carte bancaire (mais pas de frais si vous restez dans les limites)

#### Étape 1 : Créer un compte

1. Allez sur https://railway.app
2. Cliquez sur **"Start a New Project"**
3. Connectez-vous avec GitHub

#### Étape 2 : Déployer depuis GitHub

1. Cliquez sur **"Deploy from GitHub repo"**
2. Sélectionnez votre dépôt
3. Railway détecte automatiquement Python et installe les dépendances

#### Étape 3 : Configurer

1. Dans les **Settings** du service :
   - **Start Command** : `python blockchain_node.py --port $PORT`
2. Railway définit automatiquement la variable `PORT`

#### Étape 4 : Obtenir l'URL

1. Cliquez sur l'onglet **"Settings"**
2. Cliquez sur **"Generate Domain"**
3. Votre URL sera : `https://votre-app.up.railway.app`

**💡 Astuce :** Surveillez votre utilisation de crédits dans le dashboard pour éviter les frais.

---

### Option 3 : Fly.io (Gratuit avec limitations)

**Avantages :**
- ✅ 3 machines virtuelles gratuites
- ✅ Déploiement global
- ✅ Pas de sommeil automatique
- ✅ Support Docker natif

**Limitations :**
- 256 MB RAM par machine gratuite
- 3 GB de stockage partagé

#### Étape 1 : Installer Fly CLI

**Windows (PowerShell) :**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**macOS :**
```bash
curl -L https://fly.io/install.sh | sh
```

**Linux :**
```bash
curl -L https://fly.io/install.sh | sh
```

#### Étape 2 : Créer un compte

```bash
fly auth signup
```

Ou via le site : https://fly.io

#### Étape 3 : Déployer

```bash
# Dans le dossier de votre projet
fly launch

# Répondez aux questions :
# - App name : blockchain-node (ou votre choix)
# - Region : choisissez le plus proche
# - Postgres/Redis : Non
```

#### Étape 4 : Vérifier le déploiement

```bash
# Voir l'URL de votre app
fly status

# Ouvrir dans le navigateur
fly open
```

**Le fichier `fly.toml` est déjà configuré pour vous !**

---

### Option 4 : Heroku (Gratuit limité)

**⚠️ Note :** Heroku a supprimé son plan gratuit, mais vous pouvez utiliser l'essai gratuit de 7 jours.

**Avantages :**
- ✅ Très populaire et bien documenté
- ✅ Déploiement simple avec Git

#### Étape 1 : Installer Heroku CLI

**Windows :**
Téléchargez depuis : https://devcenter.heroku.com/articles/heroku-cli

**macOS :**
```bash
brew tap heroku/brew && brew install heroku
```

**Linux :**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

#### Étape 2 : Créer un compte

1. Allez sur https://heroku.com
2. Créez un compte gratuit
3. Vérifiez votre email

#### Étape 3 : Se connecter

```bash
heroku login
```

#### Étape 4 : Créer l'application

```bash
# Dans le dossier de votre projet
heroku create blockchain-node

# Déployer
git push heroku main
```

#### Étape 5 : Ouvrir l'application

```bash
heroku open
```

**Le fichier `Procfile` est déjà configuré pour vous !**

---

### Option 5 : Google Cloud Run (Gratuit avec limites)

**Avantages :**
- ✅ 2 millions de requêtes gratuites par mois
- ✅ 360 000 GB-secondes de CPU gratuits
- ✅ HTTPS automatique
- ✅ Scaling automatique

**Limitations :**
- Nécessite une carte bancaire (mais pas de frais dans les limites gratuites)
- Service s'endort après inactivité

#### Étape 1 : Créer un projet

1. Allez sur https://console.cloud.google.com
2. Créez un nouveau projet
3. Activez l'API Cloud Run

#### Étape 2 : Installer Google Cloud SDK

**Windows :**
Téléchargez depuis : https://cloud.google.com/sdk/docs/install

**macOS :**
```bash
brew install --cask google-cloud-sdk
```

**Linux :**
```bash
curl https://sdk.cloud.google.com | bash
```

#### Étape 3 : Se connecter

```bash
gcloud auth login
gcloud config set project VOTRE_PROJECT_ID
```

#### Étape 4 : Déployer avec Docker

```bash
# Construire et déployer
gcloud run deploy blockchain-node \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Étape 5 : Obtenir l'URL

```bash
gcloud run services describe blockchain-node --region us-central1
```

---

### Option 6 : Oracle Cloud (VPS Gratuit) ⭐⭐⭐

**Avantages :**
- ✅ VPS gratuit pour toujours (2 instances)
- ✅ 4 CPU OCPU et 24 GB RAM au total
- ✅ 200 GB de stockage
- ✅ Pas de sommeil automatique
- ✅ Performance complète

**Limitations :**
- Configuration plus complexe
- Nécessite une carte bancaire (mais pas de frais)

#### Étape 1 : Créer un compte

1. Allez sur https://www.oracle.com/cloud/free/
2. Cliquez sur **"Start for Free"**
3. Créez un compte (carte bancaire requise mais pas de frais)

#### Étape 2 : Créer une instance

1. Dans le dashboard, allez dans **"Compute" > "Instances"**
2. Cliquez sur **"Create Instance"**
3. Choisissez :
   - **Image** : Ubuntu 22.04
   - **Shape** : VM.Standard.A1.Flex (ARM)
   - **OCPU** : 2
   - **Memory** : 12 GB
   - **Boot Volume** : 100 GB

#### Étape 3 : Configurer le firewall

1. Allez dans **"Networking" > "Virtual Cloud Networks"**
2. Modifiez les règles de sécurité pour autoriser le port 5000 (ou celui que vous utilisez)

#### Étape 4 : Se connecter à l'instance

```bash
# Via SSH (utilisez la clé SSH fournie)
ssh opc@VOTRE_IP_PUBLIQUE
```

#### Étape 5 : Installer Python et le projet

```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer Python
sudo apt install python3 python3-pip git -y

# Cloner votre projet
git clone https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
cd VOTRE_REPO

# Installer les dépendances
pip3 install -r requirements.txt
```

#### Étape 6 : Lancer le nœud avec systemd (pour qu'il redémarre automatiquement)

```bash
# Créer un service systemd
sudo nano /etc/systemd/system/blockchain-node.service
```

**Contenu du fichier :**
```ini
[Unit]
Description=Blockchain Node Service
After=network.target

[Service]
Type=simple
User=opc
WorkingDirectory=/home/opc/VOTRE_REPO
ExecStart=/usr/bin/python3 /home/opc/VOTRE_REPO/blockchain_node.py --port 5000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Activer et démarrer :**
```bash
sudo systemctl daemon-reload
sudo systemctl enable blockchain-node
sudo systemctl start blockchain-node

# Vérifier le statut
sudo systemctl status blockchain-node
```

#### Étape 7 : Accéder au nœud

Votre nœud sera accessible à : `http://VOTRE_IP_PUBLIQUE:5000`

**💡 Pour un nom de domaine :** Utilisez un service comme No-IP ou DuckDNS pour avoir un nom de domaine gratuit.

---

### Option 7 : DigitalOcean App Platform (Essai gratuit)

**Avantages :**
- ✅ 100$ de crédits gratuits (valable 60 jours)
- ✅ Déploiement automatique
- ✅ HTTPS automatique

#### Étape 1 : Créer un compte

1. Allez sur https://www.digitalocean.com
2. Créez un compte avec un code promo (cherchez "DigitalOcean promo code")
3. Vous recevrez 100$ de crédits

#### Étape 2 : Créer une App

1. Dans le dashboard, allez dans **"App Platform"**
2. Cliquez sur **"Create App"**
3. Connectez votre dépôt GitHub
4. Sélectionnez votre dépôt

#### Étape 3 : Configurer

- **Build Command** : `pip install -r requirements.txt`
- **Run Command** : `python blockchain_node.py --port $PORT`
- **Plan** : Basic (5$/mois, mais gratuit avec les crédits)

#### Étape 4 : Déployer

Cliquez sur **"Create Resources"** et attendez le déploiement.

---

### Comparaison des options

| Plateforme | Gratuit | Sommeil | Performance | Difficulté |
|------------|---------|---------|-------------|------------|
| **Render** | ✅ Oui | ⚠️ Oui (15 min) | ⭐⭐ | ⭐ Facile |
| **Railway** | ✅ Oui (crédits) | ❌ Non | ⭐⭐⭐ | ⭐ Facile |
| **Fly.io** | ✅ Oui | ❌ Non | ⭐⭐⭐ | ⭐⭐ Moyen |
| **Heroku** | ⚠️ Essai 7j | ⚠️ Oui | ⭐⭐ | ⭐ Facile |
| **Google Cloud Run** | ✅ Oui (limites) | ⚠️ Oui | ⭐⭐⭐ | ⭐⭐ Moyen |
| **Oracle Cloud** | ✅ Oui (VPS) | ❌ Non | ⭐⭐⭐⭐ | ⭐⭐⭐ Difficile |
| **DigitalOcean** | ✅ Essai (100$) | ❌ Non | ⭐⭐⭐ | ⭐⭐ Moyen |

### 🎯 Recommandation

- **Pour débuter rapidement** : **Render** (le plus simple)
- **Pour un service toujours actif** : **Railway** ou **Fly.io**
- **Pour la meilleure performance** : **Oracle Cloud** (VPS gratuit)

### 🔒 Sécurité en production

Quand vous déployez dans le cloud :

1. **Utilisez HTTPS** : La plupart des plateformes le fournissent automatiquement
2. **Protégez les endpoints sensibles** : Ajoutez une authentification pour `/treasury/distribute`
3. **Limitez les accès** : Utilisez un firewall pour limiter les IPs autorisées
4. **Sauvegardez les wallets** : Ne stockez jamais les clés privées dans le code
5. **Utilisez des variables d'environnement** : Pour les configurations sensibles

### 📝 Variables d'environnement recommandées

**✅ BONNE NOUVELLE :** L'adresse du trésor est maintenant **codée directement dans le code** !

Vous n'avez **PAS besoin** de définir `TREASURY_ADDRESS` - tous les nœuds utilisent automatiquement la même adresse officielle pour garantir la cohérence du réseau.

Si vous voulez créer un fichier `.env` (et l'ajouter au `.gitignore`) :

```bash
# Port (défini automatiquement par la plateforme)
PORT=5000

# Configuration d'inactivité (optionnel)
INACTIVITY_DAYS=30

# ⚠️ TREASURY_ADDRESS n'est plus nécessaire - elle est automatique !
```

**Pour plus de détails sur ce changement, consultez [CHANGELOG_TREASURY.md](CHANGELOG_TREASURY.md)**

### 🐛 Dépannage du déploiement cloud

#### Le service ne démarre pas

1. Vérifiez les logs :
   - **Render** : Dashboard > Logs
   - **Railway** : Dashboard > Deployments > Logs
   - **Fly.io** : `fly logs`
   - **Heroku** : `heroku logs --tail`

2. Vérifiez que le port est correct :
   - Utilisez `$PORT` (variable d'environnement)
   - Ne hardcodez pas le port

#### Le service s'endort

- **Render** : C'est normal, il se réveille automatiquement
- **Railway** : Ne devrait pas s'endormir
- **Fly.io** : Vérifiez la configuration dans `fly.toml`

#### Erreur "Module not found"

1. Vérifiez que `requirements.txt` contient toutes les dépendances
2. Vérifiez les logs de build pour voir si l'installation a réussi

#### Erreur de port

Assurez-vous que votre code lit le port depuis `os.environ.get('PORT')` :
```python
port = int(os.environ.get('PORT', 5000))
```

Le code a déjà été mis à jour pour supporter cela automatiquement !

---

## 🚀 Prochaines étapes

Pour aller plus loin :

- [ ] Implémenter un vrai algorithme Dilithium (via liboqs-python)
- [ ] Ajouter la synchronisation P2P automatique
- [ ] Implémenter le slashing (pénalités)
- [ ] Ajouter un explorateur de blocs (interface web)
- [ ] Implémenter le unbonding period
- [ ] Ajouter la délégation de stake
- [ ] Ajouter un système de smart contracts simple
- [ ] Implémenter la persistance sur disque (sauvegarde automatique)

---

## 📚 Ressources

- [QRL Documentation](https://docs.theqrl.org/)
- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Documentation](https://docs.python.org/3/)

---

## 📄 Licence

Ce projet est fourni à des fins éducatives.

---

**Bon minage ! ⛏️🔗**

Si vous avez des questions ou des problèmes, consultez la section [Dépannage](#-dépannage-détaillé) ou créez une issue sur le dépôt.
