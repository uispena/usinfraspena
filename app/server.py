from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import Agent

app = FastAPI(title="KubeAid Agent")
agent = Agent()

class Ask(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/ask")
def ask(body: Ask):
    return {"answer": agent.answer(body.query)}

