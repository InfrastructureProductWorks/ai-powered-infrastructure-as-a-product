# Reference evidence map

**Requirement ID:** `BFR-EVD-040`

> **Status:** Traceability guide. This map distinguishes credential-free POC proof, partial design evidence, and new architecture targets. It cites canonical repositories and documents without treating a POC result as customer, live-cloud, production, compliance, or authorization evidence.

## Status definitions

- **Proven in bounded POC:** executed or deterministically tested inside the documented credential-free scope.
- **Partial:** a contract, template, placeholder, rule, or design exists, but the operational capability or customer integration was not fully executed.
- **New target:** not implemented or proven by the four canonical POC repositories.

## Canonical repositories

| Repository | Canonical evidence areas |
|---|---|
| `Crossplane reference` | `README.md`, `VALIDATION.md`, `docs/ARCHITECTURE.md`, `docs/POC_BOUNDARIES.md`, `docs/SECURITY.md`, `docs/adr/0001-seed-not-foundation.md`, `docs/adr/0003-network-policy-runtime-evidence.md` |
| `Foundation reference` | `README.md`, `VALIDATION.md`, `docs/PRODUCT_CONTRACT.md`, `docs/POC_BOUNDARIES.md`, `api/xrd-cloud-foundation-environment.yaml`, `policies/validating-admission-policy.yaml`, `provider-configs/README.md`, `compositions/` |
| `Composite AI reference` | `README.md`, `VALIDATION.md`, `docs/POC_BOUNDARIES.md`, `docs/SECURITY.md`, `docs/THREAT_MODEL.md`, `docs/EVALUATION.md`, `config/`, `contracts/`, `policies/`, `tests/` |
| `Portfolio integration` | `README.md`, `VALIDATION.md`, `docs/BOUNDARIES.md`, `docs/EVIDENCE_MODEL.md`, `config/acceptance.json`, `evidence/`, `scorecard/`, `tests/` |

The [public POC baseline index](../../poc-baselines/README.md) preserves externally reviewable scope and outcome records without making the implementation repositories part of the customer runtime.

## Proven in bounded POC

| Topic | Canonical evidence | POC-only limitation |
|---|---|---|
| Minimal nonproduction seed | seed `README.md`, architecture, boundary ADR | Existing approved Kubernetes cluster is assumed; no customer hosting foundation is built. |
| Pinned Crossplane and package guardrails | seed configuration, security, validation | Package tags/checksums support the POC; this is not full production provenance. |
| AI identity with no Kubernetes authority | seed security/boundaries; integration acceptance | Proves denial for the POC service account, not enterprise identity or tenancy. |
| Active namespace NetworkPolicy tests | seed NetworkPolicy ADR and validation; integration evidence | Proves Kubernetes namespace ingress/egress for tested clusters, not cloud/hybrid ingress or egress. |
| Stable bounded product API | product contract, XRD, admission policy, tests | AWS/GCP development/internal POC only; not a complete landing zone. |
| Deterministic request rejection | product schema/policy and integration acceptance | Covers enumerated POC cases, not every customer or provider control. |
| Credential-free simulated reconciliation | product simulated composition; integration harness | ConfigMap simulation does not prove AWS/GCP APIs, permissions, quotas, or service behavior. |
| Simulated teardown and orphan checks | integration acceptance/evidence model | Does not prove live-cloud deletion, retention, dependency ordering, or recovery. |
| Proposal-only AI authority | AI runtime policy, allowlist, contracts, tests | Offline deterministic provider; no live model quality or customer advisory ingestion. |
| Sanitized diagnosis and redaction | AI status contract, threat model, redaction tests | Operates on supplied sanitized status, not unrestricted live operations data. |
| AI evidence digests | AI evidence implementation and tests | Hashes are not signatures, attestations, durable retention, or producer authenticity. |
| Credential-free portfolio scorecard | integration evidence schema and scorecard | A POC score measures only required POC controls; it is not readiness, compliance, or authorization. |

