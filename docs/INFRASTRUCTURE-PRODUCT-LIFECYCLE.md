# Infrastructure Product Lifecycle

## Purpose and maturity

IPW is designed to manage the lifecycle of infrastructure products: from customer need and investment through delivery, operation, evolution, and retirement. Infrastructure productization is the organizing purpose; the applications contribute distinct responsibilities to that lifecycle.

This is a documentation-first target model. Existing bounded product implementations and synthetic demonstrations do not establish complete lifecycle coverage. Acceptance of this document does not authorize funding, product release, customer hosting, infrastructure execution, or resource destruction. Stage names describe business responsibilities, not newly implemented application states or permissions.

## Two lifecycles, connected

A **product definition** has an accountable owner, supported versions, consumer contract, eligibility, cost assumptions, service commitments, support boundaries, and a retirement policy. A **customer instance** is one fulfillment of an approved product version in a particular customer scope.

Publishing a product does not authorize every customer instance. Deprecating a version does not destroy its instances. Retiring an instance does not necessarily retire the product. Product records and instance records must remain distinguishable throughout ordering, operation, change, and evidence retention.

## Lifecycle responsibilities

| Stage | Accountable decision and intended IPW contribution | Evidence needed to advance |
| --- | --- | --- |
| Discover and justify | Product leadership owns the customer need and investment decision. Northstar Signal connects outcomes, reuse choices, funding assumptions, capacity, and accepted delivery work. | Defined consumer and outcome, named owner, reuse assessment, cost assumptions, and separately authorized investment where required. |
| Define and develop | Product and domain teams define the offering. Forge constructs the versioned product proposal while domain authorities retain standards and exceptions. | Consumer contract, supported implementations, dependencies, eligibility, cost basis, support commitments, compatibility, and rollback expectations. |
| Validate and approve | Authorized reviewers decide readiness. Guard supplies bounded assessments; Console presents review evidence; Assurance contributes authority and custody context. | Evidence for the exact proposed version and scope, resolved blockers, valid approvals, and retained decision history. |
| Publish and order | Product owners authorize publication. Storefront presents approved offerings and captures customer requests. | Published version and eligibility, customer scope, selected options, cost disclosure, admission result, and an identifiable order. |
| Deliver and operate | Customer execution and operations authorities own fulfillment and service operation. TFE or Crossplane may execute behind an accepted adapter; IPW connects the request and evidence. | Separately authorized execution, observed fulfillment, assigned operations owner, support/runbook readiness, service health, actual cost, and recovery evidence. |
| Improve and evolve | Product owners use customer feedback and operational evidence to prioritize changes. Northstar informs decisions; Forge prepares controlled versions. | Adoption and outcome measures, incident and cost feedback, dependency impact, compatibility assessment, authorized upgrade, rollback, and observed results. |
| Deprecate and retire | Product owners govern notices and alternatives; customer authorities govern migration and destructive effects; evidence custodians govern retention. | Consumer/dependency inventory, notice and migration plan, separate destructive authorization where needed, resource and data disposition, orphan checks, and retained closure evidence. |

These are responsibilities rather than an enforced linear pipeline. A product can return to discovery or development when evidence changes. An instance can remain on an older supported version while a replacement is validated.

## Execution-platform boundary

TFE supplies Terraform plan/apply execution and state management. Crossplane supplies declarative APIs and reconciliation. Neither is granted new authority by a lifecycle label, an AI proposal, a catalog listing, or a Northstar decision. Adapter portability is a target requiring platform-specific implementation and evidence; this document does not establish interchangeable execution adapters.

The product contract stays consumer-facing. Provider and execution details remain behind it. Actual cloud costs and billing remain authoritative in their source systems; planning estimates do not become approved budgets or observed spend. Likewise, support commitments require an accountable operations team rather than a dashboard label.

## Documentation-first roadmap and acceptance evidence

The following slices are requirements for future implementation, not completed features, numeric progress claims, or dated delivery commitments. Existing roadmap and application authorities remain authoritative for their own records.

| Slice | Required implementation proof |
| --- | --- |
| Product ownership and contract | Recover the same owned product/version and customer-instance distinction across persistence and handoffs; reject requests without required ownership or scope. |
| Publication and ordering | Demonstrate eligible version selection, publication authority, withdrawal handling, and order history without silently changing an existing order's version. |
| Operational service lifecycle | Bind fulfillment, support ownership, health, recovery, observed cost, and incidents to the correct customer instance; show unavailable evidence as unknown. |
| Feedback and controlled evolution | Connect operational/customer evidence to product decisions; demonstrate dependency impact, supported upgrade, rollback, and preserved prior-version history. |
| Deprecation and retirement | Demonstrate notices, migration, blocked retirement with active dependents, separately authorized destructive effects, orphan detection, and evidence retention/deletion rules. |
| Cross-platform consistency | Demonstrate the same customer-facing lifecycle commitments through each accepted adapter without treating TFE and Crossplane execution semantics as identical. |

For each slice, acceptance must identify the implementation revision, tested scope, observed result, limitations, and authorized reviewer. Evidence must include wrong-customer and unauthorized actions, stale or withdrawn versions and approvals, repeated/concurrent requests, interrupted recovery, and unavailable source records where relevant. A successful synthetic exercise establishes only its tested property; it does not establish production readiness.

Public reporting should summarize coverage and remaining gaps. Private implementation mechanics and customer evidence remain restricted under the [publication boundary](PUBLICATION-BOUNDARY.md). The website's lifecycle roadmap reference should link to this model while keeping live delivery telemetry separate.

## Measures

Measure product adoption, customer outcomes, time to usable fulfillment, cost to serve, support/service performance, upgrade success, migration completion, and retirement/orphan outcomes. Report missing or unverified observations explicitly. Product maturity, customer-instance status, delivery progress, and business benefit are separate measures.

See the [operating model](OPERATING-MODEL.md), [product architecture](PRODUCT-ARCHITECTURE.md), and [thesis](THESIS.md) for the surrounding product and authority boundaries.
