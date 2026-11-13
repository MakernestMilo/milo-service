#!/usr/bin/env bash
# Bring the server up to date with main and restart Milo. GitHub runs this after every merge;
# it is also safe to run by hand: cd /opt/milo && sudo bash deploy/update.sh
set -euo pipefail
cd /opt/milo
# The folder belongs to the default user and this runs as root: tell git that is fine.
git config --global --get-all safe.directory 2>/dev/null | grep -qx /opt/milo || git config --global --add safe.directory /opt/milo
git fetch -q origin main
git reset -q --hard origin/main
export GIT_COMMIT=$(git rev-parse --short HEAD)
docker compose build -q milo
docker compose up -d --remove-orphans
docker image prune -f >/dev/null
for i in $(seq 1 30); do
  if docker compose exec -T milo python -c "import urllib.request,sys; sys.exit(0 if b'\"status\":\"ok\"' in urllib.request.urlopen('http://127.0.0.1:8000/health').read() else 1)" 2>/dev/null; then
    echo "Milo is up at build $GIT_COMMIT"
    exit 0
  fi
  sleep 2
done
echo "Milo did not answer /health in 60 seconds:" >&2
docker compose logs --tail 40 milo >&2
exit 1
