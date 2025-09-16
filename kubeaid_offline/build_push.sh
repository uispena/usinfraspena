#!/usr/bin/env bash
set -euo pipefail
: "${IMAGE:?usage: IMAGE=registry/ns/kubeaid:tag ./build_push.sh}"
docker build ${MODEL_URL:+--build-arg MODEL_URL="$MODEL_URL"} -t "$IMAGE" .
docker push "$IMAGE"
echo "IMAGE=$IMAGE" > image.env
echo "Built and pushed $IMAGE"
