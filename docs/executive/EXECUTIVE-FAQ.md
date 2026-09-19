# Executive FAQ

## Why isn't Terraform, Crossplane, or another infrastructure-as-code platform enough?

Those tools can provision and reconcile infrastructure. They do not, by themselves, define the consumer, product outcome, lifecycle ownership, support model, economics, evidence expectations, roadmap, or executive accountability of an infrastructure product.

IaaP treats provisioning technology as an implementation mechanism beneath a stable product contract.

## Why not just use the cloud provider's landing-zone or foundation tooling?

Provider tooling can be valuable and should be reused where appropriate. IaaP addresses the enterprise layer above any single provider: product semantics, ownership, lifecycle, governance, evidence, multi-cloud boundaries, consumer experience, and integration with the organization's approval and operating model.

The goal is not to recreate provider capabilities.

## Are we building another platform?

Potentially, which is why adoption must be evidence-driven.

The intended design minimizes that risk by keeping the stable product contract separate from replaceable experience and implementation mechanisms. Existing enterprise systems should remain authoritative where they already perform a function well.

If the suite cannot demonstrate enough reuse, adoption, control improvement, or economic value to justify its operating cost, leadership should constrain or stop it.

## Why not use Backstage or an IT service catalog as the solution?

A storefront or catalog can improve discovery and ordering, but the storefront is not the infrastructure product. It should not own cloud credentials, reconciliation, policy authority, or lifecycle state merely because it captures the request.

IaaP can integrate with Backstage, an enterprise portal, API, CLI, conversational interface, or ITSM catalog without making any one of those the permanent product boundary.

## Is this just platform engineering with a different name?

IaaP overlaps with platform engineering but makes a narrower claim: infrastructure capabilities should be managed as products with explicit consumers, contracts, lifecycle ownership, economics, governance, evidence, and measurable outcomes.

An organization can practice platform engineering without consistently treating infrastructure capabilities as products. IaaP is intended to make that product discipline explicit and executable.

## Why is AI included?

AI can reduce friction in translating intent, detecting missing information, explaining policy results, diagnosing sanitized conditions, assembling evidence, and identifying repeated product friction.

AI is deliberately not the final authority.

> **AI proposes and explains. Deterministic controls validate. Authorized people approve. The product plane binds execution authority. The Customer Execution Layer reconciles only the current authorized effects. Cloud-native controls enforce.**

The product model remains useful even if a customer limits or removes AI capabilities.

## Does this create vendor lock-in?

The design attempts to reduce lock-in at the consumer boundary by keeping the product contract stable while allowing provider and execution implementations to differ.

Lock-in is not eliminated. Every implementation choice has switching costs. The executive question is whether those choices remain replaceable without forcing consumers to relearn the product or losing lifecycle and evidence continuity.

## Does multi-cloud mean lowest-common-denominator infrastructure?

No. Common consumer semantics should not erase provider-native strengths.

The suite aims to standardize what the consumer should be able to expect while allowing AWS, Azure, and GCP to satisfy those expectations differently where provider behavior or organizational policy requires it.

## What happens to existing infrastructure?

The preferred adoption model supports attaching to existing foundations where they meet required boundaries. New foundation vending should be used only when justified.

IaaP should not require unnecessary migration simply to prove the model.

## Who owns IaaP?

Ownership should be explicit and divided by responsibility:

- executive sponsorship for strategic direction and investment;
- product ownership for roadmap, adoption, lifecycle, economics, and outcomes;
- responsible engineering for technical quality and compatibility;
- security/control authorities for policy and risk decisions;
- operations for service health, incidents, recovery, and support; and
- consumers for demand, feedback, and outcome validation.

## What would make leadership stop the initiative?

Examples include:

- weak or artificial demand;
- no material improvement over existing delivery;
- operating cost that exceeds realized value;
- unacceptable security or reliability risk;
- persistent need for manual intervention that defeats the product model;
- low reuse after the first implementation;
- authority conflicts that cannot be resolved; or
- inability to demonstrate measurable business outcomes.

## What should leadership approve first?

A bounded pilot with a real consumer, named owners, a measurable baseline, explicit authority boundaries, and a scheduled scale/refine/constrain/stop decision.
