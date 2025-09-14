import glob, os
def load_chunks(cfg: dict):
    globs = cfg["rag"].get("file_glob", [])
    size = int(cfg["rag"].get("chunk_size", 900))
    overlap = int(cfg["rag"].get("chunk_overlap", 150))
    files = []
    for g in globs: files += glob.glob(g, recursive=True)
    chunks = []
    for path in files:
        try:
            with open(path, "r", errors="ignore") as f:
                text = f.read()
        except Exception:
            continue
        start = 0
        L = len(text)
        while start < L:
            end = min(L, start + size)
            chunks.append({"text": text[start:end], "source": path, "start": start, "end": end})
            if end == L: break
            start = max(0, end - overlap)
    return chunks
