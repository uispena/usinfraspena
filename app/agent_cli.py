import typer
from app.agent import Agent

app = typer.Typer()
agent = Agent()

@app.command()
def ask(q: str):
    print(agent.answer(q))

if __name__ == "__main__":
    app()

