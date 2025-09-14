import argparse
from app.agent import Agent

def main():
    p = argparse.ArgumentParser(prog="kubeaid", description="Linux & Kubernetes troubleshooting assistant")
    sub = p.add_subparsers(dest="cmd", required=True)

    ask = sub.add_parser("ask", help="Ask a question (returns detailed steps/commands)")
    ask.add_argument("question", nargs="+", help="Your question")

    args = p.parse_args()
    agent = Agent()

    if args.cmd == "ask":
        q = " ".join(args.question)
        print(agent.answer(q))

if __name__ == "__main__":
    main()
