# HelixCare Architecture

## Components

### Agent Mesh
Typed agent-to-agent communication using NATS, Kafka, or gRPC.

### Orchestrator
Receives user tasks, creates task graphs, selects agents, enforces retries/timeouts, and invokes ComplianceAgent.

### MCP Context Server
Provides stable access to FHIR-like resources, plan rules, provider directories, code systems, interaction memory, and task memory.

### RAG Service
Retrieves grounded context from plan documents, prior-auth policies, ICD-10/CPT references, clinical notes, and chat transcripts.

### Trust and Compliance Layer
Includes access control, audit ledger, redaction, PHI scope enforcement, and hallucination/refusal guardrails.

## Production Shape

Frontend/API Gateway -> Orchestrator -> Agent Bus -> Agent Services -> MCP/RAG/Model Gateway -> Postgres/Vector DB/Object Store/Audit Ledger.
