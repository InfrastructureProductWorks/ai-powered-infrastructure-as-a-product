# Government Security Profile for the Customer Execution Layer

**Date:** September 19, 2026  
**Status:** documentation-first security profile  
**Applies to:** Customer Execution Layer, provider adapters, and any External Execution Authority that receives effective provider mutation authority  
**Authority:** design and validation requirements only; this profile does not grant an ATO, cATO, FedRAMP authorization, FISMA authorization, agency approval, or production authority.

## Purpose

This profile defines federal-oriented security expectations for an Infrastructure Product Works Customer Execution Layer and for any separately approved External Execution Authority (EEA) that receives provider credentials or can directly cause provider mutation.

It is intended to help a customer deploy the execution capability inside an environment where federal controls, agency overlays, restricted networking, strong identity, auditable change, supply-chain controls, and assessor evidence matter from the start.

The profile is provider-neutral and may be applied to commercial or government cloud environments where the customer requires these controls.

## Standards posture

The profile is designed to align with the intent of control families commonly used in federal authorization programs, including:

- Access Control (AC)
- Audit and Accountability (AU)
- Assessment, Authorization, and Monitoring (CA)
- Configuration Management (CM)
- Identification and Authentication (IA)
- Incident Response (IR)
- Maintenance (MA)
- Media Protection (MP)
- Physical and Environmental Protection (PE), where inherited from hosting
- Planning (PL)
- Personnel Security (PS), where inherited from organizational process
- PII Processing and Transparency (PT), when applicable
- Risk Assessment (RA)
- System and Services Acquisition (SA)
- System and Communications Protection (SC)
- System and Information Integrity (SI)
- Supply Chain Risk Management (SR)

The profile does not claim that every control is implemented solely by IPW. Many controls are inherited from the customer organization, cloud provider, hosting environment, identity platform, network/security services, CI/CD system, SIEM, key-management service, or operating process.

## Core security principles

The Government Security Profile requires:

1. **customer-controlled execution authority**;
2. **short-lived workload identity** by default;
3. **least privilege and explicit target scoping**;
4. **separation of proposal, approval, execution, and risk acceptance**;
5. **deny-by-default network and API posture**;
6. **approved cryptography and FIPS-capable paths where required**;
7. **immutable or integrity-protected execution evidence**;
8. **version-pinned and provenance-bound software supply chain**;
9. **strict tenant/customer isolation**;
10. **auditable lifecycle and deletion authority**;
11. **fail-closed behavior on missing trust or evidence**; and
12. **revocable authority without disrupting already-running workloads**.

## Execution-authority responsibility mapping

| Requirement area | Customer Execution Layer | External Execution Authority, when used |
|---|---|---|
| Package/grant authentication | Verify trusted issuer, CEL audience, approval provenance, exact plan/effect binding | Verify CEL-issued EEA audience, delegation signature/attestation, parent grant, expiry, replay and revocation state |
| Least privilege | Enforce IPW scope and local workload identity | Enforce only delegated target/effects and its separately approved provider identity |
| Destructive-effect gating | Compute/bind or verify exact plan/effects and require destructive authorization | Execute only the exact delegated saved plan/effects; no re-plan widening |
| Cryptography | Meet the approved profile for CEL transport, storage, signing and evidence | Meet the same applicable approved profile for hosted transport, credential custody, execution and evidence |
| Audit/evidence | Record authorization, delegation, preflight, result and returned evidence | Record provider mutation, identity, API results, retries/failures and return authenticated evidence to CEL |
| Replay/idempotency | Reject replay/conflicting grants and track revocation state | Reject replay/conflicting delegation and duplicate mutation beyond defined idempotency |
| Network/data boundary | Customer-approved ingress/egress, CA, proxy/private endpoint and data handling | Separately approved hosted-service network/data-processing boundary and destinations |
| Incident/revocation | Revoke package/delegation trust and local identity; expose authoritative current revocation state | Check current revocation state or rely on grant-scoped provider identity revocation immediately before each mutation; stop when freshness is unavailable |
| Result authenticity | Verify local engine results and any EEA result envelope | Sign/attest result evidence to exact delegation, plan/effects, attempt identity and provider results |
| Supply chain | Pin/verify CEL adapters and runtime | Pin/verify hosted agent/runtime and disclose/inherit provider service controls as approved |

