---
name: ipw-environment-operations
description: Use for IPW dev/test/staging/production separation, CI/CD promotion, service restart/backup/rollback, runtime inventory, operational acceptance or release readiness.
---

# ipw-environment-operations

## Work
1. Inventory **configured, deployed, verified, accepted** separately for each product/runtime; libraries do not automatically require permanent environments.
2. Distinguish IPW service runtime environments from a customer's infrastructure fulfillment target.
3. Design lean local/CI development, isolated shared test/staging and isolated production release configuration only for released services. No cross-env secrets, app signing keys, data stores, customer records, privileged targets, or production GitHub App/webhook installations.
4. Promote the same immutable tested artifact/digest, capture source revision and provenance, verify environment boundaries and cost ownership.
5. Require hosted end-to-end synthetic journey, cross-env denial tests, persistence/restart, backup/restore, monitoring, rollback, source identity and operator on-call before declaring hosted acceptance.
6. Separate `configured`, `merged`, `deployed`, `synthetic-verified`, `operator-accepted`, and `customer-accepted`. No infrastructure spending, secrets, deployment or production activation without existing explicit authority.

## Return
Per-runtime evidence matrix, exact artifact IDs, isolation and negative-test proof, cost/owner inventory, rollback result, readiness classification and smallest missing gate.
