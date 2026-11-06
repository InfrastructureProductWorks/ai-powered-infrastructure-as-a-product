---
name: ipw-architecture-review
description: Use for IPW product architecture reviews, API-first or AI-native consumption changes, MCP interoperability, cloud implementation decisions, or cross-product contracts.
---

# ipw-architecture-review

## Work
1. Identify the customer-facing governed product contract, owner, supported profiles, and stage of the lifecycle; compare current implementation with the proposed outcome.
2. Draw the trust and data boundaries among Storefront, Composite AI, Guard, Console, Forge, Assurance, Adapter/Crossplane/native APIs, and the human approval path. Validate against docs/GOVERNED-AGENTIC-INTEROPERABILITY.md and docs/PRODUCT-ARCHITECTURE.md.
3. Prefer stable consumer/API contracts over leaking Terraform, cloud-specific object shapes, provider workspace, or orchestration details. Compare API-native, Crossplane, Terraform/TFE and hybrid fulfillment on correctness, portability, operations, reversibility, economics and deployment maturity; do not assume API-native is automatically better.
4. Specify failure/denial paths, idempotency, reconciliation, drift, lifecycle/retirement, provenance, compatibility, and rollback.
5. Produce an ADR-level recommendation with alternatives, measurable tradeoffs, migration increments, exact impacted repositories and owners; preserve supported contracts unless verified compatibility acceptance authorizes a change.

## Hard boundary
No MCP, LLM, agent skill or generated plan may self-approve, provision privileged infrastructure, bypass Guard deterministic denial, or expand a human authorization. Do not conflate a conceptual architecture diagram with an implemented runtime.

## Return
Decision, evidence/source revisions, alternative matrix, risk review, testable interface contracts, acceptance gate, and recommended smallest next implementation slice.
