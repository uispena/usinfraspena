KubeAid Offline (Build on asgu00, Deploy on as00)

0) Copy your working kubeaid-agent.pyz into this folder.

1) (Optional) Add docs for offline RAG:
   - Place a tarball at ./docs-bundle.tar.gz   OR
   - Put files under ./docs/  (md, txt, html)

2) Build & push:
   IMAGE=registry/ns/kubeaid:offline-v1 ./build_push.sh
   # Optionally pick a different GGUF model:
   # MODEL_URL=...GGUF IMAGE=... ./build_push.sh

3) Deploy to as00:
   IMAGE=registry/ns/kubeaid:offline-v1 ./deploy.sh

4) Use:
   kubectl exec -it deploy/kubeaid -n kubeaid -- kubeaid-agent chat
