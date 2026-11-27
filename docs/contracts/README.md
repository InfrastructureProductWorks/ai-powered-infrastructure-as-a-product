# Governed Product Discovery Contract

| Attribute | Definition |
|---|---|
| Status | Public provider-neutral discovery contract (`v1alpha1`) |
| Posture | `SYNTHETIC_ONLY` (read-only discovery contract; zero execution authority) |
| Schema | [governed-product-discovery.schema.json](governed-product-discovery.schema.json) |
| Canonical Architecture | [Governed Agentic Interoperability](../GOVERNED-AGENTIC-INTEROPERABILITY.md) |
| Authority Granted | **None** — grants zero approval, merge, apply, provisioning, privilege, credential, cloud-spend, or policy-change authority |

## Canonical Principle: Human, API, and Agent Single-Catalog Parity

> **One governed product system. Multiple consumption surfaces.**

Humans discover governed infrastructure products through Storefront, Backstage, or APIs. Enterprise agents discover the **same** governed products through a bounded, read-only Model Context Protocol (MCP) discovery surface.

Both surfaces consume the same product contracts, lifecycle states, minimum security baselines, network profiles, EP-18 customer entitlements, cost classifications, input contracts, and evidence requirements. Neither surface exposes raw cloud primitives or implementation topology, and neither bypasses deterministic validation, human review, or governed realization.

See [Governed Agentic Interoperability](../GOVERNED-AGENTIC-INTEROPERABILITY.md) and [Governed Product Hierarchy](../GOVERNED-PRODUCT-HIERARCHY.md) for the broader operating model.

## Consumer-Visible `GovernedProduct` Model

Every consumer, API, and read-only MCP discovery response uses a closed object (`additionalProperties: false`) containing exactly these 11 canonical consumer-visible fields:

| Field | Purpose | Constraint |
|---|---|---|
| `productId` | Stable governed product identifier | Lowercase identifier string (`^[a-z0-9][a-z0-9._-]{1,127}$`) |
| `version` | Semantic version of the governed product contract | SemVer string |
| `lifecycleStatus` | Governed product lifecycle state | Closed enum: `DRAFT`, `PREVIEW`, `ACTIVE`, `DEPRECATED`, `RETIRED` |
| `capabilities` | Consumer-facing governed capabilities | Non-empty unique string list |
| `supportedClouds` | Provider-neutral target environments | Non-empty unique subset of `aws`, `azure`, `gcp`, `on-prem` |
| `securityBaseline` | Mandatory minimum security baseline | Closed object with `consumerOverridable: false` |
| `networkProfiles` | Approved connectivity profiles | Non-empty list of closed profile objects |
| `entitlementRequirements` | EP-18 multi-customer entitlement constraints | Closed object requiring `["customerId", "organizationId", "environmentId"]`, `commercialEntitlementGrantsExecution: false`, `crossCustomerSubstitutionAllowed: false` |
| `costClassification` | FinOps tier, ISO currency, chargeback, and budget guardrails | Closed object |
| `inputContract` | Bounded consumer input schema reference | Closed object with `closedObject: true` |
| `evidenceRequirements` | Required deterministic evidence artifacts and lineage rules | Closed object with `digestAlgorithm: "sha256"`, `customerScopedLineage: true`, `humanReviewRequiredForExceptions: true` |

## Internal-Only `fulfillmentBinding` Redaction Rule

`fulfillmentBinding` is an **internal-only** realization attribute and **MUST NEVER** appear on consumer, API, or MCP discovery responses.

- `GovernedProduct` enforces both `"additionalProperties": false` and an explicit `"not"` prohibition against `fulfillmentBinding` and internal implementation fields (`crossplaneAdmin`, `xrdRef`, `compositionRef`, `providerConfigRef`, `terraformState`, `terraformApply`, `iamPolicy`, `credentials`, `secretRef`).
- `fulfillmentBinding` may resolve internally behind governed platform boundaries to Crossplane, Terraform, native provider APIs, or approved workflows, but the consumer discovery contract remains strictly provider-neutral and implementation-independent.
- Any discovery payload that exposes `fulfillmentBinding` or provider-admin internals fails closed.

## Closed 8-Tool Read-Only MCP Discovery Surface

The read-only MCP discovery surface exposes **only** the following closed 8-tool catalog (`surfaceMode: "READ_ONLY_DISCOVERY"`, `readOnly: true`):

