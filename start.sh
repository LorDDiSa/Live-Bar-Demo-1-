#!/usr/bin/env bash
set -e
export DB_PATH=${DB_PATH:-db.sqlite3}
echo "Seeding database at $DB_PATH (idempotent)..."
python seed.py || true
echo "Starting API..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8787}