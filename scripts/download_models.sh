#!/usr/bin/env bash
set -euo pipefail
mkdir -p models/llm models/embed

# Example GGUF hotspot (you can replace with your mirror / offline stash)
# Place your GGUF file at models/llm/llama-3-8b-instruct.Q4_K_M.gguf
echo ">> Place your GGUF at models/llm/llama-3-8b-instruct.Q4_K_M.gguf"
echo ">> Or update config.yaml llm.gguf_path to match your file."

# Embeddings are pulled on first run by sentence-transformers and cached to models/embed

