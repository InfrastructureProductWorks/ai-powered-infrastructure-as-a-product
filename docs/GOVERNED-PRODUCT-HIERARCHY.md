# Governed Product Hierarchy and Operating Model

> **Secure by product definition. Governed by contract. Validated by evidence.**

Infrastructure-as-a-Product does not jump from raw cloud APIs directly to a developer-facing portal. A cloud capability becomes consumable only after it has been productized into a governed service product with a stable contract, minimum security baseline, bounded configuration envelope, entitlements, evidence requirements, lifecycle rules, and exception policy.

## Product hierarchy

```text
Raw cloud services
        ↓
Governed service products
        ↓
Composite infrastructure products
        ↓
Developer outcomes
```

Examples of governed service products include Network Product, Object Storage Product, Database Product, Kubernetes Product, DNS Product, Identity Product, Logging Product, and Messaging Product.

Composite products such as Cloud Foundation Environment, Application Platform Environment, Data Platform Environment, and Managed Interconnect are assembled from those governed service products rather than directly from provider primitives.

## Productization rule

**No raw cloud service becomes a developer-facing dependency until it has been productized.**

For each service product, the product definition should establish at least:

- a stable consumer contract;
- minimum security and compliance baseline;
- approved architecture patterns and provider mappings;
- allowed configuration and sizing envelope;
- entitlements, quotas, cost limits, and accountable ownership;
- required evidence and traceability;
- lifecycle, versioning, deprecation, and upgrade behavior;
- exception criteria and required approvers.

## Governed Product Inheritance

A composite infrastructure product inherits the security, governance, evidence, entitlement, and lifecycle constraints of the governed service products from which it is composed.

Composition may add tighter controls. It must not silently weaken inherited controls.

This prevents every new developer-facing environment from rebuilding security, networking, identity, logging, cost controls, and evidence from scratch.

## Security and governance operating role

Governance, Risk, and Security define **what must remain true**. Platform Engineering defines **how the product makes it true**.

Security responsibilities include:

- defining minimum security baselines;
- maintaining mandatory standards and prohibited states;
- defining required evidence and material-change criteria;
- identifying when human security review is required;
- defining exception and waiver rules;
- monitoring recurring control failures and policy drift.

Security does not need to manually approve every instance of an already-approved product. Compliant consumption inside the approved contract should remain automated. Human review is reserved for exceptions, material changes, and policy transitions.

## Platform Engineering role

Platform Engineering converts the approved baseline into executable product behavior through:

- schemas and closed contracts;
- product profiles and compositions;
- provider-specific implementation mappings;
- deterministic validation rules;
- control-plane reconciliation behavior;
- lifecycle and operational evidence.

Minimum security requirements are product behavior, not optional consumer choices. A developer should not be asked whether encryption, audit logging, or other mandatory controls should be enabled.

## Entitlements and cost controls

Self-service must remain bounded. Product entitlement and commercial entitlement are different concepts.

Infrastructure entitlements may constrain:

- which products a team may request;
- approved sizes or service classes;
- quotas and concurrency;
- spending limits or budget checks;
- environment TTLs;
- allowed regions or providers;
- business ownership and chargeback context.

Commercial entitlement permits use of the software. Infrastructure entitlement constrains what a team is permitted to consume. Neither is production authorization.

## Portfolio operating path

```text
Storefront
  → bounded product intent
Governance / entitlements
  → approved envelope
Guard
  → deterministic validation and evidence
Console + authorized human review
  → decision where required
Forge
  → governed product construction
Assurance
  → authority, scope, safeguards, custody
Crossplane
  → reconciliation of authorized product state
```

This is a responsibility map, not a requirement that every deployment execute every component in one rigid sequence.

## Operating principle

> **Review the product once. Automate compliant consumption. Escalate exceptions.**

That is how governance scales without turning Security into a ticket queue and without turning developer self-service into unconstrained cloud consumption.