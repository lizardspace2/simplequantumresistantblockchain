# Dockerfile pour déployer le nœud blockchain
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY blockchain_node.py .
COPY wallet_manager.py .
COPY distribute_treasury.py .

# Exposer le port (sera défini par la variable d'environnement PORT)
# Utiliser un port par défaut mais le code lit $PORT depuis l'environnement
EXPOSE 5000

# Commande pour démarrer l'application
# Le code lit automatiquement $PORT depuis l'environnement
CMD ["python", "blockchain_node.py"]

