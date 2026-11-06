# IPW Executive Skills Library

The reusable executive skills live here for Codex-compatible repository-local discovery. Each `<skill>/SKILL.md` uses Agent Skills `name` and `description` frontmatter. `AGENTS.md` routes work without importing all skills into every task.

These skills are **not** independent executives, installed ChatGPT plugins, authorization grants, or autonomous background workers. ChatGPT and other orchestrators must intentionally fetch and apply the skill instructions; a file in this repo is not automatically loaded by a separate automation or another repository.

| Skill | Accountable function | When to apply |
| --- | --- | --- |
| ipw-strategic-decisions | CEO / Strategy / Finance | Portfolio investment, pivot, competitive and opportunity analysis |
| ipw-product-discovery | Product / Revenue | Customer outcome, buyer evidence, pilot acceptance and prioritization |
| ipw-architecture-review | CTO / Architecture | API-first design, interoperability, technical boundaries, ADRs |
| ipw-security-assurance | CISO / Quality | Trust, policy, custody, denial and acceptance reviews |
| ipw-delivery-execution | Engineering leadership | Exact-head PR work, tests and source acceptance |
| ipw-environment-operations | COO / Platform operations | Dev/test/prod isolation, promotion, rollback, service readiness |
| ipw-executive-review | Executive Council / Chief of Staff | Cross-functional decision, dissent, gate and evidence review |

Use the smallest relevant skill set, never all seven by default. For mixed work the accountable Product/Technology owner coordinates other functions and records any disagreements. Skill text is source-controlled, read-only guidance to the agent; product authorization remains external.

Contract/evaluation: [executive operating contract](../../docs/executive/AGENT-SKILLS-OPERATING-CONTRACT.md), [routing tests](../../tests/agent_skills_contract.py).
