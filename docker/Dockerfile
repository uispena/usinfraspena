FROM nvidia/cuda:12.2.2-devel-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/usr/local/cuda/bin:$PATH
ENV CUDA_HOME=/usr/local/cuda
ENV CUDAToolkit_ROOT=/usr/local/cuda

RUN apt-get update && apt-get install -y \
    python3 python3-pip git build-essential cmake ninja-build jq curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
RUN curl -fsSL https://dl.k8s.io/release/$(curl -fsSL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl \ 
 && chmod +x /usr/local/bin/kubectl
RUN curl -fsSL https://dl.k8s.io/release/$(curl -fsSL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl \ 
 && chmod +x /usr/local/bin/kubectl

# Tiny CPU torch (for embeddings) so we don't pull the massive CUDA wheels
RUN pip3 install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
    torch==2.3.1 torchvision==0.18.1

# Build llama-cpp-python with CUDA (GGML_CUDA/CUBLAS)
ENV FORCE_CMAKE=1
ENV CMAKE_ARGS="-DGGML_CUDA=OFF -DGGML_NATIVE=OFF -DCMAKE_BUILD_TYPE=Release"
# LLAMA_CUBLAS disabled for CPU

COPY requirements.txt /workspace/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# App code & config
COPY app /workspace/app
RUN printf %s\n "#!\/usr\/bin\/env bash" "set -euo pipefail" "python3 -m app.cli \"\$@\"" > \/usr\/local\/bin\/kubeaid && chmod +x \/usr\/local\/bin\/kubeaid
RUN touch /workspace/app/__init__.py
COPY config.yaml /workspace/config.yaml

EXPOSE 8000
CMD ["uvicorn","app.server:app","--host","0.0.0.0","--port","8000","--workers","1"]


