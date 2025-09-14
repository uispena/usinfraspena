#!/usr/bin/env bash
set -euo pipefail
exec > >(tee -i fix.log) 2>&1

ROOT="${1:-$HOME/kubeaid-agent}"
cd "$ROOT"

# Ensure llama-cpp-python is in requirements
grep -q '^llama-cpp-python' requirements.txt || cat >> requirements.txt <<'EOR'
llama-cpp-python==0.2.90
EOR

# Use CUDA *devel* image so nvcc exists; preinstall SMALL CPU torch to dodge huge CUDA wheels
cat > docker/Dockerfile <<'EOD'
FROM nvidia/cuda:12.2.2-devel-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/usr/local/cuda/bin:$PATH
ENV CUDA_HOME=/usr/local/cuda
ENV CUDAToolkit_ROOT=/usr/local/cuda

RUN apt-get update && apt-get install -y \
    python3 python3-pip git build-essential cmake ninja-build jq \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Tiny CPU torch (for embeddings) so we don't pull the massive CUDA wheels
RUN pip3 install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
    torch==2.3.1 torchvision==0.18.1

# Build llama-cpp-python with CUDA (GGML_CUDA/CUBLAS)
ENV FORCE_CMAKE=1
ENV CMAKE_ARGS="-DGGML_CUDA=ON -DGGML_NATIVE=OFF -DCMAKE_BUILD_TYPE=Release"
ENV LLAMA_CUBLAS=1

COPY requirements.txt /workspace/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# App code & config
COPY app /workspace/app
COPY config.yaml /workspace/config.yaml

EXPOSE 8000
CMD ["python3", "app/server.py"]
EOD

echo "[*] Rebuilding (CUDA)…"
if ! docker compose build --no-cache; then
  echo "[!] CUDA build failed — falling back to CPU build."
  sed -i 's/^ENV CMAKE_ARGS.*/ENV CMAKE_ARGS="-DGGML_CUDA=OFF -DGGML_NATIVE=OFF -DCMAKE_BUILD_TYPE=Release"/' docker/Dockerfile
  sed -i 's/^ENV LLAMA_CUBLAS=1/# LLAMA_CUBLAS disabled for CPU/' docker/Dockerfile
  docker compose build --no-cache
fi

echo "[*] Starting…"
docker compose up -d

echo "[*] Done. Logs:"
docker logs -f kubeaid-agent || true

echo "[*] Quick tests:"
echo "  curl http://localhost:8000/health"
echo "  docker exec -it kubeaid-agent python3 - <<'PY'\nfrom llama_cpp import Llama; print('llama-cpp import OK')\nPY"
