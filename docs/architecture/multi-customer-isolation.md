# Multi-Customer Isolation Architecture

| Attribute | Definition |
|---|---|
| Status | Public architecture contract and implementation target |
| Scope | Customer, organization, environment, identity, policy, evidence, secrets, integrations, audit, lifecycle, recovery, and deployment isolation |
| Current-product claim | None; this document does not claim current shared multi-tenant SaaS, customer-operational isolation, pilot, or production readiness |

## Principle

Infrastructure Product Works may serve multiple customers only when customer context is explicit and preserved across every participating product boundary. Customer separation must be enforced by contracts, identity, evidence, credentials, storage, and deterministic validation rather than by naming conventions or operator discipline.

The minimum customer scope is:

```text
customerId
  organizationId
    environmentId
```

Products may add narrower system, profile, product, order, assessment, approval, or resource scopes. They must not silently drop or substitute the customer context.

## Portfolio propagation

```text
Storefront order
  -> Guard assessment / trusted profile
  -> Console review and selection
  -> Forge product proposal and rendered binding
  -> authorized handoff
  -> Assurance custody and continuity
  -> optional reconciliation adapter
```

Every customer-scoped artifact crossing these boundaries must preserve the accepted customer context. Missing, conflicting, or substituted context fails closed.

## Required invariants

- Human identities, service identities, approvers, and automations are authorized within explicit customer scope.
- Trusted profiles, assessments, evidence packages, approvals, selections, product definitions, rendered artifacts, and assurance records are bound to their customer context.
- Secrets, GitHub/GHES installations, cloud credentials, repositories, webhooks, model adapters, and provider integrations are isolated by customer unless an explicitly governed shared service says otherwise.
- Policy/profile/product versions may advance independently by customer. One customer's supersession or withdrawal does not rewrite another customer's accepted history.
- Audit history remains customer-scoped and reconstructable.
- Cross-customer replay and substitution are explicit negative-test classes.
- Shared infrastructure alone is never evidence of safe multi-tenancy.

## Deployment patterns

### Dedicated enterprise

One customer operates a dedicated Infrastructure Product Works environment. Runtime, credentials, data, policy, evidence, integrations, and operational control remain in that customer's security boundary.

### Managed isolated

A product operator maintains a common codebase while each customer receives a separate runtime/security domain. Customer data, secrets, integrations, evidence, and operational blast radius remain isolated.

### Shared multi-tenant SaaS

Multiple customers share runtime infrastructure behind hard logical tenant boundaries. This model requires additional evidence for tenant-aware identity, data/key separation, observability, backup/recovery, incident response, privacy, rate/resource isolation, and operational controls. It is separately gated and is not required for the portfolio to support multiple customers.

For regulated enterprise adoption, dedicated-enterprise and managed-isolated deployment are the preferred near-term target patterns.

## Trusted profile relationship

Trusted-profile approval binds:

```text
customer
+ profile version
+ system
+ scope
+ approved requirements/evidence mappings
+ approver identity
```

A change to customer scope, requirements, evidence mappings, system, or permitted operational evidence requires renewed review. Withdrawn or superseded profiles remain historical evidence but cannot silently support new assessments.

## Synthetic acceptance before runtime claims

Documentation and synthetic proof precede implementation claims:

1. define the customer-context contract;
2. map all customer-scoped artifacts;
3. add same-customer positive fixtures;
4. add cross-customer profile, approval, evidence, order, selection, product-binding, and replay substitutions;
5. prove deterministic rejection;
6. verify customer-scoped audit reconstruction;
7. validate dedicated and managed-isolated deployment profiles;
8. keep shared SaaS unclaimed until separately accepted.

No live customer data, customer credentials, provisioning authority, or production operation is required for this documentation-first acceptance work.
