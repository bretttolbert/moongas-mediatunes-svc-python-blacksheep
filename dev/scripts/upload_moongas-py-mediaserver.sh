#!/bin/bash
set -euo pipefail
HOST=$MEDIASERVER_DROPLET_IP
DEST_USER=root
DEST_ROOT=/var/www/moongas
SVC=moongas-py-mediaserver
SOURCE=$SVC/
DEST=$DEST_USER@$HOST:$DEST_ROOT/$SVC/
echo "Uploading $SOURCE to $DEST"
# If first run, remove:
# 1) '--exclude 'app/templates/css.html' I added that because I've put my analytics html there
# 2) '--exclude 'mediaserver.service' I modify it on the server and symlink it to /etc/systemd/system/mediaserver.service
rsync -ahvP $SOURCE $DEST --delete --exclude 'app/templates/css.html' --exclude 'mediaserver.service' --exclude 'dev/' --exclude mediaserver-config.yml --exclude '.git/' --exclude '.gitignore' --exclude '__pycache__/' --exclude='.venv*'
echo "Uploaded $SOURCE to $DEST"