Controls may be inherited differently between the CEL and an EEA, but no applicable control disappears merely because execution is delegated.

## Control-oriented requirements

### AC — Access Control

The CEL and, where the requirement applies to delegated mutation, the EEA must:

- bind each execution to one customer/tenant and one approved FoundationTarget;
- enforce least privilege at both the cloud IAM layer and the IPW execution-package layer;
- prohibit broad administrator/owner permissions as the default execution role;
- prevent a target-scoped authorization from being reused against another account, subscription, project, region, or environment;
- separate read/discovery permissions from write/execution permissions where practical;
- prohibit execution by Storefront, Console, Guard, Composite AI, and documentation surfaces;
- preserve one authoritative reconciler per resource;
- make deletion and destructive replacement/recreation separately authorized effects, regardless of the outer operation label;
- verify an engine's exact planned-effect set before mutation and fail closed when destructive effects cannot be determined; and
- support immediate revocation of future execution authority.

### IA — Identification and Authentication

The default profile prohibits long-lived cloud keys.

Preferred patterns:

- **AWS:** temporary role credentials via approved federation or EKS Pod Identity;
- **Azure:** Microsoft Entra workload identity federation and/or managed identity;
- **Google Cloud:** Workload Identity Federation, including GKE Workload Identity Federation where appropriate.

Audience validation is role-specific:

**A CEL-local executor must authenticate and bind:**

- trusted execution-package / execution-grant issuer and signing/attestation provenance;
- the exact CEL deployment identity as the intended audience;
- trusted human-decision provenance and approval authority;
- workload principal, customer/tenant, execution adapter, FoundationTarget, allowed effects, and authorization lifetime.

**An External Execution Authority must authenticate and bind:**

- the CEL as the trusted delegation-grant issuer;
- the exact EEA service/agent identity as the intended audience;
- the signed parent execution-grant and planned-effect chain;
- trusted human/destructive-decision provenance carried through that chain;
- its grant-scoped workload/provider principal, customer/tenant, FoundationTarget, allowed effects, and authorization lifetime.

An EEA must reject the original CEL-audience package. A CEL-local executor must reject an EEA-audience delegation grant intended for another authority.

Interactive administrator access to the execution environment requires customer-approved strong authentication and privileged-access controls.

### AU — Audit and Accountability

The CEL must retain the end-to-end evidence chain, and any EEA must emit enough authenticated evidence back to the CEL to reconstruct:

- who or what initiated the operation;
- which human decision authorized it;
- which exact desired-state digest was executed;
- which workload identity performed the operation;
- which provider target was affected;
- which API/action results were observed;
- whether policy/preflight blocked or allowed the action;
- retries and replay attempts;
- rollback/teardown activity;
- residual-state checks; and
- final disposition.

Audit/event collection failure must not be silently treated as successful evidence completion.

The customer defines retention, legal/records obligations, SIEM routing, and protected-data handling.

### CM — Configuration Management

The CEL, and any EEA for the runtime it controls, must:

- pin supported adapter/engine versions;
- verify configuration/profile integrity;
- make execution packages immutable;
- prevent unreviewed configuration drift from silently changing execution semantics;
- record target/profile/adapter revisions with each execution;
- require review when a security-significant execution profile changes; and
- support deterministic comparison between approved and observed configuration.

### CA — Assessment, Authorization, and Monitoring

The profile must produce evidence suitable for customer assessment activities, including:

