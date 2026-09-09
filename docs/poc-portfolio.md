# POC Portfolio

The program separates responsibilities into bounded repositories so each architectural claim can be tested independently without turning the program hub into another implementation monolith.

> **IaaS is what we buy; infrastructure-as-a-product is what we build. Backstage is where developers shop.**

```mermaid
flowchart TB
  HUB["ai-powered-infrastructure-as-a-product<br/>thesis • architecture • evidence"]
  GUARD["iaap-guard<br/>public product surface"]
  CONSOLE["iaap-console<br/>evidence • review • selection"]
  ASSURANCE["iaap-assurance<br/>authority • custody • continuous assurance"]
  CORE["iaap-guard-core<br/>private hosted runtime"]
  FORGE["iaap-forge<br/>product-building system"]
  STORE["backstage-infrastructure-product-storefront-poc"]
  SEED["crossplane-multicloud-seed-poc"]
  PRODUCT["multicloud-foundation-product-poc"]
  AI["composite-ai-infrastructure-product-poc"]
  INT["multicloud-foundation-poc-integration"]
  ADOPTER["iaap-guard-adopter-validation<br/>archived proof"]
  OUT["platform product outcomes<br/>NPS • time • adoption • escape rate"]

  HUB --> GUARD
  GUARD --> CORE
  GUARD --> CONSOLE
  CONSOLE --> FORGE
  FORGE --> ASSURANCE
  FORGE --> STORE
  FORGE --> SEED
  FORGE --> PRODUCT
  FORGE --> AI
  STORE --> INT
  SEED --> INT
  PRODUCT --> INT
  AI --> INT
  ADOPTER -. validates .-> GUARD
  INT --> OUT
  OUT --> HUB

  classDef front fill:#0D2438,stroke:#38BDF8,stroke-width:3px,color:#F8FAFC
  classDef public fill:#123A24,stroke:#22C55E,stroke-width:2px,color:#F8FAFC
  classDef private fill:#2E1752,stroke:#A855F7,stroke-width:2px,color:#F8FAFC
  classDef internal fill:#102D55,stroke:#3B82F6,stroke-width:2px,color:#F8FAFC
  classDef poc fill:#3A2A0D,stroke:#F59E0B,stroke-width:2px,color:#F8FAFC
  classDef archived fill:#1F2937,stroke:#94A3B8,stroke-width:2px,color:#CBD5E1
  classDef outcome fill:#3A1530,stroke:#EC4899,stroke-width:2px,color:#F8FAFC

  class HUB front
  class GUARD public
  class CORE,CONSOLE,FORGE,ASSURANCE private
  class STORE,SEED,PRODUCT,AI,INT poc
  class ADOPTER archived
  class OUT outcome
  linkStyle default stroke:#7DD3FC,stroke-width:2px
```

## Product repositories around the POCs

