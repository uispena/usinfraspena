#!/usr/bin/env bash
set -euo pipefail

echo "[info] Running with Docker on this host"
# build + run locally (no GHCR pull needed)
docker compose up -d --build
echo "[info] Health check:"
curl -fsS http://localhost:8000/health || true

