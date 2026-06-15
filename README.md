# HelixCare — Agentic Healthcare Operations Platform

HelixCare is an architecture, spec, and reference implementation for a secure multi-agent
healthcare operations platform.

It demonstrates:
- Agent-to-Agent (A2A) task delegation and negotiation
- MCP-style context providers for persistent, grounded LLM interactions
- RAG over structured and unstructured healthcare data
- Prior authorization, eligibility, provider matching, summarization, and member engagement flows
- Explainability via Why Cards
- HIPAA-aware audit, access control, observability, and MLOps patterns

Demo/specification only. Do not use for clinical or coverage decisions without formal
compliance, validation, legal review, and operational controls.

## Repository layout

```
docs/, adrs/, schemas/, api/, prompts/   Architecture, ADRs, JSON schemas, OpenAPI spec
examples/                                Sample A2A envelope and message format
app/                                     Reference implementation (LlamaIndex agents, RAG, UI)
data/                                    Synthetic policy docs, FHIR coverage, code tables
docker/                                  Docker Compose stack: Streamlit + Prometheus + Grafana
eval/                                    Evaluation harness and test cases
tests/                                   Tests (RAG retrieval, agent integration)
training/                                QLoRA fine-tuning scripts for a domain helper model
infra/                                   Reference compose for the target production agent bus
```

## Reference implementation: CareGraph

The `app/` directory contains a working multi-agent implementation built on **LlamaIndex**,
covering the MRI prior-authorization MVP flow described in
[docs/HELIXCARE_SPEC.md](docs/HELIXCARE_SPEC.md):

- Role-specialized agents: Eligibility, PriorAuth, Provider, Summarizer (`app/agents/`)
- Hybrid RAG over plan policy documents (`app/rag/`)
- Tool use for ICD-10/CPT lookups, mock FHIR coverage, and provider directory (`app/tools/`)
- Explainability via a "Why Card" JSON (see [schemas/why_card.schema.json](schemas/why_card.schema.json))
- Local LLM (llama.cpp GGUF) or OpenAI fallback (`app/llm.py`)
- Prometheus metrics + Grafana dashboard
- Streamlit demo UI (`app/ui.py`)

### Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r docker/requirements.txt

# (Optional) Use a local GGUF model:
export LLAMA_CPP_MODEL_PATH=./models/<your-model>.gguf
# Otherwise the app falls back to OpenAI and requires:
export OPENAI_API_KEY=sk-...

streamlit run app/ui.py
```

Open http://localhost:8501, use member **M123**, modality **MRI**, symptom
**"low back pain"**, and click **Run Prior-Auth Flow**.

### Run with Docker Compose

```bash
docker compose -f docker/docker-compose.yml up --build
```

- UI: http://localhost:8501
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default creds admin/admin)

### Evaluate and test

```bash
python eval/eval_runner.py
python tests/test_rag.py
```

### Fine-tune a small helper model (QLoRA)

```bash
pip install -r docker/requirements.txt  # includes transformers/trl/peft/bitsandbytes
python training/train_qlora.py
python training/infer_with_adapter.py
```

## Notes

- All data is synthetic and safe to publish.
- This is a demo; do not use for clinical or coverage decisions.
- See [docs/COMPLIANCE_MAP.md](docs/COMPLIANCE_MAP.md) for HIPAA-oriented design patterns and
  [docs/JIRA_EPICS.md](docs/JIRA_EPICS.md) for the production work breakdown.

## License & Citation

MIT License — Copyright (c) 2026 Aga Jaron / SciComp Qlab LLC. See [LICENSE](LICENSE) and
[CITATION.cff](CITATION.cff).
