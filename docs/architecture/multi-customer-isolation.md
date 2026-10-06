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


## Shared platform and customer-specific administration boundary

A shared platform operator may own the cloud organization, provider relationship, landing-zone factory, or common management services while each customer retains a separately scoped product and workload boundary. Shared ownership of the substrate does not merge customer identity, approval, evidence, secrets, workload administration, or risk decisions.

| Responsibility | Shared platform operator | Customer product/workload owner |
|---|---|---|
| Foundation | Defines approved provider services, network paths, baseline identity and security controls, logging destinations, and allowed target scopes | Selects an approved foundation target for its workloads and supplies customer-specific requirements |
| Accounts and resource hierarchy | Creates or assigns the customer’s account, subscription, project, folder, or equivalent scope under shared guardrails | Administers products and resources within the assigned scope, subject to platform guardrails |
| IPW control plane | May provide hosting or a shared runtime only under an accepted deployment profile | Owns or explicitly accepts the customer’s product catalog, profiles, policies, approval roles, and customer-scoped records |
| Execution authority | Operates only the shared foundation functions it has been assigned | Customer-controlled execution identity performs only the exact approved action against the customer’s bound target |
| Evidence and operations | Supplies platform-level events, inherited-control evidence, and shared-service operations evidence | Retains customer-specific approvals, product/evidence history, workload telemetry, and operational decisions |

The shared platform boundary and customer boundary must be represented separately in the deployment profile, identity map, data-flow diagram, access review, and evidence records. A shared-platform identity must not gain workload or customer-evidence access merely because it operates the underlying platform. Any exceptional support or emergency access must be separately authorized, time-bounded, attributable, and logged.

The product control plane does not hold broad provider credentials. A customer-controlled execution layer (CEL) validates the exact customer, organization, environment, target, approved product, decision, and execution package before a provider call. Cloud-native guardrails remain enforceable at the shared platform boundary; the narrower of the platform-permitted scope and customer-approved scope governs. A conflict, missing boundary, or unsupported delegation fails closed.

This pattern is compatible with either a dedicated customer runtime or a managed-isolated customer runtime. It does not require shared multi-tenant SaaS and does not imply that the platform operator owns the customer’s mission decisions or workload data. See [Customer Execution Layer](customer-execution-layer.md) for the execution-authority contract.

## Shared-platform deployment acceptance

Before a customer-hosted or managed-isolated deployment can advance beyond documentation and synthetic validation, its acceptance profile must identify:

1. the shared platform operator and customer product/workload owner, including who can approve, administer, support, and revoke each layer;
2. the exact customer boundary (account, subscription, project, tenant, or equivalent) and which upstream guardrails constrain it;
3. where the IPW product control plane, customer-scoped data, secrets, audit records, and CEL run;
4. the human and workload identities used at each boundary, with least privilege, short-lived access where supported, and explicit break-glass handling;
5. the evidence each party supplies and retains, including how customer-specific records stay separate from shared platform operations;
6. the denied paths and synthetic negative tests for cross-customer target substitution, operator privilege leakage, stale approval, and unintended scope expansion; and
7. recovery, incident response, export, and decommissioning ownership for both layers.

These are acceptance requirements. They do not claim that any current deployment has passed them.
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