- control-relevant configuration;
- exact implementation revision;
- test results;
- negative/denial results;
- identity bindings;
- network restrictions;
- cryptographic posture;
- operational/audit evidence;
- change/approval references;
- residual gaps; and
- inherited-control declarations.

A passing IPW test is never itself an authorization decision.

### SC — System and Communications Protection

The default network posture must:

- avoid unsolicited public inbound access to the executor;
- use customer-controlled boundary protections;
- support explicit egress allowlists;
- support proxies and inspection where required;
- support customer/private CA trust;
- prefer private provider endpoints where the customer architecture requires them;
- support environment-specific endpoints for government cloud partitions;
- protect data in transit using customer-approved TLS/cryptographic configurations;
- prevent secrets from appearing in URLs, logs, evidence artifacts, or client-visible error bodies; and
- distinguish connectivity from authority.

### Cryptography

Where the customer requires federal cryptographic-module requirements, the profile must support FIPS 140-3 validated cryptographic modules/endpoints appropriate to the environment.

The profile must record:

- required cryptographic policy;
- applicable endpoint mode;
- TLS requirements;
- signing/hashing requirements;
- key/secret ownership;
- evidence that the selected runtime/endpoint matched the approved profile.

SHA-256 or stronger remains the baseline for IPW artifact integrity unless a stronger customer requirement applies.

### SI — System and Information Integrity

The CEL and any EEA receiving a delegation grant must:

- fail closed on malformed or unsupported execution/delegation grants;
- reject digest mismatch;
- authenticate the artifact appropriate to its role: a CEL-local executor rejects an unsigned/unauthenticated execution package/grant, untrusted issuer, wrong CEL audience, or unverifiable approval provenance; an EEA rejects an unsigned/unauthenticated CEL delegation grant, untrusted CEL issuer, wrong EEA audience, broken parent-grant chain, or unverifiable carried approval provenance;
- reject expired authorization;
- reject replay or conflicting duplicate operations;
- prevent a completed, expired, or revoked execution grant from becoming standing continuous write authority;
- require later drift-driven writes to obtain a fresh plan/effect authorization and execution/delegation grant;
- detect unsupported adapter/engine versions;
- require a two-phase plan/authorization or immutable saved-plan protocol before mutation;
- bind exact planned effects, affected resources, and provider-state preconditions into the authenticated execution/delegation grant;
- invalidate authority on re-plan, state-precondition, affected-resource, or effect-digest drift;
- require separate exact authority for destroy, replace/recreate, or other irreversible effects even when produced by update/rollback/reconcile;
- surface drift and degraded reconciliation states;
- distinguish provider API acceptance from resource readiness;
- avoid auto-escalating permissions to recover from failure;
- preserve bounded failure evidence; and
- support vulnerability and dependency remediation without silently widening runtime authority.

### SR / SA — Supply Chain and Acquisition

The CEL deployment profile should support:

- version-pinned dependencies;
- provenance/signature verification where available;
- customer-controlled package/container mirrors;
- restricted-network acquisition;
- SBOM/provenance retention where required;
- review of third-party provider/adapters;
- explicit supported-version matrices;
- tamper detection;
- controlled upgrade/rollback;
- removal/revocation of compromised artifacts; and
- no download-and-execute behavior from untrusted runtime sources.

Third-party adapter inclusion does not transfer customer risk acceptance to IPW.

A hosted orchestration service that receives provider credentials or can directly cause provider mutation is a separate **External Execution Authority**, not merely a software dependency. The customer must explicitly approve its trust boundary, credential custody, data processing, network path, logging/evidence, retention, incident, revocation, and shared-responsibility model. Where feasible, a customer-hosted agent/runtime should keep provider credentials and provider API calls inside the customer-controlled boundary.

### IR — Incident Response

The CEL must support evidence needed to investigate:

- unauthorized execution attempts;
- denied policy transitions;
- identity/trust failures;
- anomalous retries/replays;
- cross-tenant routing attempts;
- unexpected provider mutations;
- compromised adapter versions;
- failed rollback/teardown;
- evidence-delivery failures.

