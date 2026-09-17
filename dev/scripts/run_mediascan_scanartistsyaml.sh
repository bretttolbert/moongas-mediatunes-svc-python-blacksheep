#!/bin/bash
set -euo pipefail

pushd moongas-go-mediascan > /dev/null
go run cmd/mediascan-artists-yaml/main.go "$MOONGAS_COLLECTION_ROOTDIR/mediascan-config.yml" "$MOONGAS_COLLECTION_ROOTDIR/mediascan-artists.yml"
popd > /dev/null