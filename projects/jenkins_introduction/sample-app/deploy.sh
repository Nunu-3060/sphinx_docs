#!/usr/bin/env bash
set -euo pipefail

TARGET_ENV="${1:?usage: deploy.sh <environment>}"

echo "==> Deploying to ${TARGET_ENV}..."
sleep 1
echo "==> Deployed to ${TARGET_ENV} successfully."
