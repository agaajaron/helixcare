# CareGraph — Multi‑Agent Healthcare RAG (LlamaIndex)

**What it is.** CareGraph is a portfolio‑ready demo that shows how to build a secure, explainable multi‑agent system on top of **LlamaIndex**. It handles a realistic workflow: *“Do I need prior authorization for an MRI?”*

**What it demonstrates.**
- Role‑specialized agents (Eligibility, PriorAuth, Provider, Summarizer) with tool use
- **Hybrid RAG** over structured (ICD‑10/CPT) and unstructured (plan rules, notes)
- **Explainability** via a “Why Card” JSON with citations
- **Local LLM** support (llama.cpp, GGUF) + OpenAI fallback
- **Observability** with Prometheus metrics and a pre‑built Grafana dashboard
- Clean Streamlit UI, Dockerized for one‑command demos

**Why it matters.** It highlights agent orchestration, grounding & compliance patterns that recruiters love to see for real‑world healthcare and enterprise AI.

**Tech stack.** LlamaIndex, HuggingFace embeddings, Streamlit, Prometheus/Grafana, Docker, GitHub Actions.

**Try it.**
```bash
docker run --rm -p 8501:8501 -p 9000:9000 \
  -e LLAMA_CPP_MODEL_PATH=/models/YOUR_MODEL.gguf \
  -v $(pwd)/models:/models \
  ghcr.io/<your-user-or-org>/caregraph:latest
```
Open **http://localhost:8501** and click **Run Prior‑Auth Flow**.
