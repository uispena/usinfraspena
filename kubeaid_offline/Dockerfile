FROM debian:bookworm AS llbuild
RUN apt-get update && apt-get install -y --no-install-recommends build-essential cmake git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 https://github.com/ggerganov/llama.cpp /src \
    && make -C /src -j$(nproc) server

FROM curlimages/curl:8.8.0 AS fetch
WORKDIR /out
ARG KUBECTL_VERSION=v1.32.3
RUN curl -fL https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl -o kubectl && chmod +x kubectl

FROM python:3.10-slim AS ingest
WORKDIR /ingest
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
RUN apt-get update && apt-get install -y --no-install-recommends git unzip && rm -rf /var/lib/apt/lists/*
COPY ingest.py ./ingest.py
RUN pip install "faiss-cpu==1.8.0" "sentence-transformers==2.7.0" "beautifulsoup4==4.12.3" "lxml==5.2.2"
COPY docs-bundle.tar.gz* ./ || true
COPY docs/ ./docs/
RUN python3 ingest.py

FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends jq ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=llbuild2 /src/build/bin/llama-server /usr/local/bin/llama-server
COPY --from=fetch /out/kubectl /usr/local/bin/kubectl
COPY kubeaid-agent.pyz /app/kubeaid-agent.pyz
ARG MODEL_URL="https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
RUN mkdir -p /models && python3 - <<PY
import os,urllib.request
u=os.environ.get("MODEL_URL")
p="/models/model.gguf"
print("Downloading model:",u)
urllib.request.urlretrieve(u,p)
print("Saved:",p)
PY
COPY --from=ingest /ingest/index /app/index
RUN printf '%s\n' '#!/usr/bin/env bash'   'set -euo pipefail'   'export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"'   'if [ -f /var/run/secrets/kubernetes.io/serviceaccount/token ]; then unset KUBECONFIG; fi'   ': "${LLM_MODEL_PATH:=/models/model.gguf}"'   'export LLM_MODEL_PATH'   'exec python3 /app/kubeaid-agent.pyz "$@"'   > /usr/local/bin/kubeaid-agent && chmod 0755 /usr/local/bin/kubeaid-agent
CMD ["/bin/sh","-lc","echo KubeAid ready. Use: kubeaid-agent chat; sleep infinity"]

# -- Build llama-server via CMake (CPU) --
FROM debian:bookworm AS llbuild2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 https://github.com/ggml-org/llama.cpp /src
WORKDIR /src
RUN cmake -S . -B build -DGGML_BLAS=OFF -DCMAKE_BUILD_TYPE=Release -DLLAMA_CURL=OFF
RUN cmake --build build -j $(nproc) --target llama-server
