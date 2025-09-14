# KubeAid Agent (Portable, Offline)

## Features
- Offline LLM (llama.cpp) + small instruct model (7B–8B, GGUF).
- RAG over your Linux/K8s notes, logs, and playbooks (FAISS + SQLite).
- CLI assistant (`agent_cli.py`) + optional FastAPI server (`server.py`).
- Minimal tools: `kubectl` queries, `journalctl`, node facts.
- Optional QLoRA fine-tune pipeline (one GPU).

## Quickstart
1. `docker compose up --build` (pulls model if present; otherwise run `scripts/download_models.sh`).
2. In another terminal: `python app/agent_cli.py`
3. Ask: "Which nodes have a taint?" or "Why is kubelet flapping?" or "Inspect pod logs for X".

## Data layout
- `data/corpora/` put your markdown/faq/log snippets here.
- `data/vectordb/` FAISS + SQLite index is written here.
- `models/llm/` put GGUF file here (e.g., llama-3-8b-instruct.Q4_K_M.gguf)
- `models/embed/` embedding model cache.

## Fine-tune (optional)
See `scripts/finetune_qlora.sh` and `app/rag/prepare_dataset.py`.

