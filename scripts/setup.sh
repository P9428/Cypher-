#!/usr/bin/env bash
# Install Python dependencies for tests
set -euo pipefail

if [ ! -f requirements.txt ]; then
  echo "requirements.txt not found" >&2
  exit 1
fi

pip install -r requirements.txt
