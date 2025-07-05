FROM python:3.10-slim

WORKDIR /app

# Copier uniquement les requirements
COPY ../requirements.txt /app/requirements.txt

# Installer les dépendances
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copier le reste du code
COPY . /app

# Ajouter et rendre exécutable le script d'attente PostgreSQL
COPY gateway/wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

# Définir le chemin racine Python
ENV PYTHONPATH=/backend

# Commande de démarrage : attente Postgres puis lancement FastAPI
CMD ["/wait-for-postgres.sh", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

