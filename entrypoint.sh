#!/bin/bash

set -e

log() {
  echo -e "$1"
}

if [ "$(id -u)" -ne 0 ]; then
  echo "❌ This script must be run as root (current UID: $(id -u))"
  exit 1
fi

echo "#### ENTRYPOINT ####"
whoami

# Create log directory if it doesn't exist
if [ ! -d /app/mailenv-data ]; then
  echo "❌ Directory /app/mailenv-data does not exist. Exiting."
  exit 1
fi

pip install -r /app/requirements.txt 

# Start the Python script in background
echo "🚀 Starting 0mq.py..."
/usr/local/bin/python -u /app/0mq >> /app/mailenv-mq-in.log 2>&1 &

# Wait a moment for the log file to be created
sleep 2

# Follow the log file
echo "📋 Following log file..."
tail -f /app/mailenv-mq-in.log