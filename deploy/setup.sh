#!/usr/bin/env bash
# First-time set-up of a fresh Ubuntu 24.04 server (AWS Lightsail, Mumbai). Run once, as the default user:
#   curl -fsSL https://raw.githubusercontent.com/MakernestMilo/milo-service/main/deploy/setup.sh | bash
# It asks for one thing, the Anthropic key. Everything else it does by itself, and from then on the
# server keeps itself up to date with main (deploy/milo-update.timer), so GitHub needs no secrets.
set -euo pipefail

sudo apt-get update -y
sudo apt-get install -y ca-certificates curl git openssl
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
fi
# The panel's password: a long random one, made here, never typed by anybody.
if grep -q '^PANEL_TOKEN=$' .env; then
  sed -i "s/^PANEL_TOKEN=$/PANEL_TOKEN=$(openssl rand -hex 24)/" .env
fi
# The Anthropic key: asked for once, read from the keyboard, never shown on the screen.
if grep -q '^MODEL_API_KEY=$' .env; then
  echo
  printf 'Paste the Anthropic API key and press Enter (nothing shows while you paste): '
  read -rs KEY < /dev/tty; echo
  KEY=$(printf '%s' "$KEY" | tr -d '[:space:]')
  if [ -z "$KEY" ]; then echo "No key given. Run this again when you have it." >&2; exit 1; fi
  sed -i "s|^MODEL_API_KEY=$|MODEL_API_KEY=$KEY|" .env
  unset KEY
fi

# Keep itself up to date: every 5 minutes, if main has moved, run deploy/update.sh.
sudo cp deploy/milo-update.service deploy/milo-update.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now milo-update.timer

sudo bash deploy/update.sh
echo
echo "Milo's panel password is in /opt/milo/.env (PANEL_TOKEN)."
