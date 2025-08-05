#!/bin/sh
set -e

echo "#### ENTRYPOINT (Go) ####"
whoami

# Ensure mount dir exists
if [ ! -d /app/mailenv-data ]; then
  echo "❌ Directory /app/mailenv-data does not exist. Exiting."
  exit 1
fi

# Start the Go daemon
echo "🚀 Starting Go mqdrop..."
/app/mqdrop >> /app/mailenv-mq-in.log 2>&1 &

sleep 2

# Follow logs
echo "📋 Following log file..."
tail -f /app/mailenv-mq-in.log
