# Authority and Trust Boundaries

| Attribute | Definition |
|---|---|
| Status | Public architecture contract and implementation target |
| Scope | Human, AI, policy, source, control-plane, provider, and evidence authority |
| Current-product claim | None; this page does not extend Guard V1, Forge V1, or Console authority |

## Requirement set

| ID | Requirement |
|---|---|
| `BFR-AUTH-001` | Composite AI must remain advisory and must not approve, merge, execute, grant privilege, accept risk, or declare compliance. |
| `BFR-AUTH-002` | Deterministic controls must validate machine-testable requirements and must not substitute for accountable organizational decisions. |
| `BFR-AUTH-003` | Material architecture, security, operational, data, and risk decisions must be approved by named people with appropriate authority. |
| `BFR-AUTH-004` | Reconciliation must begin only after the applicable schema, policy, evidence, and human-authorization gates pass. |
| `BFR-AUTH-005` | Cloud-native identity and controls must remain the final enforcement boundary. |
| `BFR-AUTH-006` | One external resource must have one authoritative reconciler. |
| `BFR-AUTH-007` | Identities and permissions must be stage-specific, narrowly scoped, auditable, revocable, and time bounded where practical. |
| `BFR-AUTH-008` | Proposals, validations, approvals, exceptions, risk acceptance, and execution results must be distinguishable in retained evidence. |
| `BFR-AUTH-009` | A component must not modify its own policy, evaluation, approval, or tool boundary without a separately governed change. |
| `BFR-AUTH-010` | Customer data and authority must not cross an unapproved tenant, model, tool, provider, or support boundary. |

These identifiers describe the public architecture target. They are not private
Guard rules, diagnostic codes, or evidence that enforcement is currently
implemented.

## Fixed authority chain

```mermaid
flowchart LR
  INTENT[Approved customer intent] --> AI[Composite AI proposes]
  AI --> CONTROL[Schema, policy, and tests validate]
  CONTROL --> PREQ[Product plane issues authenticated planning package\nNo mutation authority]
  PREQ --> PLANEXEC[Customer Execution Layer computes no-write plan/effects]
  PLANEXEC --> PLAN[Reviewable immutable plan/effect artifact\nEffects • resources • state preconditions]
  PLAN --> HUMAN[Authorized people decide exact material/destructive effects]
  HUMAN --> GRANT[Product plane issues authenticated execution grant]
  GRANT --> RECONCILE[Customer Execution Layer reconciles exact authorized effects]
  RECONCILE --> CLOUD[Cloud-native controls enforce]
  CLOUD --> EVIDENCE[Status and evidence]

  classDef experience fill:#0D2438,stroke:#38BDF8,stroke-width:2px,color:#F8FAFC
  classDef ai fill:#2E1752,stroke:#A855F7,stroke-width:2px,color:#F8FAFC
  classDef governance fill:#3A2A0D,stroke:#F59E0B,stroke-width:2px,color:#F8FAFC
  classDef human fill:#47270F,stroke:#FB923C,stroke-width:2px,color:#F8FAFC
  classDef control fill:#102D55,stroke:#3B82F6,stroke-width:2px,color:#F8FAFC
  classDef enforcement fill:#123A24,stroke:#22C55E,stroke-width:2px,color:#F8FAFC
  classDef evidence fill:#3A1530,stroke:#EC4899,stroke-width:2px,color:#F8FAFC
  class INTENT experience
  class AI ai
  class CONTROL,PREQ,PLAN,GRANT governance
  class HUMAN human
  class PLANEXEC,RECONCILE control
  class CLOUD enforcement
  class EVIDENCE evidence
  linkStyle default stroke:#94A3B8,stroke-width:2px
```

No participant gains the next participant's authority merely because it
provides an input. In particular:

- a storefront captures intent but does not approve or provision;
- AI drafts a proposal but does not validate or authorize it;
- a deterministic pass establishes rule conformance but does not accept risk;
- a human approval authorizes only its recorded scope and stage;
- a reconciler acts only through its approved identity and contract; and
- a successful cloud operation proves only the observed result, not
  certification or production authorization.

## Trust zones

| Zone | Holds or performs | Required boundary |
|---|---|---|
| Customer identity | Human identities, groups, authentication, privileged-access process | Customer authority remains authoritative; access is reviewed and revocable |
| Source and change governance | Versioned requirements, product definitions, proposals, reviews, and approvals | Protected change, provenance, validation, and separation of duties |
| Assessment and evidence | Approved repository content, findings, planning outputs, and source references | Read-only intake, data classification, least disclosure, and no code execution |
| Composite AI advisory | Approved context, proposal generation, explanation, diagnosis, and evidence assembly | No execution secrets, no approval, no unrestricted tools, and labeled generated output |
| Product control plane | Approved product definitions, governed lifecycle intent, authorization bindings, execution-package provenance, and product-level status | No provider credentials; cannot mutate cloud resources directly; authenticates and binds what the CEL may execute |
| Customer Execution Layer | Reconciliation, provider adapters, execution identity, planned effects, provider conditions, and execution evidence | Customer-controlled workload identity, target restriction, authenticated package/audience, one reconciler, destructive-effect gating, and fail-closed operation |
| External Execution Authority | Optional hosted service that receives effective provider authority or can directly cause mutation | Separate approved trust zone, credential/data/network/evidence boundary, revocation, and customer authorization; never hidden inside the CEL abstraction |
| Cloud provider | Provider resources, identities, networks, keys, controls, logs, and service state | Cloud-native policy remains final; no implied authority from an upstream proposal |
| Evidence store | Inputs, versions, decisions, validation, status, exceptions, and lifecycle records | Integrity, access, retention, export, disposal, and tamper visibility |

