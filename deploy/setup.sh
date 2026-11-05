#!/usr/bin/env bash
# First-time set-up of a fresh Ubuntu 24.04 server (AWS Lightsail, Mumbai). Run once, as the default user:
#   curl -fsSL https://raw.githubusercontent.com/MakernestMilo/milo-service/main/deploy/setup.sh | bash
set -euo pipefail

sudo apt-get update -y
sudo apt-get install -y ca-certificates curl git
if ! command -v docker >/dev/null; then
  curl -fsSL https://get.docker.com | sudo sh
fi
sudo usermod -aG docker "$USER"

sudo mkdir -p /opt/milo && sudo chown "$USER" /opt/milo
if [ ! -d /opt/milo/.git ]; then
  git clone https://github.com/MakernestMilo/milo-service /opt/milo
fi
cd /opt/milo
if [ ! -f .env ]; then
  cp deploy/env.example .env
  chmod 600 .env
  echo
  echo "Now fill in /opt/milo/.env (MODEL_API_KEY, PANEL_TOKEN, DOMAIN), then run:"
  echo "  cd /opt/milo && sudo bash deploy/update.sh"
  exit 0
fi
sudo bash deploy/update.sh
