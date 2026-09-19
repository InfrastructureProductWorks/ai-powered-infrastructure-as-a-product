# Composite AI advisory operating model

**Requirement IDs:** `BFR-AI-001`, `BFR-AI-002`, `BFR-AI-003`

## Requirement

Composite AI may help a customer understand, design, and improve a cloud foundation only inside a documented advisory boundary. Its outputs are proposals. Deterministic policy validates machine-testable constraints, named humans authorize material decisions, the product control plane binds authenticated execution authority, and a customer-controlled execution layer or separately approved External Execution Authority reconciles only the exact authorized plan/effects.

> AI interprets intent and evidence. Policy validates. Humans authorize. The product plane binds authority. The Customer Execution Layer executes.

This is a public architecture contract and implementation target. It does not assert that frozen Guard V1 or Forge V1 already enforces every requirement on this page.

## Why this requirement exists

Foundation decisions combine incomplete evidence, business intent, provider-specific choices, and organizational risk. AI can reduce discovery and documentation effort, but allowing model output to become approval or execution would collapse independent control layers and make provenance, accountability, and failure containment weaker.

## Permitted responsibilities

Composite AI may:

- identify missing or inconsistent information;
- translate approved intent into a proposed product request;
- compare evidence with published requirements;
- propose alternatives and expose their assumptions;
- explain deterministic validation results;
- diagnose sanitized product status;
- draft decision records, acceptance criteria, and remediation backlogs; and
- assemble a redacted evidence bundle.

See [approved inputs and proposal types](approved-inputs-and-proposals.md) and [authority, provenance, and human review](authority-provenance-and-human-review.md).

## Prohibited responsibilities

Composite AI must not:

- approve or merge a governed change;
- apply, destroy, or remediate infrastructure;
- grant privilege or manufacture credentials;
- accept risk or waive a control;
- declare compliance, certification, production readiness, or an authorization to operate;
- conceal uncertainty, omitted evidence, or conflicting source material; or
- bypass the stable infrastructure-product contract.

## Applicability by stage

| Stage | Permitted AI role |
|---|---|
| Intake | Classify supplied material and identify missing inputs. |
| Assessment | Draft findings, alternatives, dependencies, and questions. |
| Simulation | Prepare and review non-executable or credential-free product proposals. |
| Read-only discovery | Interpret sanitized, authorized observations. |
| Live sandbox | Explain proposed changes and diagnose sanitized status; no direct execution. |
| Pilot | Assist evidence and operations within the separately authorized data boundary. |
| Production consideration | Support accountable reviewers; never substitute for them. |

## Deterministic validation target

An implementation should fail closed when an AI output lacks its source references, declared assumptions, applicable requirement identifiers, proposed stage, requested human reviewers, or an explicit `proposal` status. Tooling exposed to the AI must exclude cloud, Kubernetes, Git, CI/CD, approval, and secret-writing authority.

## Required evidence

- model and adapter identifier suitable for the customer boundary;
- input inventory and classification;
- redaction or minimization record;
- prompt/template version or equivalent provenance identifier;
- cited requirements and evidence sources;
- declared assumptions and uncertainty;
- deterministic validation result;
- human disposition; and
- final outcome linked separately from the proposal.

## FoundationReadinessDecision behavior

- `CONTINUE`: the advisory boundary, provenance, validation, and human roles meet the requested stage.
- `CONTINUE_WITH_CONDITIONS`: AI assistance may continue on narrowed or sanitized inputs while specified gaps remain open.
- `STOP`: the proposed use grants AI approval/execution authority, exposes prohibited data, or lacks accountable human review.

These are `FoundationReadinessDecision` values, not existing Guard V1 verdicts or diagnostic codes.

## Related requirements

- [Authority and trust boundaries](../architecture/authority-and-trust-boundaries.md)
- [AI governance](../foundation-domains/ai-governance.md)
- [Evidence integrity](../evidence/evidence-integrity.md)
- [Human review and risk acceptance](../decisions/human-review-and-risk-acceptance.md)