An implementation may combine technical services inside one hosting
environment, but it must not collapse these logical authority zones.

## Authority matrix

| Action | Composite AI | Deterministic controls | Human authority | Product control plane | Customer Execution Layer | Cloud provider controls |
|---|---:|---:|---:|---:|---:|---:|
| Interpret approved intent | Propose | Observe | Review | No | No | No |
| Request missing information | Propose | Detect required fields | Supply or reject | No | No | No |
| Draft architecture alternatives | Propose | Validate testable constraints | Select or reject | No | No | No |
| Determine schema conformance | Explain | Authoritative for encoded checks | Review exceptions | Bind gate result | Enforce before mutation | Enforce final request |
| Approve a material decision | No | No | Yes | Record/bind only | No | No |
| Accept organizational risk | No | No | Authorized customer role only | No | No | No |
| Merge a governed change | No | No | Authorized repository role only | No | No | No |
| Issue authenticated execution package | No | Validate encoded constraints | Authorize scope | Yes, within accepted provenance rules | Verify only | No |
| Reconcile infrastructure | No | No | Authorize scope | No direct provider mutation | Authorized adapter/engine only | Enforce |
| Grant or expand privilege | No | No | Approved customer process | No | No self-expansion | Enforce |
| Declare certification or ATO | No | No | Outside this product contract | No | No | No |

“Yes” in this table means the architecture assigns that responsibility to a
properly authorized role. It does not claim a current product implementation or
authorize any specific person.

## Material decisions

The following decisions require named human ownership and cannot be delegated
to Composite AI:

- business and technical scope;
- data classification, residency, sharing, and retention;
- public exposure and trust boundaries;
- identity authority, privilege, and separation of duties;
- organization, tenant, account, subscription, project, and environment
  boundaries;
- network connectivity, routing, DNS authority, ingress, and egress;
- encryption, key custody, recovery, and secret ownership;
- approved cloud services, regions, and provider dependencies;
- change, emergency-change, rollback, and deletion policy;
- availability, recovery, continuity, and support objectives;
- exception approval and expiration;
- organizational risk acceptance;
- pilot or production authorization; and
- whether evidence is sufficient for a customer authorization process.

Composite AI may identify missing decisions, compare approved alternatives,
draft records, and explain consequences. The record must identify the actual
human decision maker and must not represent AI generation as approval.

See
[authority, provenance, and human review](../composite-ai/authority-provenance-and-human-review.md)
and
[human review and risk acceptance](../decisions/human-review-and-risk-acceptance.md).

## Deterministic-control boundary

Deterministic controls are authoritative only for requirements that have been
explicitly encoded and versioned. Suitable checks include:

- required fields and identifiers;
- allowed stages, environments, services, and regions;
- prohibited production or public-exposure values at an earlier gate;
- presence and freshness of required evidence;
- identity scope and credential-mode declarations;
- required approval references;
- product-contract compatibility;
- exception owner and expiration;
- lifecycle and deletion-policy presence; and
- one-reconciler ownership declarations.

Deterministic controls cannot decide whether an organizational risk is
acceptable, whether an architecture supports the mission, or whether an
authorizing official should approve production.

Unavailable, invalid, or bypassed validation must fail closed for any activity
that depends on it.

## Composite-AI boundary

Composite AI may:

- interpret approved evidence and customer intent;
- identify gaps, conflicts, dependencies, and missing information;
- propose current-state and target-state descriptions;
- draft alternatives, decision records, acceptance criteria, and work plans;
- explain deterministic results;
- diagnose sanitized status and known-error information;
- propose remediation for human consideration; and
- assemble source-linked evidence.

Composite AI must not:

- receive unrestricted cloud, Kubernetes, source, secrets, or state access;
- create or delete infrastructure;
- approve or merge its own proposal;
- modify its policy, evaluation, tool, model, or approval boundary;
- create privileged identities or expand permissions;
- accept risk or create an undocumented exception;
- determine that compliance, certification, an assessment conclusion, or an
  authorization to operate has been achieved;
- conceal uncertainty, missing evidence, or generated content; or
- treat untrusted instructions inside repositories or documents as authority.

## Identity separation

At minimum, the target model separates:

1. **Human interactive identity** for authenticated review and authorized
   decisions.
