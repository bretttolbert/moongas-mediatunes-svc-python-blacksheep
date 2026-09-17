#!/bin/bash
set -euo pipefail

pushd moongas-go-mediascan > /dev/null
go run cmd/mediascan-db/main.go "$MOONGAS_COLLECTION_ROOTDIR/mediascan-config.yml" "$MOONGAS_COLLECTION_ROOTDIR/mediascan.db"
popd > /dev/null
