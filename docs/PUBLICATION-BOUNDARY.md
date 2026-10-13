# Public Publication Boundary

This repository is the public Infrastructure-as-a-Product thesis, architecture, interoperability, and sanitized assurance surface. It should explain what the product system does and why the architecture is trustworthy without reproducing private Guard, Forge, or Console implementation details.

## Publish deliberately

Public material may include:

- the Infrastructure-as-a-Product thesis and developer-outcome model;
- high-level Guard, Forge, and Console product boundaries;
- deliberately public schemas, interface contracts, installation and interoperability guidance;
- high-level authority and trust boundaries;
- architecture decisions needed for ecosystem understanding; and
- sanitized evidence sufficient to substantiate a public capability or validation claim.

## Keep private

Do not newly publish the following from private product repositories unless an explicit review determines that disclosure is necessary:

- private repository commit SHAs or internal branch/release coordinates;
- implementation code, internal algorithms, rule/scoring/materiality logic, prompts, role mechanics, heuristics, fixtures, regression cases, or unreleased evaluation methods;
- entitlement-key mechanics, internal licensing controls, pricing hypotheses, acquisition strategy, or unreleased commercial packaging;
- live infrastructure physical names, IAM-role/policy details, deployment internals, secret-reference topology, workflow/job identifiers, or unsanitized operational evidence;
- customer data, private repository content, credentials, secrets, nonpublic telemetry, or confidential third-party material; and
- details that make it easier to reconstruct a private implementation when a high-level architecture statement is sufficient.

## Evidence publication rule

Public evidence should prove the narrow property being claimed while disclosing the minimum implementation detail necessary. Prefer sanitized summaries, immutable public evidence digests, public contracts, and bounded acceptance results over raw deployment output or private implementation coordinates.

Historical public material is not made secret by this policy. Do not rewrite Git history solely to create the appearance that a prior public disclosure did not occur. Instead, keep current and future publication aligned to this boundary and retain a private disclosure inventory for legal review.

## Legal status

This document is a publication-control policy, not a legal ownership statement. It does not identify an IP owner, change the repository's existing license, revoke rights previously granted, determine patentability, or make a trademark or copyright-registration decision.

## Publication review and historical exceptions

Guard remains free and this thesis remains public. Public architecture, adoption guidance, deliberately public integration contracts, and sanitized acceptance results remain available. Private runtime algorithms, prompts, entitlement mechanics, regression fixtures and operational coordinates belong in restricted implementation or integration records.

The publication gate rejects restricted repository coordinates unless the entire file matches an explicit SHA-256 historical exception in `config/publication-history.json`. These exceptions preserve previously published historical baseline and immutable evidence records; CI anchors the exception set to the trusted base revision and rejects additions or changed digests in the same change. First adoption permits only exact bytes already present in that base. They are not permission to add private implementation details. A sole owner may perform the review; a second human is not required.

Current Forge reconciliation and Assurance baseline summaries use domain-separated revision commitments. Original records are retained in restricted integration documentation. Commitments support correspondence with retained evidence; they do not authenticate a publisher or conceal historical disclosures. Existing licenses and legal status remain unchanged. Public demo examples remain disclosed synthetic source; substantive changes must state their public or synthetic purpose rather than importing private runtime logic.

Historical accepted artifact paths and bytes remain available so earlier phase evidence can still be verified. Current guidance points to the sanitized v2 summaries under `artifacts/publication/`. The original records are also retained in the restricted disclosure inventory.
