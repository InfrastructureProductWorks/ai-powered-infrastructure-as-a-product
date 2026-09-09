# Product and runtime architecture

This is the authoritative end-to-end view of the Infrastructure Product Works™ Infrastructure-as-a-Product portfolio. It separates the **product experience** from the **runtime implementation** so developers can order outcomes without inheriting cloud, Kubernetes, or provider complexity.

> [!IMPORTANT]
> This is the target operating model. Current portfolio evidence remains bounded and synthetic. IaaP Guard is the supported GitHub-native product. Forge ships an installable, loopback-only, nonproduction HTTP preview. Network-exposed service distribution and Console or Backstage client adapters remain targets. Direct Backstage → Console → Forge → Crossplane production execution, credentials, customer data, pilot authority, and commercial activation are not claimed here.

## Product view

```mermaid
flowchart TB
  DEV["Developer or product team"]
  STORE["Backstage storefront<br/>Browse • configure • order"]
  ORDER["InfrastructureProductOrder"]
  GUARD["IaaP Guard GitHub App<br/>Architecture and evidence assessment"]
  CONSOLE["IaaP Console<br/>Evidence and selection experience"]
  SELECT["Authorized human selection"]
  FORGE["IaaP Forge<br/>Create inert bound proposal"]
  REVISION["Versioned GitHub proposal<br/>Reviewable candidate"]
  FINAL["Protected finalization<br/>Immutable delivery revision"]
  VALIDATE["Forge deterministic gates<br/>Final revision • digest • target • window"]
  APPROVE["Authorized human approval<br/>Same revision • digest • target • window"]
  DELIVERY["Authorized GitOps delivery<br/>Enforce complete approval binding"]
  CONTROL["Crossplane in Kubernetes<br/>Reconcile approved product claim"]
  OUTCOME["Infrastructure product outcome<br/>Kubernetes • network • data • identity • connectivity"]
  ASSURE["IaaP Assurance<br/>Custody • continuity • rollback • evidence"]

  DEV --> STORE
  STORE --> ORDER
  GUARD --> CONSOLE
  CONSOLE --> SELECT
  ORDER --> FORGE
  SELECT --> FORGE
  FORGE --> REVISION
  REVISION --> FINAL
  FINAL --> VALIDATE
  VALIDATE --> APPROVE
  APPROVE --> DELIVERY
  DELIVERY --> CONTROL
  CONTROL --> OUTCOME
  OUTCOME --> ASSURE
  ASSURE --> CONSOLE

  classDef experience fill:#0D2438,stroke:#38BDF8,stroke-width:2px,color:#F8FAFC
  classDef product fill:#2E1752,stroke:#A855F7,stroke-width:2px,color:#F8FAFC
  classDef governance fill:#3A2A0D,stroke:#F59E0B,stroke-width:2px,color:#F8FAFC
  classDef human fill:#47270F,stroke:#FB923C,stroke-width:2px,color:#F8FAFC
  classDef control fill:#102D55,stroke:#3B82F6,stroke-width:3px,color:#F8FAFC
  classDef outcome fill:#123A24,stroke:#22C55E,stroke-width:2px,color:#F8FAFC
  classDef evidence fill:#3A1530,stroke:#EC4899,stroke-width:2px,color:#F8FAFC
  class DEV,STORE,CONSOLE experience
  class ORDER,FORGE product
  class GUARD,REVISION,FINAL,VALIDATE governance
  class SELECT,APPROVE human
  class DELIVERY governance
  class CONTROL control
  class OUTCOME outcome
  class ASSURE evidence
  linkStyle default stroke:#7DD3FC,stroke-width:2px
```

The developer orders an **outcome**, not a collection of provider resources. Backstage captures product intent. Separately, Guard produces architecture and planning evidence through its supported GitHub-native boundary; Console presents that evidence for human selection. Forge consumes the order and accepted selection to create an inert proposal. That proposal is finalized through the protected GitHub path into an immutable delivery revision before approval. Forge’s deterministic gates validate that final revision, artifact digest, authorized target, and delivery window; an authorized person approves the same complete binding. GitOps verifies all four values before delivering the claim to Crossplane. There is no content-changing merge after approval. Any change to content, revision, digest, target, or window invalidates the prior validation and approval and restarts the gate. Assurance keeps the authority and custody chain intact.

