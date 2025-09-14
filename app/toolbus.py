import subprocess, shlex, re, yaml

class ToolBus:
    def __init__(self, cfg):
        self.cfg = cfg
        self.kubectl = cfg["tools"]["kubectl_path"]
        self.journalctl = cfg["tools"]["journalctl_path"]

    def _run(self, cmd: str) -> str:
        try:
            out = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT, timeout=10)
            return out.decode("utf-8", "ignore")
        except Exception as e:
            return f"[tool-error] {e}"

    def autorun(self, query: str) -> str:
        q = query.lower()
        if "taint" in q and "node" in q:
            return self._run(f"{self.kubectl} get nodes -o json | jq -r '.items[] | \"\\(.metadata.name): \\(.spec.taints)\"'")
        if "pod logs" in q or "logs" in q:
            return self._run(f"{self.kubectl} get pods -A --no-headers | head -n 10")
        if "events" in q:
            return self._run(f"{self.kubectl} get events -A --sort-by=.lastTimestamp | tail -n 20")
        if "journal" in q or "kubelet" in q:
            return self._run(f"sudo {self.journalctl} -u kubelet -n 100 --no-pager")
        return ""

