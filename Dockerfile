# Utilisez une image Python officielle comme image de base
FROM python:3.9-slim

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers de dépendances et installez-les
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le reste du code de l'application dans le conteneur
COPY . .

# Exposez le port sur lequel l'application s'exécute
EXPOSE 8000

# Commande pour exécuter l'application
CMD ["python", "ace_exporter.py"]
