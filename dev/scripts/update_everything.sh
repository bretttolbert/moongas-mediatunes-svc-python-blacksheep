#!/bin/bash
set -euo pipefail
./run-mediascan-scanfilesyaml
./run-mediascan-scanartistsyaml
./run-mediascan-scantodb
./upload-mediascandb
./update-covers
./upload-covers
./restart-remote-mediaserver
sudo ./restart-local-mediaserver
