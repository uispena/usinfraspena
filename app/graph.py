import os, json, numpy as np, faiss
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama
from app.rag.index import ensure_index

class Graph:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.embed = SentenceTransformer(cfg["embed"]["name"])
        self.llm = Llama(
            model_path=cfg["llm"]["gguf_path"],
            n_ctx=cfg["llm"]["n_ctx"],
            n_gpu_layers=cfg["llm"]["n_gpu_layers"],
            verbose=False
        )
        ensure_index(cfg)
        self.index, self.meta = self._load_index()

    def _load_index(self):
        vdb = self.cfg["rag"]["vdb_path"]
        idx_path, meta_path = f"{vdb}/faiss.index", f"{vdb}/meta.json"
        index = faiss.read_index(idx_path) if os.path.exists(idx_path) else None
        meta = {}
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f: meta = json.load(f)
        return index, meta

    def retrieve(self, query: str, k: int = 6) -> str:
        if self.index is None or getattr(self.index, "ntotal", 0) == 0 or not self.meta:
            return ""
        q = self.embed.encode([query], normalize_embeddings=True)
        k = max(1, min(k, self.index.ntotal))
        D, I = self.index.search(np.array(q, dtype=np.float32), k)
        parts = []
        for idx in I[0]:
            if idx < 0: continue
            m = self.meta.get(str(idx))
            if not m: continue
            parts.append(f"[{m['source']}:{m['start']}-{m['end']}]\n{m['text']}")
        return "\n\n---\n\n".join(parts)

    def llm_generate(self, prompt: str) -> str:
        with open("app/system_prompt.txt") as sp: sys_p = sp.read().strip()
        prompt = sys_p + "\n\nUser:\n" + prompt + "\n\nAssistant:"
        out = self.llm(
            prompt,
            max_tokens=512,
            temperature=self.cfg["llm"]["temp"],
            top_p=self.cfg["llm"]["top_p"],
            stop=["</s>", "###", "User:"],
        )
        return out["choices"][0]["text"].strip()
