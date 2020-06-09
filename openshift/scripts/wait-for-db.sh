#!/usr/bin/env sh
set -e
  
until python ./connect.py; do
  >&2 echo "DB is not available yet.."
  sleep 1
done
