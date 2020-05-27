#!/usr/bin/env sh
set -e
  
until python ./connect.py; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
