# Composite AI authority, provenance, and human review

**Requirement IDs:** `BFR-AI-020` through `BFR-AI-029`

## Requirement

The customer must be able to distinguish source evidence, AI interpretation, deterministic validation, human authorization, and execution evidence. Those records must not be collapsed into one undifferentiated result.

## Authority separation

| Layer | May do | Must not do |
|---|---|---|
| Composite AI | interpret, propose, explain, summarize | approve, execute, accept risk |
| Deterministic policy | test explicit rules and schemas | infer organizational intent or waive failure |
| Human authority | authorize material decisions within assigned responsibility | hide or silently override failed controls |
| Product control plane | bind approved intent, provenance, exact plan/effects, and authenticated execution grants | hold provider credentials, reconcile cloud resources, redefine intent, or manufacture approval |
| Customer Execution Layer / approved External Execution Authority | reconcile only the exact currently authorized plan/effects | self-approve, silently re-plan/widen effects, or retain write authority after grant completion/expiry/revocation |
| Cloud control | enforce provider configuration | represent customer governance by itself |

## Provenance chain

Each retained result should link:

```text
source evidence
  → AI proposal and assumptions
  → deterministic validation
  → protected desired-state revision
  → authenticated planning package with no mutation authority
  → reviewable no-write plan/effect artifact and provider-state preconditions
  → named human disposition over the exact material/destructive effects
  → authenticated execution/delegation grant bound to that artifact
  → execution and authenticated operational evidence
```

The record must make later edits, superseded proposals, expired approvals, and incomplete evidence visible.

## Human review requirements

Material decisions require reviewers appropriate to the subject. Examples include:

- architecture authority for trust boundaries and integration patterns;
- security authority for privilege, exposure, encryption, and event handling;
- data owner for classification and model use;
- operations owner for support, recovery, and incident response;
- financial owner for budgets and lifecycle cost; and
- risk authority for an explicitly documented exception.

One person may hold more than one role only when the customer permits it and the resulting separation-of-duties risk is recorded.

## Deterministic validation target

Validation should verify that a proposal identifies its sources and assumptions, required reviewer roles are populated, the protected desired-state revision is exact, the reviewable no-write plan/effect artifact (or authenticated retrievable reference) was available to the reviewer before approval, approval has not expired, the human decision binds the exact affected resources/effect classes/provider-state preconditions and artifact digest, the final execution grant authenticates those same plan/effect bindings, and the execution record points to the exact authorized grant/attempt rather than merely the desired-state revision.

## Required evidence

- immutable or integrity-protected source references;
- proposal and model-adapter identifiers;
- validation results;
- reviewer identity, role, decision, scope, and time;
- exception and expiration data where applicable;
- authorized revision identity; and
- resulting status/evidence identity.

## FoundationReadinessDecision behavior

- `CONTINUE`: the complete authority and provenance chain exists for the stage.
- `CONTINUE_WITH_CONDITIONS`: non-executing analysis may proceed while a named reviewer or evidence item remains pending.
- `STOP`: execution is requested without valid authorization, provenance cannot be reconstructed, or AI output is represented as human approval.

## Forge handoff

The handoff should contain only an approved, versioned product contract plus authorization and evidence references. Prompts, hidden reasoning, raw secrets, or unapproved alternatives must not become execution input.

## Related requirements

- [Human review and risk acceptance](../decisions/human-review-and-risk-acceptance.md)
- [Evidence integrity](../evidence/evidence-integrity.md)
- [Delivery and change governance](../foundation-domains/delivery-and-change-governance.md)
- [Authority and trust boundaries](../architecture/authority-and-trust-boundaries.md)
