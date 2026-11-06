# IPW portfolio-agent instructions

This repository maintains the public architecture and portfolio thesis of Infrastructure Product Works. Read the documentation relevant to the task rather than loading the full repository.

For executive product, portfolio, strategy, architecture, risk, delivery, or operating decisions, discover the relevant workflow in `.agents/skills/` and use the corresponding `SKILL.md`. The selection matrix and evidence contract are in [docs/executive/AGENT-SKILLS-OPERATING-CONTRACT.md](docs/executive/AGENT-SKILLS-OPERATING-CONTRACT.md). Skills are reusable work instructions, not new identities or standing permissions.

Prioritize an observed customer problem and the connected request-to-ready infrastructure-product journey. Separate evidence from assumptions, simulated tests from hosted acceptance, and approved customer use from plans. Do not turn unmeasured OKRs into achieved results. Keep the Readiness Diagnostic offer separate from the managed service.

Respect product contracts and boundaries in docs/OPERATING-MODEL.md, docs/GOVERNED-AGENTIC-INTEROPERABILITY.md, docs/PRODUCT-ARCHITECTURE.md, and docs/INFRASTRUCTURE-PRODUCT-LIFECYCLE.md as applicable. Guard validates; it does not grant execution authority. Human selection and authorization, deterministic checks, and native security vetoes are separate gates. A skill, PR approval, green CI, or simulation cannot authorize cloud spend, production activation, customer adoption, credential changes, or privileged infrastructure operations.

Check live revisions/ownership before edits; preserve work in progress. Use branches/PRs, tests, evidence and protected-branch rules. Confirm actual merge and deployments independently. Never fabricate customer demand, operator acceptance, active services, or production readiness.
