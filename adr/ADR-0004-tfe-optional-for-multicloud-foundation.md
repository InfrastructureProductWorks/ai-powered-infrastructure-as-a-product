# ADR-0004: Terraform Enterprise Is Optional for the Multi-Cloud Foundation Product Architecture

- **Status:** Accepted
- **Date:** 2026-08-07
- **Decision scope:** Credential-free, non-production AWS and GCP minimum viable foundation POC
- **Evidence baseline:** `credential-free-multicloud-foundation-v1`

## Executive decision

Terraform Enterprise (TFE) will **not** be treated as a mandatory architectural dependency or the presumed strategic control plane for the multi-cloud foundation product.

The default product architecture is:

1. A minimal trusted bootstrap establishes Crossplane and its control-plane boundaries.
2. Crossplane exposes versioned infrastructure products through stable Kubernetes APIs.
3. Deterministic policy decides what is allowed.
4. Composite AI assists with request intake, review, diagnosis, explanation, and evidence generation.
5. Humans retain approval authority.
6. Crossplane, not the AI layer, performs reconciliation.

TFE remains eligible as an **optional implementation tool** for explicitly justified use cases such as bootstrap, brownfield Terraform estates, migration, stateful legacy workflows, or exceptions that Crossplane does not yet serve economically or safely.

## Context

The organization already owns or is evaluating TFE while AWS is more mature and GCP and Azure foundation capabilities are still developing. Treating TFE as mandatory before testing alternatives would convert an implementation choice into an architectural constraint.

Technology and operating models have changed:

- Crossplane can expose infrastructure through product APIs instead of distributing raw infrastructure code to every consumer.
- Composite AI can accelerate intake, review, operations diagnosis, and evidence without receiving execution authority.
- Infrastructure-as-a-Product shifts the unit of value from a Terraform workspace or module to a supported, governed consumer outcome.
- GitHub-based validation and evidence can make the platform decision measurable rather than assumption-driven.

The decision therefore requires executable evidence that a minimum viable foundation path can operate without TFE.

## Evidence

The integration workflow run [Portfolio integration](https://infrastructureproductworks.com/portfolio/) passed across Kubernetes 1.34, 1.35, and 1.36.

Each matrix entry scored **100/100** and proved:

- Crossplane 2.3.0 installation from a bounded seed.
- Active ingress and egress NetworkPolicy enforcement.
- Stable AWS and GCP `CloudFoundationEnvironment` requests.
- Successful simulated reconciliation and Ready conditions.
- Deterministic rejection of production, invalid-region, and TFE-coupled requests.
- Composite AI proposal-and-evidence-only authority.
- Prompt-injection containment.
- An AI service account with no product-create authority.
- Complete teardown with zero product-component orphans.
- Exact upstream commit verification.

The frozen evidence is documented in [`docs/poc-baselines/2026-08-07-credential-free-multicloud-foundation.md`](../docs/poc-baselines/2026-08-07-credential-free-multicloud-foundation.md).

## Decision drivers

### Product ownership

The platform should own a small set of supported infrastructure products, their contracts, policies, evidence, lifecycle, and service outcomes. Consumers should request products rather than assemble the platform from low-level tooling.

### Separation of concerns

- Composite AI proposes, explains, and collects evidence.
- Deterministic policy validates.
- Humans approve.
- Crossplane reconciles.
- GitHub preserves source, review, and evidence history.

No single component is allowed to silently expand its authority.

### Avoiding mandatory-tool coupling

A platform architecture should not require a commercial workflow engine unless the required outcome cannot be achieved safely, supportably, and economically without it.

### Measurable investment

TFE investment should be based on demonstrated remaining use cases, operating cost, migration cost, governance benefit, skills availability, and lock-in—not on historical familiarity or prior purchase.

## What this decision does not claim

This ADR does **not** claim that:

- TFE is obsolete for every organization or workload.
- The POC is production ready.
- Simulated AWS and GCP resources prove live-cloud provider behavior.
- Crossplane should immediately replace every Terraform estate.
- Existing TFE workspaces should be migrated without workload-by-workload analysis.
- AI should receive infrastructure execution authority.

The evidence supports a narrower conclusion: **TFE is not required for the demonstrated foundation-product path and must earn any broader role through additional evidence.**

## TFE decision matrix

| Use case | Default position | Required justification |
|---|---|---|
| New productized foundation APIs | Crossplane-first | Demonstrate a capability, safety, support, or cost gap that TFE uniquely closes |
| Minimal bootstrap | Native tooling or bounded Terraform/OpenTofu; TFE optional | Show why remote orchestration is needed before Crossplane exists |
| Existing brownfield TFE estate | Retain temporarily | Record ownership, state, migration risk, lifecycle, and retirement or coexistence plan |
| One-time migration/import | TFE optional | Time-box the use and prevent dual ownership after migration |
| Unsupported Crossplane resource | Exception path | Confirm no practical provider or composition option and define exit criteria |
| AI-generated change | Proposal only | Human approval and deterministic policy remain mandatory; AI receives no apply authority |
| Same resource managed by TFE and Crossplane | Prohibited | One authoritative reconciler per resource |

## Consequences

### Positive

- The organization can continue the foundation effort without waiting for TFE platform maturity.
- The control plane is aligned to product APIs and continuous reconciliation.
- Composite AI is useful without becoming a privileged automation account.
- TFE can be evaluated where it adds measurable value rather than adopted everywhere by default.
- Existing Terraform investments can coexist during a controlled transition.

### Tradeoffs

- Crossplane provider maturity and Kubernetes operating skills become important platform concerns.
- Live-cloud identity, ProviderConfig, quotas, service controls, billing, and teardown still require validation.
- Brownfield state and import workflows may remain easier in Terraform for some resources.
- The organization must govern one-reconciler ownership to prevent TFE/Crossplane conflicts.

## Guardrails

1. Never allow TFE and Crossplane to co-manage the same resource.
2. Keep cloud credentials and provider configuration outside the composite-AI runtime.
3. Require deterministic policy and human approval before execution.
4. Preserve exact source commits and evidence digests for each accepted baseline.
5. Treat production enablement as a separate decision gate.
6. Time-box exceptions and document their exit criteria.

## Next decision gate

The next phase will validate a live AWS sandbox path using workload identity, bounded provider configuration, real resource reconciliation, evidence collection, and deterministic teardown. GCP follows after the AWS path is repeatable.

In parallel, a limited TFE comparison will measure only the use cases where it may still add value:

- bootstrap,
- brownfield state,
- migration/import,
- exception resources,
- governance and evidence integration,
- operational cost and skills burden.

A production investment recommendation will be made only after those results are available.