## Partial design evidence

| Topic | Canonical evidence | What remains unproven |
|---|---|---|
| Live AWS/GCP sandbox path | product live composition and provider-config guidance | No live resource creation, ProviderConfig validation, effective-permission proof, or live teardown. |
| Workload identity outcome | product live templates and identity guidance | AWS trust is a deny placeholder; GCP federation binding is not demonstrated. |
| Private network product | product contract and compositions | No enterprise routing, DNS, firewall/inspection, hybrid connectivity, or live validation. |
| Private/encrypted storage intent | product contract and simulated composition | Provider-managed/default encryption is not customer KMS ownership, rotation, or evidence. |
| Ownership and cost metadata | product XRD requires owner/cost center/change ID | Metadata is not governance RACI, budget enforcement, allocation, or FinOps operation. |
| Human review boundary | AI PR contract and integration assertions | Requirement is encoded; no actual accountable human approval/merge event is proven. |
| Git-governed delivery | seed/product workflows and PR proposal | No end-to-end approved GitOps controller handoff is proven by these POCs. |
| Operational guidance | product runbooks and known-error record | No support model, SLO, incident command, backup, restore, or continuity proof. |
| TFE optionality | seed/product ADRs and comparison design | No fully observed, neutral TFE-versus-Crossplane live lifecycle comparison. |
| Evidence integrity | manifests, hashes, source locks, baseline digests | No signed provenance, retention lock, customer legal hold, durable export, or restore. |

## New architecture targets

| Topic | Why it is new |
|---|---|
| Customer foundation intake and readiness assessment | POCs assess fixed architecture/tests, not a customer's organization or cloud foundation. |
| Customer-hosted Console runtime and enterprise SSO | POCs assume an approved cluster and do not implement the unified Console or workforce SSO. |
| Read-only live-cloud discovery | POCs use supplied fixtures and sanitized status with no cloud credentials. |
| Complete resource hierarchy/vending | Account, subscription, and project vending are explicitly excluded. |
| DNS ownership and hybrid resolution | Product contract explicitly does not guarantee enterprise DNS. |
| Cloud ingress, egress, inspection, and enterprise connectivity | Kubernetes NetworkPolicy proof cannot establish these cloud controls. |
| Central audit logging, SIEM, and security-event routing | No customer central integration is implemented. |
| Customer KMS, key custody, and secrets lifecycle | Static cloud keys are prohibited, but a key/secrets operating model is absent. |
| Backup, restore, disaster recovery, and continuity | POC teardown is not backup or recovery. |
| Actual pilot and production authorization | Production, regulated data, real users, SLOs, and ATO/compliance claims are excluded. |
| BFR decisions, exceptions, expiration, and RACI | These semantics and records are introduced by this package. |
| Full AWS/Azure/GCP foundation profiles | POCs include limited AWS/GCP development components; Azure is absent. |
| Bootstrap/readiness schemas | Proposed examples in this package are new and non-executable. |
| Live Composite AI foundation advisory | Current AI translates bounded product intent; it does not ingest broad foundation evidence or generate an approved foundation. |
| Customer retention, legal hold, traceability export, and restoration | Hosted POC artifacts and digests do not provide these services. |

## Claim rules

- State the proof status and scope beside every reused claim.
- Use **Kubernetes NetworkPolicy** when that is what was tested; do not abbreviate it to enterprise network isolation.
- Use **proposal requires human approval** until an actual authoritative approval event exists.
- Use **provider-default or simulated encryption intent** until customer key controls are observed.
- Use **cost metadata** until budgets and spend controls are observed.
- Use **credential-free simulated product** until live cloud evidence exists.
- Use **architecture target** for every new capability in this package.

## Related requirements

- [Evidence requirements](evidence-requirements.md)
- [Evidence integrity](evidence-integrity.md)
- [Gate 2 — simulation](../readiness-gates/gate-2-simulation.md)
- [Provider-neutral contract](../providers/provider-neutral-contract.md)
