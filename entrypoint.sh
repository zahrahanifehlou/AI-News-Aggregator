#!/bin/sh

echo "Waiting for Postgres..."
while ! python -c "
import socket
import os
import time
s = socket.socket()
host = os.getenv('POSTGRES_HOST', 'postgres')
port = int(os.getenv('POSTGRES_PORT', 5432))
print(f'Waiting for Postgres at {host}:{port}...')
s.connect((host, port))
print('Postgres is ready!')
" 2>/dev/null; do
  sleep 1
done

echo "Waiting for Redis..."
while ! python -c "
import socket
import os
s = socket.socket()
host = os.getenv('REDIS_HOST', 'redis')
port = int(os.getenv('REDIS_PORT', 6379))
s.connect((host, port))
print('Redis is ready!')
" 2>/dev/null; do
  sleep 1
done

echo "All dependencies are ready. Starting application..."

# Execute the command passed as arguments
exec "$@"