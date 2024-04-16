#!/bin/bash

# Host and port that the script should wait for
HOST=household-manager
PORT=8000

# Wait for the host:port to be available (i.e., a successful connection can be made)
until bash -c "exec 3<>/dev/tcp/$HOST/$PORT" > /dev/null 2>&1; do
  echo "Waiting for $HOST:$PORT..."
  sleep 1
done

# Start Nginx once the connection is available
nginx -g 'daemon off;'