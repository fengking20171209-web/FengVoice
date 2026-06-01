#!/usr/bin/env sh
set -eu
curl --fail --silent --show-error "${FENGVOICE_API_URL:-http://localhost:8000}/health"

