#!/bin/sh

set -e

HOST=${POSTGRES_HOST:-postgres}
PORT=${POSTGRES_PORT:-5432}

echo "⏳ Waiting for PostgreSQL at $HOST:$PORT..."

# Attente active jusqu'à ce que la connexion au port soit possible
while ! nc -z $HOST $PORT; do
  sleep 0.5
done

echo "✅ PostgreSQL is up - executing command"

# Lancer la commande passée en argument (uvicorn ...)
exec "$@"