#!/bin/sh

env > /container-config/.cronenv
sed -i 's/\"/\\"/g' /container-config/.cronenv
cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 32 | head -n 1 > /app/git_hash

# elevation permissions required
sudo /startup.sh
poetry run gunicorn govapp.wsgi --bind :8080 --config /app/gunicorn.conf.py
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start gunicorn: $status"
  exit $status
fi
