# Product and runtime architecture

This is the authoritative end-to-end view of the Infrastructure Product Works™ Infrastructure-as-a-Product portfolio. It separates the **product experience** from the **runtime implementation** so developers can order outcomes without inheriting cloud, Kubernetes, or provider complexity.

> [!IMPORTANT]
> This is the target operating model. Current portfolio evidence remains bounded and synthetic. IaaP Guard is the supported GitHub-native product; the bounded customer-hosted Forge HTTP transport was accepted through Forge PR #96 and merged to protected `main` at `fd6452fcb7e4934695b8ed73657daf98c4f0bc28`. Direct Backstage → Console → Forge → Crossplane production execution, credentials, customer data, pilot authority, and commercial activation are not claimed here.

## Product view

```mermaid
flowchart TB
  DEV["Developer or product team"]
  STORE["Backstage storefront<br/>Browse • configure • order"]
  CONSOLE["IaaP Console<br/>Track • review • decide"]
  FORGE["IaaP Forge<br/>Translate intent into an inert proposal"]
  GUARD["IaaP Guard<br/>Validate architecture, policy, and evidence"]
  HUMAN["Authorized human<br/>Approve the exact bound proposal"]
  CONTROL["Crossplane product control plane<br/>Reconcile approved desired state"]
  OUTCOME["Infrastructure product outcome<br/>Kubernetes • network • data • identity • connectivity"]
  ASSURE["IaaP Assurance<br/>Custody • continuity • rollback • evidence"]

  DEV --> STORE
  STORE --> CONSOLE
  CONSOLE --> FORGE
  FORGE --> GUARD
  GUARD --> HUMAN
  HUMAN --> CONTROL
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
  class FORGE product
  class GUARD governance
  class HUMAN human
  class CONTROL control
  class OUTCOME outcome
  class ASSURE evidence
  linkStyle default stroke:#7DD3FC,stroke-width:2px
```

The developer orders an **outcome**, not a collection of provider resources. Backstage presents the catalog. Console presents the lifecycle. Forge proposes the implementation. Guard determines whether the proposal is admissible. An authorized person controls the material decision. Crossplane performs reconciliation only after the approved desired state crosses the execution boundary. Assurance keeps the evidence and custody chain intact.

## Technical deployment and reconciliation view

```mermaid
flowchart TB
  subgraph EXP["Customer experience plane"]
    BS["Backstage<br/>Product catalog and order entry"]
    UI["IaaP Console<br/>Lifecycle and evidence experience"]
  end

  subgraph SVC["Customer-hosted IaaP services"]
    FH["Forge HTTP adapter<br/>Bounded transport"]
    FE["Forge engine<br/>Deterministic proposal"]
    GD["Guard and Guard Core<br/>Fail-closed validation"]
    IA["IaaP Assurance<br/>Authority and custody evidence"]
  end

  subgraph GOV["Governed change boundary"]
    GH["GitHub<br/>Versioned desired state and evidence"]
    HA["Human approval<br/>Exact digest and revision"]
    GC["Authorized GitOps delivery<br/>No implicit approval"]
  end

  subgraph MGMT["Kubernetes management cluster"]
    XP["Crossplane"]
    PKG["XRDs and Compositions<br/>Stable product APIs"]
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

  BS --> UI
  UI --> FH
  FH --> FE
  FE --> GD
  GD --> GH
  GH --> HA
  HA --> GC
  GC --> PKG
  PKG --> XP
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
  XP --> IA
  WK --> IA
  MS --> IA
  IA --> UI

  classDef experience fill:#0D2438,stroke:#38BDF8,stroke-width:2px,color:#F8FAFC
  classDef service fill:#2E1752,stroke:#A855F7,stroke-width:2px,color:#F8FAFC
  classDef governance fill:#3A2A0D,stroke:#F59E0B,stroke-width:2px,color:#F8FAFC
  classDef control fill:#102D55,stroke:#3B82F6,stroke-width:3px,color:#F8FAFC
  classDef cloud fill:#12303A,stroke:#14B8A6,stroke-width:2px,color:#F8FAFC
  classDef outcome fill:#123A24,stroke:#22C55E,stroke-width:2px,color:#F8FAFC
  classDef evidence fill:#3A1530,stroke:#EC4899,stroke-width:2px,color:#F8FAFC
  class BS,UI experience
  class FH,FE,GD service
  class GH,HA,GC governance
  class XP,PKG,PRV control
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

### Plan and authorize

```mermaid
sequenceDiagram
  actor Developer
  participant Backstage
  participant Console
  participant Forge
  participant Guard

  Developer->>Backstage: Choose product and allowed parameters
  Backstage->>Console: Create bounded product order
  Console->>Forge: Submit order through customer-hosted API
  Forge-->>Console: Return inert digest-bound proposal
  Console->>Guard: Request deterministic validation
  Guard-->>Console: Return verdict and evidence
```

### Approve, reconcile, and report

```mermaid
sequenceDiagram
  participant Console
  actor Approver
  participant GitHub
  participant Crossplane
  participant Cloud

  Console->>Approver: Present exact proposal and evidence
  Approver->>GitHub: Approve versioned desired state
  GitHub->>Crossplane: Deliver approved declaration
  Crossplane->>Cloud: Reconcile through scoped provider identity
  Cloud-->>Crossplane: Return conditions and resource status
  Crossplane-->>Console: Return sanitized status and evidence
```

## Implementation status boundary

| Capability | Current portfolio position |
|---|---|
| Backstage product ordering | Bounded POC with runtime dry-run evidence; no infrastructure apply authority |
| Console | Customer-hosted synthetic visibility and evidence projections; non-authoritative |
| Forge | Deterministic proposal engine with bounded loopback-only customer-hosted HTTP parity accepted through PR #96; no deployment authority |
| Guard | Supported GitHub-native deterministic architecture and evidence check |
| Crossplane | Credential-free contracts, bundles, simulations, and bounded reconciliation evidence |
| Live end-to-end provisioning | Separately governed target; not authorized or claimed by this diagram |

The stable center is the **infrastructure product contract**. Backstage, Console, GitHub workflows, models, providers, and individual cloud implementations may evolve without forcing developers to relearn how to order the outcome.
