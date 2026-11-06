# IPW executive agent skills — operating contract

**Status:** Version-controlled reusable procedures, not runtime activation or delegated legal authority.

## Purpose and routing
IPW virtual executive functions use a minimum set of focused repeatable skills in [the local skills library](../../.agents/skills/README.md). Skills drive better decisions; they do not create independent executives, tools, model instances, budget authority, customer consents or privileged runtime access.

| Task | Lead skill | Supporting skill | Evidence gate |
| --- | --- | --- | --- |
| New buyer/pilot signal | `ipw-product-discovery` | `ipw-strategic-decisions` | interview/prospect provenance and falsifiable pilot criteria |
| AI-native/API/MCP portfolio shift | `ipw-architecture-review` | `ipw-product-discovery` | accepted consumer contract and negative authority tests |
| Cross-product implementation | `ipw-delivery-execution` | `ipw-architecture-review` | exact-head tests plus connected journey proof |
| Admission/security blocker | `ipw-security-assurance` | `ipw-delivery-execution` | native veto, custody and independent authorization |
| Separate dev/staging/prod | `ipw-environment-operations` | `ipw-security-assurance` | actual isolated hosted tests and rollback |
| Investment/prioritization | `ipw-strategic-decisions` | `ipw-executive-review` | evidence/assumption ledger, cost and decision |
| Founder executive briefing | `ipw-executive-review` | chosen specialists | dissent, accountable owner, proof and next gate |

## Executive responsibilities
Product/Technology jointly supply end-to-end connected customer capability evidence, with one designated accountable delivery owner per decision. Security/Quality retains independent veto and test disposition. Finance flags observed versus estimated cost, and Revenue distinguishes actual buyer discovery from internal assumptions. Chief of Staff maintains decisions, dependencies and cross-repo alignment. The founder retains strategic decision authority.

## Required decision receipt
Record: decision ID/date; customer and job; source links with exact revision or event time; observations vs hypotheses; alternatives including no change; owner and dissent; customer acceptance gate; status (planned/source-verified/synthetic/staging/operator/customer); security and human hold points; next measured experiment; review condition. **NOT MEASURED** is preferable to invented baselines.

## Invariants
- Deterministic Guard denial, human selection, custody, separate deployment approval, native branch rules and credential boundaries survive every skill invocation.
- No skill grants customer authority, new spending, privileged cloud access, production activation or deployment. A green PR or documentation update is not runtime proof.
- Do not create a competing product roadmap, a duplicate customer journey or a second operational scoreboard.
- The first buyer hypothesis remains a regulated-platform leader until customer evidence changes it; no assumption that this buyer is confirmed.
- The supported starting slice is CloudFoundationEnvironment development intent and the existing bounded synthetic AWS/GCP customer journey.
- Commit skill changes through reviewed PRs and rerun routing/contract checks when skill names, descriptions or scopes change.

## Orchestration adoption
Codex-compatible repository-local discovery reads `.agents/skills/<name>/SKILL.md` for this repository. Separate ChatGPT automations and agents do **not** discover files simply because they are in GitHub: their prompts must explicitly retrieve these instructions from the canonical repository's trusted revision and apply only relevant skills. GitHub connectors provide supported reads/writes; an instruction to use a tool cannot widen tool permissions. Track adoption by recording loaded skill name + commit SHA in the next executive decision receipt. Never claim a runtime has adopted a skill until an actual execution shows it loaded the content.
