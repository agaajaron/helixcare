# ADR-001: Use A2A Typed Envelopes and MCP-Style Context

## Status
Accepted for MVP.

## Context
Healthcare workflows require traceable delegation, minimal PHI access, and source-grounded answers.

## Decision
Agents communicate through JSON A2A envelopes. Context is accessed through named MCP-style providers rather than arbitrary prompt stuffing.

## Consequences
Positive: easier audit, stronger access control, better testability, cleaner agent responsibilities.
Negative: more schema work, orchestration latency, disciplined source management required.
