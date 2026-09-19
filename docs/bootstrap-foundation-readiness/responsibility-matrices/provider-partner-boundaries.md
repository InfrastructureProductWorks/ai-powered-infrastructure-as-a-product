# Cloud-provider and implementation-partner boundaries

**Requirement ID:** `BFR-RSP-003`

> **Status:** Architecture target. The POCs demonstrate a provider-neutral product boundary and limited AWS/GCP implementations, but they do not establish a customer/provider/partner advisory contract or transfer customer accountability.

## Principle

> A cloud provider or partner may help establish the runway. The customer owns its architecture, data, operations, and risk. IaaP evaluates the product-readiness boundary and governs approved infrastructure products.

Cloud-foundation advisory is therefore an enabling workstream, not an undocumented prerequisite and not a substitute for customer decisions.

## Responsibility boundary

| Responsibility | Customer | Cloud-provider advisory | Implementation partner | IaaP products/workflow |
|---|---|---|---|---|
| Business outcome and risk appetite | A/R | C | C | I |
| Foundation scope and authoritative decisions | A/R | C | C | assessment support |
| Provider reference patterns and service guidance | A | R/C | C | consume as versioned input |
| Customer-specific target architecture | A | C | R when contracted | propose/trace, never self-approve |
| Landing-zone or foundation implementation | A | C/R when contracted | R when contracted | not assumed by Guard/Console |
| Product-readiness assessment | A | C | C | R within approved boundary |
| Infrastructure-product contract | A | C | C/R when contracted | governed product workflow |
| Provider-specific adapter implementation | A | C | R when contracted | Forge/adapter handoff only after approval |
| Human approval and risk acceptance | A/R customer authority | I/C | I/C | prohibited authority |
| Cloud execution | A | provider platform supplies APIs | R only when authorized | Customer Execution Layer or separately approved External Execution Authority executes only the authenticated, plan-bound effects; product plane holds no provider credential |
| Operations, incident, backup, and cost | A | provider shared-responsibility inputs | R when contracted | evidence/status integration only |
| Production authorization | A/R customer authority | C | C | cannot authorize |

`A`, `R`, `C`, and `I` follow the [bootstrap RACI](bootstrap-raci.md). Contract language may change who is responsible, but not silently transfer customer accountability.

## Supported engagement patterns

### Customer brings an existing foundation

IaaP assesses documented and observed interfaces, identifies gaps, and consumes only the approved attachment contract. Passing provider assessments or badges do not automatically establish product readiness.

### Provider or partner remediates an incomplete foundation

The readiness assessment supplies requirements, evidence gaps, acceptance criteria, and decision owners. The provider/partner proposes and implements within its contract. Customer domain owners approve; IaaP re-evaluates the resulting evidence.

### Narrow minimum viable bootstrap

The customer may authorize a bounded nonproduction bootstrap for assessment and simulation while enterprise foundation work continues. Live provisioning remains gated by every required attachment and owner.

### IaaP-aligned implementation partner

A partner may implement provider adapters or foundation capabilities as products. The stable consumer contract, authority separation, evidence model, and one-engine-per-resource rule still apply.

## Required advisory deliverables

Provider or partner work used by a readiness decision should produce:

- scope, assumptions, exclusions, and customer decisions required;
- current-state sources and collection dates;
- target architecture and responsibility split;
- provider-specific control and service mappings;
- implementation backlog and acceptance tests;
- identity, network, DNS, logging, encryption, operations, recovery, and cost interfaces;
- unresolved limitations and exceptions;
- implementation revisions and observed evidence; and
- customer approvals and operational handoff.

Slideware alone is insufficient for a live gate.

## Composite AI role

Composite AI may compare advisory deliverables with BFR requirements, identify conflicting assumptions, draft questions, map evidence, and propose acceptance criteria. It may not select the provider/partner, accept contractual terms, approve architecture, or treat vendor statements as observed customer evidence.

## Decision behavior

- `CONTINUE`: provider/partner deliverables and implemented interfaces meet the exact requested gate and customer approvals.
- `CONTINUE_WITH_CONDITIONS`: advisory/design work or a narrower bootstrap may continue while live dependencies remain blocked.
- `STOP`: responsibility is ambiguous, vendor claims substitute for evidence, the customer lacks accountable owners, or a partner is expected to accept customer risk.

## Related requirements

- [Provider-neutral contract](../providers/provider-neutral-contract.md)
- [AWS profile](../providers/aws-foundation-profile.md)
- [Azure profile](../providers/azure-foundation-profile.md)
- [GCP profile](../providers/gcp-foundation-profile.md)
- [Gate 1 — assessment](../readiness-gates/gate-1-assessment.md)
