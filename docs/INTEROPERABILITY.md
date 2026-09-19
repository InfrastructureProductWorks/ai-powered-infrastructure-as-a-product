# Enterprise Interoperability

The modern accelerator is intentionally not a universal replacement for every enterprise platform.

## Principle

> **Integrate where an enterprise capability is authoritative; do not inherit it as a dependency unless the product requires it.**

## Terraform / OpenTofu / TFE

An enterprise may retain Terraform or TFE for brownfield state, migrations, unsupported resources, or accredited workflows. Those systems should remain external to the maintained accelerator unless a future ADR establishes a new product requirement.

The consumer product contract should not expose workspaces, state, module topology, or plan/apply details.

## Backstage or another storefront

A storefront can present product documentation, ownership, approved profiles, request experiences, order history, status, and links.

The program now maintains [`backstage-infrastructure-product-storefront-poc`](https://github.com/InfrastructureProductWorks/backstage-infrastructure-product-storefront-poc) as the **reference consumer experience**. It demonstrates how a developer can browse, configure, order, and track `CloudFoundationEnvironment` without learning Crossplane, ProviderConfig, cloud credentials, IAM JSON, Terraform/TFE, or Composition internals.

Backstage is not the product contract and is not the provisioning or execution authority. Provider mutation occurs only through the customer-controlled execution boundary.

```mermaid
flowchart LR
  DEV[Developer] --> STORE[Backstage storefront]
  STORE --> ORDER[InfrastructureProductOrder]
  ORDER --> GOV[GitHub + AI + deterministic policy + approval]
  GOV --> API[Infrastructure product API]
  API --> GRANT[Authenticated execution grant]
  GRANT --> CEL[Customer Execution Layer]
  CEL --> XP[Reference reconciler: Crossplane]
```

The same product contract could be consumed through:

- Backstage;
- a CLI;
- an API;
- an enterprise service portal;
- a conversational interface; or
- another approved experience layer.

Changing the storefront should not require changing the infrastructure product API or its cloud implementation.

## Azure Arc

Arc can remain useful for hybrid inventory, governance, or Kubernetes management in an Azure-centered enterprise. It is not required to unify the product architecture.

## Ticketing, CMDB, and service management

GitHub governs product source and change. Tickets, CMDB, incident systems, and records platforms may remain authoritative for their existing responsibilities. Link rather than duplicate when duplication creates ownership disputes.

A storefront may display links or status from those systems without becoming their system of record.

## Existing account/project factories

If an enterprise already has an authoritative vending system, a foundation product can integrate with or depend on it. Crossplane should not silently create a second authority for the same resource.

## Consumer-experience boundary

The storefront may own:

- browse;
- configure;
- order;
- track; and
- product-facing documentation/status.

It should not silently acquire:

- cloud administrator authority;
- Kubernetes administrator authority;
- Crossplane reconciliation ownership;
- direct infrastructure apply/remediation authority;
- policy override authority; or
- approval authority.

## Rule

One external resource has one authoritative owner and reconciler. One product capability should also have one clearly defined owner, even when several enterprise systems participate in its lifecycle.
