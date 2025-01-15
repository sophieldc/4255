# Utiliser une image légère
FROM python:3.10-alpine

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires
COPY app.py /app/

# Installer les dépendances Flask et pymongo
RUN pip install flask pymongo

# Exposer le port 5000
EXPOSE 5000

# Lancer l’application Flask
CMD ["python", "app.py"]
