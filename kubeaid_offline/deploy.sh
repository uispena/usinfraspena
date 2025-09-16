#!/usr/bin/env bash
set -euo pipefail
if [ -f image.env ]; then source image.env; fi
: "${IMAGE:?set IMAGE=registry/ns/kubeaid:tag or create image.env}"
sed "s#@IMAGE@#${IMAGE}#g" kubeaid.yaml | kubectl apply -f -
echo "Deployed $IMAGE to namespace kubeaid"
echo "Use: kubectl exec -it deploy/kubeaid -n kubeaid -- kubeaid-agent chat"
