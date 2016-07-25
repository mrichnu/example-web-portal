#!/bin/bash
set -e

if [ "$ENV" = 'DEV' ]; then
  echo "Running Development Server"
  exec python "app.py"
else
  echo "Running Production Server"
  exec /usr/local/bin/gunicorn -w 2 -b :8000 app:app
fi