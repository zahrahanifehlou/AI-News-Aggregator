#!/bin/sh

echo "Waiting for Postgres..."
while ! python -c "
import socket, os, time
s = socket.socket()
host = os.getenv('POSTGRES_HOST', 'postgres')
port = int(os.getenv('POSTGRES_PORT', 5432))
s.connect((host, port))
print('Postgres is ready!')
" 2>/dev/null; do
  sleep 1
done

echo "Waiting for Redis..."
while ! python -c "
import socket, os
s = socket.socket()
host = os.getenv('REDIS_HOST', 'redis')
port = int(os.getenv('REDIS_PORT', 6379))
s.connect((host, port))
print('Redis is ready!')
" 2>/dev/null; do
  sleep 1
done

echo "Waiting for Ollama..."
while ! python -c "
import socket, os, time
s = socket.socket()
host = os.getenv('OLLAMA_HOST', 'ollama').replace('http://', '').replace('https://', '').split(':')[0]
port = 11434
print(f'Waiting for Ollama at {host}:{port}...')
s.connect((host, port))
print('Ollama is ready!')
" 2>/dev/null; do
  sleep 2
done

echo "All services are ready. Starting application..."
exec "$@"