## Technical deployment and reconciliation view

```mermaid
flowchart TB
  subgraph EXP["Customer experience plane"]
    BS["Backstage<br/>Product catalog and order entry"]
    UI["IaaP Console<br/>Lifecycle and evidence experience"]
  end

  subgraph GUARDPLANE["GitHub-native assessment boundary"]
    GPR["GitHub pull request"]
    GAPP["IaaP Guard GitHub App<br/>Bounded AWS runtime"]
    GE["Versioned Guard evidence"]
  end

  subgraph SVC["Customer-hosted Forge boundary"]
    FH["Forge HTTP adapter<br/>Bounded transport"]
    FE["Forge engine<br/>Deterministic proposal"]
    FV["Forge deterministic validation<br/>Final revision • digest • target • window"]
    FA["Target status adapter<br/>Normalize operational facts"]
  end

  subgraph GOV["Governed change boundary"]
    GH["GitHub proposal<br/>Versioned desired state and evidence"]
    PM["Protected finalization<br/>Create immutable delivery revision"]
    HA["Human approval<br/>Same revision • digest • target • window"]
    GC["Authorized GitOps delivery<br/>Verify complete approval binding"]
  end

  subgraph MGMT["Kubernetes management cluster"]
    CLAIM["Approved product claim<br/>Per-order desired state"]
    XP["Crossplane"]
    PKG["Installed XRDs and Compositions<br/>Stable product APIs"]
    PRV["Provider packages<br/>Workload identity"]
  end

  subgraph DEST["Delivery targets"]
    C1["AWS"]
    C2["Azure"]
    C3["Google Cloud"]
    C4["Approved on-premises"]
  end

  subgraph RUN["Delivered product outcomes"]
    WK["Kubernetes workload clusters<br/>Namespaces • policies • platform services"]
    MS["Managed services<br/>Network • data • identity • DNS • connectivity"]
  end

  IA["IaaP Assurance<br/>Authority and custody evidence"]

  BS -. future adapter .-> FH
  GPR --> GAPP
  GAPP --> GE
  GE --> UI
  UI -. future adapter .-> FH
  FH --> FE
  FE --> GH
  GH --> PM
  PM --> FV
  FV --> HA
  HA --> GC
  GC -- verified revision, digest, target, window --> CLAIM
  CLAIM --> XP
  PKG -.-> XP
  XP --> PRV
  PRV --> C1
  PRV --> C2
  PRV --> C3
  PRV --> C4
  C1 --> WK
  C2 --> WK
  C3 --> WK
  C4 --> WK
  C1 --> MS
  C2 --> MS
  C3 --> MS
  C4 --> MS
  XP --> FA
  WK --> FA
  MS --> FA
  FA --> IA
  IA --> UI

  classDef experience fill:#0D2438,stroke:#38BDF8,stroke-width:2px,color:#F8FAFC
  classDef service fill:#2E1752,stroke:#A855F7,stroke-width:2px,color:#F8FAFC
  classDef governance fill:#3A2A0D,stroke:#F59E0B,stroke-width:2px,color:#F8FAFC
  classDef control fill:#102D55,stroke:#3B82F6,stroke-width:3px,color:#F8FAFC
  classDef cloud fill:#12303A,stroke:#14B8A6,stroke-width:2px,color:#F8FAFC
  classDef outcome fill:#123A24,stroke:#22C55E,stroke-width:2px,color:#F8FAFC
  classDef evidence fill:#3A1530,stroke:#EC4899,stroke-width:2px,color:#F8FAFC
  class BS,UI experience
  class FH,FE,FA service
  class GPR,GAPP,GE,FV,GH,HA,PM,GC governance
  class CLAIM,XP,PKG,PRV control
  class C1,C2,C3,C4 cloud
  class WK,MS outcome
  class IA evidence
  linkStyle default stroke:#94A3B8,stroke-width:2px
```

### Why Kubernetes appears twice

Kubernetes has two distinct roles in this architecture:

