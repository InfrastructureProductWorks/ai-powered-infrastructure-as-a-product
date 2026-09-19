# ADR-0006: Establish the IaaP Bootstrap and Foundation Readiness Contract

- **Status:** Accepted
- **Date:** 2026-08-22
- **Issue:** [#139](https://github.com/SAABOLImpactVenture/ai-powered-infrastructure-as-a-product/issues/139)
- **Decision scope:** Public architecture and documentation contract
- **Implementation status:** Target; not asserted as shipped Guard V1, Forge V1, or IaaP Console behavior

## Context

The maintained architecture already establishes this sequence:

```text
external trust prerequisites
→ minimal trusted seed
→ product control plane
→ foundation capabilities as products
→ minimum viable foundation
→ consumer infrastructure products
→ evidence-led evolution
```

The existing thesis, product-control-plane architecture, POCs, and evidence
also establish that:

- repository assessment can begin without customer cloud credentials;
- the minimal trusted seed is not the complete cloud foundation;
- Crossplane is the maintained reference reconciler inside the customer-controlled execution boundary;
- Terraform Enterprise is optional rather than mandatory;
- Composite AI remains proposal-and-evidence-only;
- deterministic controls and authorized people remain authoritative;
- one external resource has one authoritative reconciler;
- live-cloud and production activity require separate evidence and authority;
  and
- Guard V1 and Forge V1 have frozen supported boundaries.

The public architecture did not yet consolidate those facts into a
customer-facing readiness contract. Short phrases such as “DNS
responsibilities,” “workload identity,” or “recovery” did not explain what the
customer must decide, when the requirement becomes mandatory, what evidence is
needed, how AI may assist, or what blocks advancement.

A single large Markdown page would remain difficult to navigate, review,
version, implement, and keep aligned with future validation.

## Decision

The repository will maintain an authoritative
[IaaP Bootstrap and Foundation Readiness](../docs/bootstrap-foundation-readiness/README.md)
documentation package.

The package is an accepted public architecture contract and implementation
target. It does not claim that Guard V1, Forge V1, or the IaaP Console
currently implements the requirements, schema targets, decisions, gates, or
experience described by the package.

### Preserve canonical layers

The package uses these terms:

- **Layer 0 — external trust prerequisites:** customer authority, identity,
  source, audit, connectivity, ownership, and other irreducible dependencies.
- **Customer bootstrap:** the approved environment, prerequisite decisions,
  and operating responsibilities required for the requested IaaP stage.
- **Layer 1 — minimal trusted seed:** the bounded technical subset that
  establishes the Customer Execution Layer runtime, including Crossplane when selected as the reference reconciler.
- **Layer 2 — foundation products:** governed identity, network, logging,
  security, encryption, cost, recovery, and environment capabilities.
- **Minimum viable foundation:** the smallest approved combination needed for
  a defined consumer-product portfolio and risk boundary.

The customer bootstrap is broader than the technical seed. Neither is
represented as a complete enterprise landing zone.

### Preserve the bootstrap-independent assessment path

Repository assessment and planning remain available without requiring:

- customer cloud credentials;
- Kubernetes;
- Crossplane;
- Terraform or TFE credentials;
- AI;
- a customer personal access token;
- repository-code execution;
- merge authority; or
- infrastructure provisioning authority.

Customer-hosted advisory, simulation, discovery, and provisioning are
independently gated capabilities. They must not be converted into prerequisites
for Guard's supported assessment boundary.

### Adopt customer-hosted deployment as the target

The package defines a customer-hosted target for the IaaP management
experience, bounded advisory services, evidence, configuration, product state,
and the separately controlled execution runtime needed for the requested stage.

Customer-hosted means the customer approves and controls hosting, identity,
data custody, external integrations, operations, recovery, export, and
decommissioning. It does not require every approved external service to run on
customer-owned hardware.

The target does not claim a currently available customer-hosted distribution
of Guard V1, Forge V1, or the Console.

### Adopt stable public requirement identifiers

Detailed pages use `BFR-*` requirement identifiers.

These identifiers:

- make prose, future schemas, evidence, tests, and Console help refer to the
  same public requirement;
- are documentation identifiers, not shipped Guard rule or diagnostic codes;
- do not disclose or mirror private scoring, materiality, prompt, fixture, or
  evaluation logic; and
- require separate product compatibility work before runtime enforcement is
  claimed.

### Adopt a stage-specific readiness decision

The public architecture defines `FoundationReadinessDecision` with:

- `CONTINUE`;
- `CONTINUE_WITH_CONDITIONS`; and
- `STOP`.

The decision always applies to a named scope and requested gate. Passing one
gate does not authorize a later gate.

These values are distinct from Guard V1 verdicts and supported decision
semantics. They do not declare compliance, certification, an assessment
conclusion, an authorization to operate, pilot approval, or production
approval.

### Adopt seven readiness gates

The package defines:

0. intake;
1. assessment;
2. credential-free simulation;
3. read-only discovery;
4. live sandbox;
5. pilot; and
6. production consideration.

The gates progressively add evidence and authority. Cloud access advances from
none, to read only, to narrowly bounded nonproduction write only after the
applicable prerequisites and human decisions.

The customer may stop at an earlier stable outcome.

### Preserve the authority model

The fixed authority rule remains:

> Composite AI proposes and explains. Deterministic controls validate.
> Authorized people approve. The product control plane binds authenticated execution authority.
> The Customer Execution Layer reconciles exact authorized effects. Cloud-native
> controls enforce the final boundary.

Composite AI may support discovery, design, review, explanation, diagnosis,
planning, and evidence assembly. It cannot approve, merge, deploy, grant
privileges, accept risk, create undocumented exceptions, or declare compliance
or authorization.

### Use linked detailed pages

Every summarized prerequisite, domain, gate, decision, evidence category,
provider profile, schema target, and responsibility matrix links to a dedicated
Markdown page or a deliberately consolidated detailed page.

Detailed pages use a consistent structure:

1. requirement;
2. purpose and applicability;
3. customer decisions;
4. minimum acceptable state;
5. acceptable pattern categories;
6. Composite AI assistance;
7. deterministic validation target;
8. human approval;
9. required evidence;
10. readiness behavior;
11. future product handoff;
12. exceptions and expiration;
13. prohibited shortcuts; and
14. related requirements.

### Keep the public package provider neutral

The public contract defines common consumer outcomes and decision semantics.
AWS, Azure, and GCP profiles may explain provider-specific questions and
pattern categories without:

- pretending the providers are identical;
- binding the consumer contract to provider topology;
- claiming a public POC implementation that does not exist;
- publishing private implementation details; or
- allowing two systems to co-manage the same resource.

### Enforce the publication boundary

The package follows
[Public Publication Boundary](../docs/PUBLICATION-BOUNDARY.md).

It may publish:

- product and responsibility boundaries;
- customer decisions and required outcomes;
- high-level trust and authority models;
- deliberately public interface and schema targets;
- provider-neutral guidance;
- sanitized evidence categories; and
- limitations necessary to interpret public claims.

It must not newly publish:

- private repository revisions or branch coordinates;
- internal algorithms, rules, scoring, materiality logic, prompts, role
  mechanics, fixtures, or evaluations;
- credentials, secrets, private IAM policies, live resource names, deployment
  topology, workflow identifiers, or raw operational output;
- entitlement, pricing, acquisition, or unreleased commercial mechanics;
- customer or confidential third-party data; or
- details that make private implementation reconstruction easier when a
  high-level requirement is sufficient.

## Compatibility with accepted decisions

This decision extends documentation without superseding:

- [ADR-0002](ADR-0002-product-control-plane.md), which places the stable product
  contract and Crossplane reference implementation at the strategic center; this decision's later Customer Execution Layer clarification supersedes only older wording that could be read as placing provider credentials or reconciliation authority in the product plane;
- [ADR-0004](ADR-0004-tfe-optional-for-multicloud-foundation.md), which keeps
  TFE optional and records the minimal-seed and authority guardrails; or
- [ADR-0005](ADR-0005-supersede-legacy-implementation-stack.md), which prevents
  the public architecture repository from accumulating superseded
  implementation stacks.

Runtime implementation remains in bounded product or POC repositories rather
than being duplicated in this public architecture hub.

## Consequences

### Positive

- Customers receive a navigable definition of what “foundation ready” means.
- Assessment can start before a complete landing zone or cloud credential path
  exists.
- Composite AI advisory has a useful but bounded role.
- Every stage identifies customer decisions, evidence, and authority.
- Provider advisory can integrate without becoming the IaaP product model.
- Public requirements can later align documentation, schemas, tests, evidence,
  and Console guidance.
- Frozen V1 product boundaries remain explicit.
- Public explanation improves without requiring private implementation
  disclosure.

### Tradeoffs

- The documentation package is substantial and must be maintained as one
  versioned system.
- Public requirement identifiers require compatibility discipline.
- Provider profiles must evolve as provider capabilities change.
- Documentation acceptance does not deliver runtime enforcement.
- Future Guard, Forge, and Console adoption requires separate protected product
  decisions, tests, evidence, and versioning.
- The customer must still assign accountable human owners and cannot delegate
  organizational risk decisions to AI.

## Alternatives considered

### Require a complete landing zone before IaaP assessment

Rejected because repository assessment and planning do not require cloud
credentials, and the product-led architecture intentionally allows foundation
capabilities to be established incrementally.

### Let Composite AI design and deploy the foundation autonomously

Rejected because it collapses proposal, validation, approval, execution, and
enforcement authority and creates unacceptable identity, evidence, and risk
boundaries.

### Add the new decisions directly to Guard V1

Rejected because Guard V1 is frozen and this documentation decision does not
establish a compatibility requirement or accepted product implementation.

### Publish one large checklist

Rejected because short checklist entries do not provide applicability,
decision, evidence, exception, AI, human-review, or product-handoff guidance
and would be difficult to navigate and maintain.

### Publish provider-specific implementation blueprints

Rejected because the public architecture should preserve stable
provider-neutral contracts and avoid exposing private implementation details.

### Treat hyperscaler advisory as the complete IaaP operating model

Rejected because cloud-provider advisory can help establish provider
capabilities but does not replace customer product ownership, cross-provider
contracts, IaaP authority separation, lifecycle, or evidence continuity.

## What this decision does not authorize

This ADR does not:

- change Guard V1 or Forge V1;
- claim a shipped IaaP Console workflow;
- enable cloud discovery or provisioning;
- create credentials or infrastructure;
- approve a pilot or production workload;
- declare production readiness;
- validate Terraform Enterprise;
- determine compliance, certification, assessment sufficiency, or ATO;
- make a licensing, ownership, pricing, or commercial decision; or
- permit publication of private product internals.

## Validation

The documentation change is accepted only when:

- all package links resolve;
- the package renders through the repository's strict MkDocs build;
- Mermaid diagrams render without HTML labels;
- every summarized requirement has linked detail;
- `BFR-*` identifiers remain distinct from shipped product codes;
- Guard V1 and Forge V1 boundaries are explicit;
- provider guidance does not overclaim implementation coverage;
- the public publication boundary is preserved; and
- no runtime, credential, cloud-resource, or production claim is inferred from
  documentation alone.

Future implementation claims require evidence from the corresponding protected
product repository and a separate accepted change.
