#!/usr/bin/env bash
set -euo pipefail
OUT="${1:-docs}"
mkdir -p "$OUT"

# Curated admin docs (no comments, just URLs)
read -r -d '' URLS <<'EOF'
https://documentation.ubuntu.com/server/
https://documentation.ubuntu.com/server/how-to/
https://debian-handbook.info/browse/stable/
https://www.freedesktop.org/software/systemd/man/systemctl.html
https://www.freedesktop.org/software/systemd/man/journalctl.html
https://kubernetes.io/docs/tasks/
https://kubernetes.io/docs/tasks/debug/
https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/
https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/
https://kubernetes.io/docs/reference/kubectl/
https://kubernetes.io/docs/reference/kubectl/quick-reference/
https://kubernetes.io/docs/concepts/cluster-administration/
https://docs.uipath.com/automation-suite/automation-suite/2024.10/installation-guide/
https://docs.uipath.com/automation-suite/automation-suite/2024.10/installation-guide/troubleshooting
https://docs.uipath.com/automation-suite/automation-suite/2024.10/installation-guide/running-the-diagnostics-tool
https://docs.uipath.com/automation-suite/automation-suite/2024.10/installation-guide/using-support-bundle-tool
EOF

i=0
echo "$URLS" | while IFS= read -r U; do
  [ -z "$U" ] && continue
  i=$((i+1))
  F="$OUT/$(echo "$U" | sed 's~https\?://~~; s~[^A-Za-z0-9._-]~_~g').html"
  echo "[$(printf %02d "$i")] GET $U"
  curl -fsSL --retry 3 --retry-delay 1 "$U" -o "$F" || echo "WARN: failed $U"
done

tar -C "$OUT" -czf docs-bundle.tar.gz .
echo "Wrote docs-bundle.tar.gz"
sha256sum docs-bundle.tar.gz || shasum -a 256 docs-bundle.tar.gz || true

