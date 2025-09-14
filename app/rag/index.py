import os, json, numpy as np, faiss
from sentence_transformers import SentenceTransformer
from .ingest import load_chunks

def ensure_index(cfg: dict):
    vdb = cfg["rag"]["vdb_path"]
    os.makedirs(vdb, exist_ok=True)
    idx_path, meta_path = f"{vdb}/faiss.index", f"{vdb}/meta.json"
    if os.path.exists(idx_path) and os.path.exists(meta_path):
        return

    model = SentenceTransformer(cfg["embed"]["name"])
    dim = model.get_sentence_embedding_dimension()
    chunks = load_chunks(cfg)

    if not chunks:
        index = faiss.IndexFlatIP(dim)
        faiss.write_index(index, idx_path)
        with open(meta_path, "w") as f: json.dump({}, f)
        return

    texts = [c["text"] for c in chunks]
    embs = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
    xb = np.array(embs, dtype=np.float32)
    index = faiss.IndexFlatIP(xb.shape[1])
    index.add(xb)
    faiss.write_index(index, idx_path)

    meta = {
        str(i): {
            "text": chunks[i]["text"],
            "source": chunks[i]["source"],
            "start": chunks[i]["start"],
            "end": chunks[i]["end"],
        } for i in range(len(chunks))
    }
    with open(meta_path, "w") as f: json.dump(meta, f, ensure_ascii=False)
