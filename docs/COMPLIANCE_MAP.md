# HelixCare Compliance and Trust Map

## HIPAA-Oriented Controls

| Risk | Control |
|---|---|
| Excess PHI in prompts | PHI scope declaration in A2A envelopes |
| PHI in logs | Redaction before logging; prompt logging disabled or sanitized |
| Unauthorized access | OIDC service auth + OPA ABAC policies |
| Untraceable decisions | Audit ledger with model, prompt, sources, task id |
| Hallucinated policy answer | RAG citation requirement + refusal threshold |
| Unsafe automation | Human review for adverse or high-risk actions |

This demo does not claim regulatory compliance. It demonstrates design patterns useful for benefit transparency, auditability, reproducibility, and source-grounded explanations.