The customer incident-response program remains authoritative for declaration, containment, reporting, and recovery decisions.

## Government cloud/environment profiles

Government support is not represented by a generic boolean.

Each cloud/environment profile must define its exact semantics.

### AWS

The profile must distinguish commercial AWS from AWS GovCloud (US) partitions and account/organization boundaries.

The adapter configuration must explicitly bind:

- partition;
- approved region(s);
- account/organization boundary;
- service endpoint profile;
- FIPS endpoint requirements where applicable;
- workload-identity method;
- effective IAM role/policy;
- logging/security-event destinations; and
- network path.

A commercial AWS endpoint, ARN pattern, service availability assumption, or identity configuration must not be silently reused for GovCloud.

### Azure

The profile must distinguish Azure commercial from Azure Government.

The adapter configuration must explicitly bind:

- Azure cloud environment;
- tenant;
- management-group/subscription/resource-group boundary;
- approved region(s);
- ARM/resource endpoints appropriate to the cloud;
- Microsoft Entra identity authority appropriate to the cloud;
- workload/managed identity configuration;
- private endpoint/network requirements;
- logging/security destinations; and
- cryptographic requirements.

Commercial-cloud service availability or endpoint semantics must not be assumed for Azure Government.

### Google Cloud

Google Cloud federal deployment must be represented through the exact customer control environment rather than by inventing a separate generic "GovCloud" mode.

Where required, the profile may bind:

- organization/folder/project hierarchy;
- Assured Workloads control package/environment;
- approved regions/data-location constraints;
- Workload Identity Federation;
- VPC Service Controls or other customer-selected perimeter controls;
- approved services;
- logging/security destinations;
- key-management/encryption requirements; and
- evidence required to demonstrate those settings.

The executor must verify that the target project/environment satisfies the exact approved profile before mutation.

## Restricted-network profile

The Government Security Profile must be compatible with the portfolio's restricted-network direction.

A deployment may require:

- customer-controlled container mirrors;
- customer-controlled package mirrors;
- pinned GitHub Actions or internally hosted equivalents;
- proxy-only egress;
- no arbitrary browser/runtime downloads;
- private CA;
- internal artifact repositories;
- allowlisted provider endpoints;
- disconnected validation before external connectivity is granted.

The execution layer must not weaken those controls merely because a cloud provider adapter normally assumes public internet access.

## Human authorization

A human approval reference and the resulting execution package must be authenticity-protected and bind to the exact:

- trusted issuer / decision provenance;
- intended CEL audience;
- customer/tenant;
- FoundationTarget;
- product/revision;
- desired-state digest;
- operation;
- trusted profile;
- assessment/evidence set;
- expiration/validity period.

Approval is invalid if any material binding changes.

A prior approval does not authorize:

- another customer;
- another cloud target;
- another environment;
- another operation;
- a later product revision;
- deletion;
- expanded permissions; or
- production when only non-production was approved.

## Evidence model

The Government Security Profile should make control-relevant evidence machine-readable where practical.

Evidence should be able to map implementation observations to customer assessment requirements without claiming the assessment conclusion.

Examples:

| Control intent | CEL evidence example |
|---|---|
| least privilege | exact workload principal, role/policy reference, effective-scope observation |
| separation of duties | distinct proposal, assessment, approval, and execution identities |
| auditability | execution event IDs, provider activity/request IDs, evidence digests |
| configuration integrity | product/config/adapter/profile revisions and digests |
| boundary protection | approved endpoints, network profile, proxy/private-endpoint evidence |
| cryptography | endpoint/crypto profile and validated runtime references |
| monitoring | delivery/health events and customer-selected SIEM references |
| supply chain | pinned versions, provenance/signatures/SBOM references |

## Assessor boundary

IPW may:

