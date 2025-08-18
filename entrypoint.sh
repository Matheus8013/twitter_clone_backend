#!/bin/sh

until nc -z db 5432; do
  echo "Aguardando o banco de dados..."
  sleep 1
done

exec "$@"