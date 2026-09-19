# ADR-0002: Product Contract and Reconciliation Are the Strategic Center

- **Status:** Accepted
- **Date:** 2026-08-06

## Decision

The strategic infrastructure architecture is centered on:

```text
consumer intent
→ bounded composite AI
→ GitHub proposal, deterministic validation, and human approval
→ stable infrastructure product API
→ authenticated execution authority
→ Customer Execution Layer
→ Crossplane or another approved reconciler
→ cloud-specific implementation
→ product status and evidence
```

The product contract defines consumer outcomes, profiles, required metadata, lifecycle, guarantees, exclusions, status, and versioning.

Crossplane is the maintained reference reconciler for the reference POCs where provider coverage and lifecycle behavior are sufficient. Provider mutation authority belongs to the separately governed Customer Execution Layer, not to the product plane itself. Crossplane may write only for the finite, authenticated execution session currently authorized by that layer; later drift-driven writes require a fresh plan and execution grant.

Composite AI may interpret intent, draft proposals, explain policy, diagnose sanitized status, and assemble evidence. It may not directly apply/delete infrastructure, approve/merge its own work, read unrestricted secrets/state, create privileged identities, or modify its own policy/tool boundary.

## Consequences

- Consumer contracts are decoupled from implementation topology.
- Foundation capabilities can be established incrementally as products after a minimal trusted seed exists.
- Multi-cloud differences remain behind the contract unless they are a deliberate product choice.
- GitHub and the product plane provide change governance, provenance, and authenticated execution authority, not provider credentials or cloud reconciliation.
- The Customer Execution Layer owns write-capable reconciliation through the selected engine.
- Cloud-native IAM remains the final permission boundary.
- One external resource has one authoritative reconciler.

## Supersession note

The reference implementation no longer carries the previous Terraform, Arc, Backstage, or legacy execution-MCP stack. See `ADR-0005-supersede-legacy-implementation-stack.md`.

The September 2026 Customer Execution Layer architecture clarifies this accepted decision: references in earlier material to "Crossplane product control plane" describe the strategic reconciliation mechanism, not ownership of product-plane credentials or perpetual provider-write authority. The stable product contract remains central; provider mutation occurs only through the customer-controlled execution boundary.