1. The **management cluster** hosts Crossplane and its product APIs. Crossplane watches approved claims and reconciles them through provider packages.
2. A **workload cluster** may be one of the infrastructure products delivered by Crossplane. It is a destination, not the place where a developer directly operates the management control plane.

Crossplane can also deliver managed services that do not run inside Kubernetes, including networks, databases, storage, identities, DNS, encryption resources, and managed connectivity.

## Authority and responsibility

| Component | Owns | Does not own |
|---|---|---|
| Backstage | Product discovery, permitted configuration, order entry | Cloud or Kubernetes provisioning |
| IaaP Console | Order state, proposal and evidence presentation, human workflow | Forge logic, Guard verdicts, silent approval, or reconciliation |
| IaaP Forge | Deterministic product proposals and lifecycle artifacts | Approval, cloud credentials, apply, or provisioning |
| IaaP Guard | Deterministic architecture, policy, authority, and evidence validation | Human authorization or infrastructure execution |
| GitHub and GitOps | Versioned change, review record, approved desired-state delivery | Product definition or hidden policy bypass |
| Authorized human | Acceptance or rejection of the exact material change | Undocumented override of deterministic gates |
| Crossplane | Continuous desired-state reconciliation and lifecycle status | Storefront experience, business approval, or product selection |
| Kubernetes management cluster | Runtime for the Crossplane control plane | Automatic authority to administer workload environments |
| Cloud-native IAM and controls | Final technical enforcement | Redefinition of the consumer product contract |
| IaaP Assurance | Authority, custody, safeguard continuity, rollback, and evidence chain | Storefront, proposal generation, or cloud provisioning |

## Order-to-outcome sequence

### Accepted synthetic Guard-to-Forge chain

```mermaid
sequenceDiagram
  participant Guard
  participant Console
  actor Selector
  participant Forge

  Guard->>Console: Import pinned evidence and planning report
  Console->>Selector: Present traceable findings and candidates
  Selector->>Console: Select the exact planning item
  Console->>Forge: Submit digest-bound selection evidence
  Forge-->>Console: Return inert product proposal
```

### Target authorization and delivery handoff

```mermaid
sequenceDiagram
  participant ForgeGate as Forge validation
  actor Approver
  participant GitHub
  participant GitOps
  participant Crossplane

  GitHub->>GitHub: Protected finalization creates delivery revision
  GitHub->>ForgeGate: Present final revision, digest, target, and window
  ForgeGate-->>GitHub: Bind passing validation to all four values
  Approver->>GitHub: Approve the same complete binding
  GitHub->>GitOps: Release exact revision and approval envelope
  GitOps->>GitOps: Verify revision, digest, target, and window
  GitOps->>Crossplane: Apply within window to approved management cluster
```

### Target runtime evidence return

```mermaid
sequenceDiagram
  participant Crossplane
  participant Cloud
  participant ForgeAdapter as Forge status adapter
  participant Assurance
  participant Console

  Crossplane->>Cloud: Reconcile through scoped provider identity
  Cloud-->>Crossplane: Return conditions and resource status
  Crossplane-->>ForgeAdapter: Supply bounded status facts
  ForgeAdapter-->>Assurance: Normalize and bind evidence
  Assurance-->>Console: Present custody-bound status and evidence
```

## Implementation status boundary

| Capability | Current portfolio position |
|---|---|
| Backstage product ordering | Bounded POC with runtime dry-run evidence; no infrastructure apply authority |
| Console | Customer-hosted synthetic visibility and evidence projections; non-authoritative |
| Forge | Deterministic proposal engine with an installable loopback-only nonproduction HTTP preview; no network-exposed service, client adapter, or deployment authority is claimed |
| Guard | Supported GitHub-native deterministic architecture and evidence check |
| Crossplane | Credential-free contracts, bundles, simulations, and bounded reconciliation evidence |
| Live end-to-end provisioning | Separately governed target; not authorized or claimed by this diagram |

The stable center is the **infrastructure product contract**. Backstage, Console, GitHub workflows, models, providers, and individual cloud implementations may evolve without forcing developers to relearn how to order the outcome.