| # | Tool Name | Access Mode | Customer Scope Required | Purpose |
|---|---|---|---|---|
| 1 | `list_products` | `readOnly: true` | `customerId`, `organizationId`, `environmentId` | List entitled governed products in customer scope |
| 2 | `search_products` | `readOnly: true` | `customerId`, `organizationId`, `environmentId` | Search entitled governed products by capability, cloud, or lifecycle state |
| 3 | `get_product` | `readOnly: true` | `customerId`, `organizationId`, `environmentId` | Retrieve a single consumer-visible `GovernedProduct` descriptor |
| 4 | `get_product_version` | `readOnly: true` | `customerId`, `organizationId`, `environmentId` | Retrieve a specific versioned `GovernedProduct` descriptor |
| 5 | `get_product_requirements` | `readOnly: true` | `customerId`, `organizationId`, `environmentId` | Retrieve security baseline, network profile, input contract, and evidence requirements |
| 6 | `check_entitlement` | `readOnly: true` | `customerId`, `organizationId`, `environmentId` | Check whether a customer/organization/environment scope is entitled to discover or request a product |
| 7 | `get_product_evidence` | `readOnly: true` | `customerId`, `organizationId`, `environmentId` | Retrieve sanitized, customer-scoped product evidence summaries and digest references |
| 8 | `get_lifecycle_status` | `readOnly: true` | `customerId`, `organizationId`, `environmentId` | Retrieve current lifecycle state (`DRAFT`, `PREVIEW`, `ACTIVE`, `DEPRECATED`, `RETIRED`) |

### Zero-Authority Invariant

The root contract, the MCP catalog descriptor, and **every individual tool descriptor** enforce a closed 6-flag authority object where every flag is fixed to boolean `false` (`const: false`):

- `mayApprove: false`
- `mayMerge: false`
- `mayApply: false`
- `mayProvision: false`
- `mayGrantPrivilege: false`
- `mayChangePolicy: false`

Any tool outside the closed 8-tool enum, any `readOnly: false` flag, or any authority flag set to `true` (or non-boolean) fails closed.

## Hard Deny List

The contract embeds a mandatory 7-item hard deny list where every rule carries `decision: "DENY"` and `overridePermitted: false`:

| Operation ID | Prohibited Operation Class | Decision |
|---|---|---|
| `CROSSPLANE_ADMIN_MUTATION` | Crossplane admin, XRD, or Composition mutation | `DENY` |
| `TERRAFORM_APPLY_OR_STATE` | Terraform apply or state access/mutation | `DENY` |
| `PROVIDER_PRIVILEGED_API` | Direct cloud provider privileged API invocation | `DENY` |
| `IAM_MODIFICATION` | IAM role, principal, or policy modification | `DENY` |
| `DIRECT_INFRASTRUCTURE_PROVISION` | Direct infrastructure provisioning bypassing governed intake and validation | `DENY` |
| `SELF_APPROVAL` | Self-approval or human-review bypass | `DENY` |
| `CREDENTIAL_OR_SECRET_ACCESS` | Credential, token, or secret retrieval or exfiltration | `DENY` |

## EP-18 Multi-Customer Entitlement Scoping

Consistent with [Multi-Customer Isolation Architecture](../architecture/multi-customer-isolation.md), every discovery and entitlement operation requires the full EP-18 three-part customer scope:

```json
["customerId", "organizationId", "environmentId"]
```

- Missing, empty, partial, or unknown scope fields fail closed.
- Cross-customer queries or scope substitutions are denied (`crossCustomerAccess: "DENY_FAIL_CLOSED"`) with retained negative evidence (`retainNegativeEvidence: true`).
- Commercial software entitlement is separate from infrastructure product entitlement, and neither grants execution or production authorization (`commercialEntitlementGrantsExecution: false`).

## Explicit Claim Boundaries

- **Contract and synthetic validation posture (`SYNTHETIC_ONLY`):** This contract defines the public machine-readable schema and static fail-closed invariants for governed product discovery.
- **No execution or approval authority:** Satisfying this schema or passing its tests grants zero authority to approve requests, merge changes, apply infrastructure, provision cloud resources, grant privileges, change policies, spend cloud budget, or access credentials.
- **No production or hosted-service claim:** This contract does not claim production deployment, hosted multi-tenant SaaS operation, live cloud integration, or customer adoption acceptance.
- **Public publication boundary:** This contract is deliberately public and provider-neutral in accordance with [Public Publication Boundary](../PUBLICATION-BOUNDARY.md).
