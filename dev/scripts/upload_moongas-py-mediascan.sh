#!/bin/bash
set -euo pipefail
rsync -ahvP "$MOONGAS_COLLECTION_ROOTDIR/moongas-py-mediascan/" root@$MEDIASERVER_DROPLET_IP:/var/www/moongas/moongas-py-mediascan/ --delete 

