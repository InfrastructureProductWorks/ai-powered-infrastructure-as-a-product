# Storefront protected-main evidence — 2026-09-11

**Posture:** `CONTINUE_VALIDATION`  
**Purpose:** retain the exact source and acceptance coordinates supporting the public thesis statement that InfrastructureProductWorks now has a first-class standalone Storefront application plus a Backstage Storefront Adapter.  
**Authority:** evidence/provenance record only. This record grants no credential, approval, merge, apply, deploy, remediation, provisioning, pilot, production, compliance, or customer-data authority.

## Source coordinate

Repository: `InfrastructureProductWorks/backstage-infrastructure-product-storefront-poc`  
Protected-main merge: `1b0af539d62a569fe48bcb1f140682a1f9be0c20`  
Merged PR: `#22 — Storefront: apply drive-thru visual experience`  
Standalone application version: `0.2.0`  
Backstage adapter release: `storefront-distribution-v0.1.1`  
Backstage adapter protected-main release coordinate: `790643571d5e40566f51062093e5aabb1cd8a171`

The September 11 drive-thru visual refresh was intentionally contract-neutral and did not create a new Storefront application version.

## Exact-head acceptance before merge

The final PR head was `da8c32427f468e029c7c664fdffc4f42d8b41b95`. The following GitHub Actions runs passed on that exact head before protected-main merge:

| Gate | Run | Result |
|---|---:|---|
| Standalone Storefront smoke | `34607361042` | PASS |
| Validate storefront POC | `34607360949` | PASS |
| IaaP Guard Dogfood | `34607360737` | PASS |
| Root README link integrity | `34607361756` | PASS |
| Backstage runtime smoke | `34607360619` | PASS |

The standalone smoke built the customer-hosted Storefront runtime, exercised live HTTP order submission, verified the digest-bound order/handoff and independent issuance record, rejected a tampered handoff, and proved the container remained non-privileged. The Backstage runtime smoke independently proved the adapter through a real Backstage Scaffolder dry-run without live infrastructure or repository writes.

## Demonstrated bounded capability

At the pinned source coordinate, the first-class Storefront demonstrates:

- browser-based product discovery and bounded order configuration;
- the closed `InfrastructureProductOrder` contract;
- contract validation and fail-closed request handling;
- session-scoped `AWAITING_HUMAN_REVIEW` status;
- digest-bound order identity;
- inert `iaap-storefront-handoff/v1` envelope issuance;
- independent `iaap-storefront-handoff-verification/v1` issuance record;
- browser-side canonical SHA-256 recomputation against the issuance record;
- customer-hosted web/OCI packaging; and
- zero Storefront approval, merge, apply, deploy, remediation, or provisioning authority.

The Backstage Storefront Adapter demonstrates the same bounded order contract through a customer-controlled Backstage installation and remains an adapter rather than the canonical Storefront application.

## Explicit non-claims

This record does **not** prove or claim:

- authenticated external transport of a Storefront handoff into Console, Forge, GitHub, Crossplane, or a cloud provider;
- durable customer persistence or production-grade authentication/authorization for the standalone Storefront;
- pilot or production readiness;
- FedRAMP, FISMA, ATO/cATO, or other compliance authorization;
- autonomous approval or infrastructure authority; or
- that product cards labeled `Coming soon` are released or orderable.

Only **Cloud Foundation Environment** is currently orderable through the bounded Storefront implementation.

## Public-thesis interpretation

This record allows the public thesis to distinguish the implemented experience surfaces without treating implementation evidence as operational authorization:

> **Storefront is the first-class product experience. Backstage is a supported adapter. Authorized people make material decisions. Crossplane reconciles authorized product state.**