- generate evidence;
- verify integrity/provenance;
- map evidence to requirements;
- identify missing evidence;
- support continuous monitoring inputs; and
- preserve decision history.

IPW must not independently declare:

- control effectiveness for the customer's authorization boundary;
- risk acceptance;
- POA&M closure;
- FedRAMP authorization;
- FISMA compliance;
- ATO/cATO approval; or
- agency production authorization.

Those decisions remain with authorized customer/assessor/authorizing roles.

## Acceptance criteria

A future Government Security Profile implementation is not accepted until tests prove at least:

1. static cloud keys are rejected by the default profile;
2. target/customer substitution fails closed;
3. region/partition/cloud-environment substitution fails closed;
4. expired and replayed authorizations fail closed;
5. excessive effective permissions fail the applicable execution profile;
6. missing audit/evidence sink fails according to profile policy;
7. non-approved endpoints fail;
8. private-CA/proxy behavior works under the selected profile;
9. artifact tamper fails;
10. unsupported adapter/engine version fails;
11. cross-tenant execution fails;
12. destroy or replace/recreate effects cannot be inferred from create/update/rollback/reconcile authority;
13. the exact planned-effect set is verified before mutation and ambiguous destructive effects fail closed;
14. untrusted issuer, wrong audience, bad signature/attestation, or fabricated approval provenance fails closed;
15. a hosted execution service with provider authority is treated as a separate trust zone and cannot bypass CEL authorization;
16. the EEA rejects a CEL-audience package and requires its own CEL-signed audience-bound delegation grant;
17. the EEA delegation grant binds exact planned effects, affected resources, provider-state preconditions, target, expiry, replay identity and revocation state;
18. CEL or EEA execution fails closed if the plan/effects or provider-state preconditions change after authorization;
19. an EEA checks current authoritative revocation state (or uses a grant-scoped provider identity whose revocation is provider-enforced) immediately before each mutation;
20. inability to establish current revocation freshness prevents an EEA mutation;
21. completion/expiry/revocation of a grant removes or suspends continuous provider-write capability;
22. a later drift correction requires a fresh plan, provider-state preconditions, authorization, and execution/delegation grant;
23. customer revocation prevents subsequent provider mutation;
24. partial provider failure remains explicit;
25. EEA-returned evidence is signed/attested by the exact authorized EEA and linked to the exact delegation grant, plan/effects, attempt identity, provider results, and replay identity;
26. replay of an already accepted EEA result nonce/receipt sequence is rejected for current-state projection;
27. an EEA result outside the permitted receipt window is historical-only unless an explicit late-result rule accepts it without superseding newer state;
28. a result for an attempt that is neither outstanding nor the latest terminal attempt, or that has been superseded by a newer accepted attempt/result, cannot become the current operational result;
29. an older signed EEA result cannot replace a newer accepted attempt/result;
30. required provider-state freshness/reference mismatch prevents the result from being projected as current state;
31. stale/replayed/superseded results may be retained only as ordered historical evidence with explicit disposition;
32. evidence does not contain credentials/secrets;
33. restricted-network dependency acquisition is deterministic; and
34. no test result is promoted into an authorization claim.

## Relationship to cloud-provider attestations

Cloud-provider FedRAMP, DoD, government-cloud, or other certifications/authorizations are inherited inputs only to the extent the customer's architecture and authorization boundary permit.

They do not automatically authorize:

- the IPW deployment;
- the customer's configuration;
- the CEL;
- an individual infrastructure product; or
- the customer's production use.

## Related architecture

- [Customer Execution Layer](../../architecture/customer-execution-layer.md)
- [Provider-neutral foundation contract](../providers/provider-neutral-contract.md)
- [FoundationTarget](../schemas/foundation-target.md)
- [Live sandbox gate](../readiness-gates/gate-4-live-sandbox.md)
- [Provider and partner boundaries](../responsibility-matrices/provider-partner-boundaries.md)
