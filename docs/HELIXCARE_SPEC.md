# HelixCare Lightweight Spec v0.2

## Purpose

HelixCare is a secure, explainable, multi-agent platform for healthcare operations. It supports eligibility checks, prior authorization guidance, provider matching, clinical summarization, benefits support, and member engagement.

## Core Agents

- MemberEngagementAgent: interprets member requests and routes intent.
- EligibilityAgent: retrieves coverage, benefit status, deductible, and out-of-pocket information.
- PriorAuthAgent: determines whether prior authorization may be required and identifies missing criteria.
- ProviderMatchAgent: finds in-network providers based on modality, location, plan, and preferences.
- ClaimsAgent: validates basic claim metadata and flags likely missing information.
- ClinicalSummarizerAgent: summarizes notes into policy-relevant evidence.
- ComplianceAgent: checks PHI minimization, source grounding, and response constraints.
- OrchestratorAgent: decomposes goals, delegates tasks, handles retries, and assembles final response.

## MVP Flow: MRI Prior Authorization

1. MemberEngagementAgent classifies intent as prior_auth_check.
2. Orchestrator creates a task plan.
3. EligibilityAgent retrieves plan and coverage.
4. PriorAuthAgent retrieves plan rules and relevant CPT/ICD rules.
5. ClinicalSummarizerAgent extracts evidence from notes.
6. ProviderMatchAgent finds in-network imaging providers.
7. ComplianceAgent checks citations and PHI scope.
8. Orchestrator returns a member-friendly answer plus Why Card.

## Acceptance Criteria

- Prior-auth flow runs end-to-end on synthetic data.
- Final response includes Why Card JSON.
- Every rule-based assertion includes a source id and span.
- PHI fields are declared in the A2A envelope.
- Prometheus-style metrics are emitted.
- Audit event is written for each task.
