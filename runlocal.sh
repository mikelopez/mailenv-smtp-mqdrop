#!/bin/bash
set -euo pipefail
trap 'echo "💥 Script failed on line $LINENO: $BASH_COMMAND"' ERR

cd "$(dirname "$0")"

LOCALENV="$HOME/Desktop/dev/localenv"

# Load envs
if [ -f $LOCALENV ]; then
  source $LOCALENV
else
  echo "❌ Missing $LOCALENV"
  exit 1
fi





# Build image

IMAGE_NAME="mailenv-smtp-mqdrop:localdev"

docker build \
  --build-arg APPVER=localdev \
  -t ${IMAGE_NAME} .

# Stop + remove old containers
CONTAINERS=$(docker ps -a | grep mailenv-smtp-mqdrop | awk '{print $1}' || true)
if [ -n "$CONTAINERS" ]; then
  for c in $CONTAINERS; do
    docker stop "$c" || true
    docker rm "$c" || true
  done
fi

# Remove old images
IMAGES=$(docker images | grep mailenv-smtp-mqdrop | awk '{print $3}' || true)
for img in $IMAGES; do
  docker rmi -f "$img" || true
done

# Run
docker-compose -f docker-compose.yaml up -d --remove-orphans mailenv-smtp-mqdrop-local



echo "🚀 Running..."