- [`iaap-guard`](https://github.com/InfrastructureProductWorks/iaap-guard) is the active public product, adoption, contract, support, security, and sanitized assurance surface.
- [`iaap-guard-core`](https://github.com/InfrastructureProductWorks/iaap-guard-core) is the protected private engine, hosted GitHub App runtime, deployment, internal test, and operational-evidence repository.
- [`iaap-console`](https://github.com/InfrastructureProductWorks/iaap-console) owns the customer-hosted evidence, review, selection, and traceability experience.
- [`iaap-forge`](https://github.com/InfrastructureProductWorks/iaap-forge) consumes bounded Guard evidence and owns the active product-building, Composite AI, GitHub governance, Crossplane lifecycle, and outcome system.
- [`iaap-assurance`](https://github.com/InfrastructureProductWorks/iaap-assurance) owns bounded authority, protected-data custody, and continuous assurance. Its sanitized Gate 6 prerelease was accepted under the former Vanguard Suite name and remains pinned at `gate-6-bounded-pass-2026-09-02` / `f96961c47f6866dd12025eca8afc43b376163520`; the acceptance is only `PASSED_FOR_BOUNDED_SYNTHETIC_PROOF`.
- [`iaap-guard-adopter-validation`](https://github.com/InfrastructureProductWorks/iaap-guard-adopter-validation) is archived clean-adopter proof, not an active runtime or supported distribution.
- [`ai-powered-infrastructure-as-a-product`](https://github.com/InfrastructureProductWorks/ai-powered-infrastructure-as-a-product) remains the public thesis, architecture, evidence, and portfolio front door.

## Portfolio lifecycle register

Evidence status, product maturity, and permission to operate are separate decisions. A passed test or evidence gate does not by itself make a capability a supported release, authorize a pilot, or authorize production use.

The controlled product lifecycle is:

`Concept → POC → Preview → Release Candidate → Supported Release → Maintenance → Retired`

Operational authorization is recorded separately:

`Synthetic Only → Bounded Evaluation → Pilot Authorized → Production Authorized`

| Application or capability | Product lifecycle | Current operational authorization | Next exit gate |
|---|---|---|---|
| IaaP Guard and Guard Core | Supported Release | Bounded Evaluation through the supported GitHub-native product boundary | Continue release, security, support, and adoption evidence; any broader operating authority requires a separate decision. |
| IaaP Forge | Preview | Synthetic Only; installable loopback-only nonproduction HTTP transport and inert proposals | Validate and authorize a network-exposed customer-hosted evaluation surface without adding provisioning authority. |
| IaaP Console | POC | Synthetic Only; evidence, review, selection, and traceability projections | Validate an authenticated bounded Forge adapter and separately authorize external evaluation. |
| Backstage Storefront | POC | Synthetic Only; catalog and dry-run order generation | Validate a bounded client adapter and an authorized human-reviewed order submission path. |
| IaaP Assurance | Preview | Synthetic Only; bounded prerelease custody and authority proof | Validate customer-hosted identity, custody, operational evidence, recovery, and support before any named pilot. |
| Crossplane bootstrap and product APIs | POC | Bounded Evaluation in controlled sandboxes; no production delivery authority | Establish a named pilot target, scoped identity, SLOs, recovery, support ownership, and explicit pilot authorization. |
| Composite AI capability | POC | Synthetic Only, including bounded synthetic fixtures through the limited live-model adapter | Validate repeatable evaluation quality, cost controls, model governance, and human-review safeguards for a named evaluation. |
| Complete Backstage-to-Crossplane journey | POC | Synthetic Only; no pilot or production authority | Obtain separate named-pilot authorization with exact revision, digest, target, delivery window, SLOs, recovery, support, monitoring, and rollback. |

A component advances only when its stated exit gate has objective evidence and the required authority decision is recorded. A lifecycle advance does not silently expand credentials, target environments, customer-data access, spending, approval, apply, provisioning, pilot, or production authority.

## Supporting POC governance

As of September 3, 2026, the default branches of `crossplane-multicloud-seed-poc`, `multicloud-foundation-product-poc`, and `composite-ai-infrastructure-product-poc` are protected by active rulesets with no bypass actors. Each requires pull requests, resolved review conversations, and an up-to-date `validate` check; branch deletion and force pushes are blocked. These controls change repository governance only and add no collaborator, credential, token scope, visibility, runtime, or production access.

## Responsibilities

### `backstage-infrastructure-product-storefront-poc`

Owns the optional reference **consumer experience** for infrastructure products: browse, configure, order, and track.

The storefront:

- presents curated product-level inputs;
- emits a narrow `InfrastructureProductOrder` artifact;
- can open a human-reviewable GitHub order path when publication is intentionally enabled with an authorized integration;
- hides Crossplane, ProviderConfig, cloud credentials, IAM JSON, Terraform/TFE, and composition internals; and
- never becomes the provisioning control plane.

Backstage is therefore a replaceable experience layer. A CLI, API, service portal, or conversational interface could submit the same product intent without changing the product-control-plane architecture.

The storefront repository now also carries a bounded runtime smoke that starts an actual Backstage backend, registers the reference template in the Software Catalog, and executes `fetch:template` plus `publish:github:pull-request` through Backstage's supported dry-run path. That runtime evidence deliberately provides no real GitHub write credential and creates no real order PR.

### `crossplane-multicloud-seed-poc`

Owns the minimal trusted Crossplane runtime. No product APIs, cloud credentials, production, consumer storefront, or TFE dependency.

### `multicloud-foundation-product-poc`

Owns the `CloudFoundationEnvironment` contract, provider-specific implementations, policy, examples, product status, and lifecycle experiments.

### `composite-ai-infrastructure-product-poc`

Owns bounded request, review, operations, and evidence-agent contracts and evaluations. No direct execution authority.

### `iaap-assurance`

Owns authority, protected-data custody, and continuous assurance across the bounded portfolio evidence relationship. Gate 6 is accepted only for the deterministic synthetic proof at prerelease `gate-6-bounded-pass-2026-09-02` and closure SHA `f96961c47f6866dd12025eca8afc43b376163520`.

That acceptance does not authorize a pilot, live personal data, production connectors, organization-specific policy, live telemetry, credentials, cloud access, external delivery, or autonomous production action. Guard remains the deterministic assessment surface; Console remains the customer-hosted evidence and selection experience; Forge remains the governed product-building lifecycle; Storefront remains the optional reference consumer experience.

### `multicloud-foundation-poc-integration`

Owns pinned upstream integration, including the storefront handoff, clean-cluster acceptance, active network-policy proof, AI authority checks, simulated reconciliation, evidence, teardown, scorecard, cross-repository storefront/product contract compatibility, and workflow/bootstrap reproducibility checks.

The repository also retains the trusted-main managed-interconnect safety proof. One deterministic synthetic AWS/Azure profile passes the exact accepted Forge → Guard path, while thirteen unsafe address, route, resilience, DNS, encryption, identity, coordinate, and authority profiles fail closed. This remains an inert validation result, not a live-cloud connection or provisioning path.

The trusted-main Phase 24 proof also preserves Forge's `v1alpha1` renderer byte-for-byte while validating a detached selection-evidence envelope across Guard, Console, recorded human selection, Forge, and the existing IaaP Assurance custody reference. The accepted Guard source revision and the distinct synthetic subject revision are separately bound; producer, journey, custody, tamper, cross-selection, and source-substitution failures are rejected. The proof establishes canonical byte relationships, not a cryptographically authenticated human identity or operational authority.

The integrated consumer path is:

```mermaid
flowchart LR
  DEV[Developer] --> STORE[Backstage storefront]
  STORE --> ORDER[InfrastructureProductOrder]
  ORDER --> AI[Bounded Composite AI]
  AI --> POLICY[Deterministic validation]
  POLICY --> HUMAN[Human approval boundary]
  HUMAN --> API[CloudFoundationEnvironment]
  API --> XP[Crossplane]
  XP --> STATUS[Status + evidence]
  STATUS --> STORE
  STATUS --> OUTCOMES[Product outcome evidence]
  OUTCOMES --> NPS[Developer NPS]
  OUTCOMES --> TTP[Time-to-Provision]
  OUTCOMES --> ADOPT[Internal adoption]
  OUTCOMES --> ESCAPE[Exception / escape rate]
```

### Platform product outcomes

Product success is measured by developer outcomes in addition to engineering and runtime health. The minimum outcome set is Developer NPS, Order-to-Ready and Approval-to-Ready Time-to-Provision, Internal Adoption Rate, Repeat Consumption Rate, and Exception / Escape Rate.

Infrastructure code volume is an implementation activity metric, not a product-success metric. Terraform lines of code, number of modules, pipelines, pull requests, and tickets can help manage engineering work but do not prove that the platform is useful, fast, adopted, or preferred.

The detailed measurement and telemetry contract is defined in [Platform Product Outcomes](platform-product-outcomes.md).

### `ai-powered-infrastructure-as-a-product`

Owns the thesis, architecture, product operating model, decisions, frozen evidence baselines, portfolio boundaries, outcome measurement model, and investment framing. It intentionally does not duplicate runtime implementation code.

## Product-system mental model

| Layer | Reference implementation | Responsibility |
|---|---|---|
| Program | `ai-powered-infrastructure-as-a-product` | Thesis, architecture, evidence, decisions, roadmap framing. |
| Guard product | `iaap-guard` | Public product, contracts, adoption, support, security, and assurance. |
| Guard implementation | `iaap-guard-core` | Private deterministic engine, hosted runtime, deployment, and regression evidence. |
| Product builder | `iaap-forge` | Guard consumption, bounded Composite AI, governed proposals, Crossplane lifecycle, and outcomes. |
| Assurance authority | `iaap-assurance` | Authority, protected-data custody, and continuous assurance within explicitly accepted bounds. |
| Experience | `backstage-infrastructure-product-storefront-poc` | Browse, configure, order, track. |
| Intelligence | `composite-ai-infrastructure-product-poc` | Interpret, propose, review, explain, diagnose, evidence. |
| Governance | GitHub + deterministic policy + people | Change, tests, approval, traceability. |
| Product contract | `multicloud-foundation-product-poc` | Stable infrastructure-product API and lifecycle semantics. |
| Control plane | Crossplane | Reconciliation and product status. |
| Bootstrap | `crossplane-multicloud-seed-poc` | Minimal trusted runtime required for the control plane. |
| Acceptance | `multicloud-foundation-poc-integration` | End-to-end evidence across the bounded components. |
| Retained validation | `iaap-guard-adopter-validation` | Archived clean-adopter proof for Guard. |
| Outcomes | Cross-layer telemetry + developer feedback | Developer NPS, Time-to-Provision, adoption, repeat use, exceptions. |
| Realization | AWS / Azure / GCP | Cloud-native services and enforcement. |

## Evidence gates

1. **Credential-free control-plane integration** — passed and retained as v1.
2. **Storefront-to-product integration** — passed as historical v2.
3. **Storefront/product accepted-domain compatibility** — corrected and passed as historical v3 across Kubernetes 1.34/1.35/1.36 at 100/100.
4. **Workflow/bootstrap supply-chain reproducibility** — passed as historical v4 across Kubernetes 1.34/1.35/1.36 at 100/100, with immutable GitHub Action revisions, pinned Python, hash-locked CI dependencies, and publisher SHA-256 verification for Kind/kubectl/Helm.
5. **Backstage runtime smoke + repinned integration** — **passed as current v5**. An actual Backstage backend registered and dry-ran the reference template/action without a real GitHub write credential, and the resulting merged storefront revision was pinned into a fresh hardened Kubernetes 1.34/1.35/1.36 integration run that remained 100/100.
6. **Product live-cloud readiness corrections** — **passed** in integration run `31256619696` across Kubernetes 1.34/1.35/1.36 at 100/100. The product now enforces semantic RFC1918 CIDR validity/containment, platform-owned lifecycle policy, neutral observed-evidence-only TFE comparison inputs, and explicit expected admission-denial evidence.
7. **Platform product outcome instrumentation** — **passed for the bounded pre-production evidence contract**. POC timing may be labeled `poc-observed`; Developer NPS, adoption, repeat use, and real exception behavior remain `not-observed` until an actual developer population exists.
8. **Live AWS sandbox** — **passed** with workload identity, retained sanitized evidence, and verified teardown.
9. **Live Azure and GCP sandboxes** — **passed** with workload identity, retained sanitized evidence, and verified teardown.
10. **Live model adapter** — **passed** on Vertex AI in `us-east4` using synthetic fixtures only and a fixed model-usage ceiling.
11. **HCP Terraform Free remote-run proxy** — **proxy passed** with a zero-resource fixture, protected VCS status, sanitized evidence, workspace deletion, and token revocation. Terraform Enterprise was not accessed or validated.
12. **Phase 20 architecture reconciliation** — **complete** at pinned Forge revision `6fb587cb3f521e99c33039c61090fe8b738836cc`, preserving the frozen Guard boundary and public sanitized claims.
13. **IaaP Assurance Gate 6 portfolio custody** — **passed only for the bounded synthetic proof** at prerelease `gate-6-bounded-pass-2026-09-02` and closure SHA `f96961c47f6866dd12025eca8afc43b376163520`. The gate was accepted under the former Vanguard Suite name; versioned historical identifiers remain unchanged. The public map pins the sanitized record by digest and preserves IaaP Assurance ownership of authority, custody, and continuous assurance without changing Guard, Console, Forge, or Storefront responsibilities.
14. **Managed AWS/Azure interconnect** — **passed only for one bounded deterministic synthetic profile**. The [Step 4 public closure record](https://github.com/InfrastructureProductWorks/ai-powered-infrastructure-as-a-product/blob/main/artifacts/phase-23/managed-interconnect-closure.json) binds the sanitized proof digests and accepted private revision commitments, records all thirteen unsafe profiles as `FAIL_CLOSED`, and preserves the existing IaaP Assurance custody/authority reference. Forge and Guard Core contain the minimal contract/validation change; IaaP Assurance, Console, and Storefront remain unchanged.
15. **Versioned human-selection traceability** — **passed only for the bounded synthetic proof**. The [Phase 24 public closure record](https://github.com/InfrastructureProductWorks/ai-powered-infrastructure-as-a-product/blob/main/artifacts/phase-24/selection-evidence-closure.json) binds the accepted Guard source, distinct synthetic subject, recorded selection, Forge product output, producer evidence, complete journey, and IaaP Assurance custody manifest while preserving the existing `v1alpha1` renderer byte-for-byte. Golden and migration cases pass; unsafe substitutions and rewrites fail closed. Guard, Console, Storefront, and IaaP Assurance implementation remain unchanged.
16. **Production pilot** — future and unauthorized; requires separate authorization, SLOs, recovery, support, lifecycle evidence, Developer NPS, adoption, and repeat-consumption evidence.

Downloadable workflow archives remain subject to their source repository retention windows. The accepted public digests and reproducible manifests remain committed; any longer-lived private archive requires a separate custody, access, retention, recovery, deletion, and spending decision.

The v5 runtime proof is intentionally narrower than a production Backstage deployment: the GitHub publication action ran in dry-run mode, no browser/UI journey was executed, and the generated Backstage dependency graph is not claimed immutable across future runs.

See [POC Baseline Lineage](poc-baselines/README.md) for the frozen evidence history.

## Boundary principle

> **The storefront is where the consumer shops. The product API defines what is being bought. Crossplane controls the product lifecycle. The cloud realizes it. Success is measured by developer outcomes, not infrastructure code volume.**
