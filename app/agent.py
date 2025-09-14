import os, yaml
from app.graph import Graph
from app.prompts import SYSTEM_PROMPT
from app.toolbus import ToolBus

class Agent:
    def __init__(self):
        with open("config.yaml","r") as f:
            self.cfg = yaml.safe_load(f)
        self.graph = Graph(self.cfg)
        self.tools = ToolBus(self.cfg)

    def answer(self, query: str) -> str:
        # Retrieve context
        ctx = self.graph.retrieve(query, k=6)
        # Toolhead: simple tool trigger examples
        tool_context = self.tools.autorun(query)

        prompt = f"{SYSTEM_PROMPT}\n\n# Context\n{ctx}\n\n# Tool Output\n{tool_context}\n\n# Question\n{query}\n\n# Answer:"
        return self.graph.llm_generate(prompt)

