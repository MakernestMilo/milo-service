#!/usr/bin/env bash
# Run by milo-update.timer. Updates only when main has a new commit, so it costs nothing otherwise.
set -euo pipefail
cd /opt/milo
# The folder belongs to the default user and this runs as root: tell git that is fine.
git config --global --get-all safe.directory 2>/dev/null | grep -qx /opt/milo || git config --global --add safe.directory /opt/milo
git fetch -q origin main
if [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]; then
  bash deploy/update.sh
fi