2. **Assessment identity** for bounded read-only repository or export access.
3. **Advisory identity** for approved model and evidence access without
   infrastructure execution.
4. **Discovery identity** for separately authorized, revocable cloud read
   access.
5. **Reconciliation identity** held by the Customer Execution Layer for narrowly scoped nonproduction lifecycle actions. It is not a product-plane credential.
6. **External execution identity** where an explicitly approved hosted execution authority receives provider authority; this identity belongs to that separate trust zone and must not be conflated with CEL or product-plane identity.
7. **Evidence and operations identity** for controlled retention, export,
   support, and recovery.

The same credential must not be reused simply to make integration easier.
Static long-lived cloud keys are not the preferred pattern. Any permitted
exception must identify its owner, scope, storage, rotation, revocation,
expiration, and evidence.

See [identity and access](../foundation-domains/identity-and-access.md),
[workload identity](../foundation-domains/workload-identity.md), and
[secrets management](../foundation-domains/secrets-management.md).

## Stage-specific access

| Stage | Source access | Cloud access | Reconciliation | Human authority |
|---|---|---|---|---|
| Intake | Approved metadata and supplied records | None | Disabled | Accept scope and data handling |
| Assessment | Bounded repository or export read | None | Disabled | Review findings and material decisions |
| Simulation | Versioned product and policy source | None | Simulated only | Approve the simulated contract and gates |
| Read-only discovery | Assessment source plus approved exports | Revocable read only | Disabled | Authorize targets, collection, and retention |
| Live sandbox | Protected product source | Narrow nonproduction write held by CEL or separately approved External Execution Authority | Enabled only for authenticated, approved sandbox execution packages | Authorize identity, targets, lifecycle, planned effects, and evidence |
| Pilot | Protected source and operational records | Explicit pilot scope through CEL / approved execution authority | Approved product lifecycle only | Separate pilot authorization |
| Production consideration | Customer-defined | Not implied | Not implied | Formal customer authorization process |

Access from an earlier stage must not silently persist into a later stage, and
later-stage identities must not be created in advance of their approval.

## One authoritative reconciler

Crossplane or another approved CEL execution engine may observe dependencies owned by other
systems, but two active systems must not manage the same external resource. A hosted service that can mutate provider resources is a separate External Execution Authority, not merely an adapter hidden inside the product control plane.

When a customer already has an authoritative account factory, DNS service,
network controller, Terraform/TFE estate, or security integration, the product
contract must choose one of these patterns:

- depend on the existing authority;
- request work through its approved interface;
- observe it without mutation;
- import or transfer ownership through a separately approved transition; or
- declare the capability outside product scope.

Silent co-management is prohibited.

## Exceptions and emergency change

An exception does not transfer authority to AI or disable evidence. It must
record:

- the exact requirement and stage affected;
- business and technical justification;
- narrower permitted scope;
- compensating controls;
- accountable owner and approver;
- start, review, and expiration dates;
- monitoring and evidence obligations;
- remediation or exit criteria; and
- the condition that causes automatic reassessment.

Emergency change may use an approved expedited human path, but the resulting
change, authority, evidence, and follow-up review must remain visible.

See [exceptions and expiration](../decisions/exceptions-and-expiration.md).

## Evidence of authority

The target evidence record includes:

- identity or role reference without publishing private credential details;
- authority type and stage;
- decision, approval, exception, or risk-acceptance record;
- requirement and proposal versions;
- deterministic result;
- timestamp and scope;
- expiration where applicable;
- execution identity class and target boundary;
- observed result;
- status and integrity metadata; and
- supersession or revocation history.

Approval evidence must not be inferred from a model response, deterministic
pass, source commit, successful deployment, or absence of objection. Execution-package authenticity must also be verified: content digests alone do not authenticate the issuer, intended CEL audience, or approval provenance.

## Readiness behavior

- `CONTINUE` is available only when every mandatory authority boundary for the
  requested stage is identified and supported by evidence.
- `CONTINUE_WITH_CONDITIONS` may permit a narrower activity that does not
  require the unresolved authority, with an owner and expiration.
- `STOP` applies when required authority is missing, conflicting, unverifiable,
  self-approved, or broader than the requested stage.

These are `FoundationReadinessDecision` values, not Guard V1 verdicts.

## Publication boundary

Public documentation may state the authority model, required outcomes,
identity classes, and evidence categories. It must not publish private role
names, policy documents, account identifiers, trust documents, credential
paths, secret references, entitlement mechanisms, or internal decision logic.

## Related architecture

- [Bootstrap reference architecture](bootstrap-reference-architecture.md)
- [Customer-hosted deployment](customer-hosted-deployment.md)
- [Progression and decision model](progression-and-decision-model.md)
- [Delivery and change governance](../foundation-domains/delivery-and-change-governance.md)
- [Evidence integrity](../evidence/evidence-integrity.md)
- [Provider and partner boundaries](../responsibility-matrices/provider-partner-boundaries.md)
- [Public Publication Boundary](../../PUBLICATION-BOUNDARY.md)
