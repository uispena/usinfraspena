import os, tarfile, glob, re, json
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss, numpy as np

base = os.getcwd()
docs_dir = os.path.join(base, "docs")
bundle = os.path.join(base, "docs-bundle.tar.gz")
out_dir = os.path.join(base, "index")
os.makedirs(out_dir, exist_ok=True)

if os.path.exists(bundle):
    with tarfile.open(bundle, "r:gz") as t:
        t.extractall(docs_dir)

paths = []
for ext in ("*.md","*.txt","*.html","*.htm"):
    paths.extend(glob.glob(os.path.join(docs_dir, "**", ext), recursive=True))

def read_text(p):
    try:
        t = open(p, "r", encoding="utf-8", errors="ignore").read()
        if p.endswith((".html",".htm")):
            return BeautifulSoup(t, "lxml").get_text(" ", strip=True)
        return t
    except Exception:
        return ""

docs = []
for p in paths:
    txt = read_text(p)
    txt = re.sub(r"\s+", " ", txt).strip()
    if len(txt) > 0:
        docs.append({"path": os.path.relpath(p, docs_dir), "text": txt[:40000]})

if not docs:
    with open(os.path.join(out_dir,"meta.json"),"w") as f: json.dump({"docs":0}, f)
    raise SystemExit

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
emb = model.encode([d["text"] for d in docs], batch_size=16, convert_to_numpy=True, show_progress_bar=False, normalize_embeddings=True)
index = faiss.IndexFlatIP(emb.shape[1])
index.add(emb.astype("float32"))
faiss.write_index(index, os.path.join(out_dir, "faiss.index"))
with open(os.path.join(out_dir,"docs.json"),"w") as f: json.dump(docs, f)
with open(os.path.join(out_dir,"meta.json"),"w") as f: json.dump({"docs":len(docs)}, f)
