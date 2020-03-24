#!/bin/sh
# wait-for-db.sh

set -e

cmd="$@"

until python docker-test/container-scripts/connect.py; do
  >&2 echo "Database is unavailable yet - wait 3 sec..."
  sleep 3
done

>&2 echo "Database is up - executing command"
exec $cmd
