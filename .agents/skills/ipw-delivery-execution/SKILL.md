---
name: ipw-delivery-execution
description: Use when implementing or reviewing IPW GitHub changes, fixing PR or CI findings, validating exact code revisions, coordinating release manifests, or merging an authorized change.
---

# ipw-delivery-execution

## Work
1. Inspect current repo head/base, related open PRs, existing branch ownership, CI, product acceptance criteria and targeted customer gate. Avoid duplicate or stale work.
2. Limit WIP to the primary connected customer journey plus a separately justified mandatory security/reliability release item.
3. Reproduce before fixing; isolate work, implement the smallest coherent change, update tests including negative-path cases and docs when contract changes. Do not invent command outcomes or suppress failures.
4. Verify tests against the exact published commit/tree; record source identity, artifacts, failing tests, limitations, review threads and approvals.
5. Check native rulesets, merge authority, head drift, and review/check status immediately before any merge. Protected branches are not bypassed. A merge is not deployment; deploy, runtime persistence, operator/customer acceptance must each be separately proven.
6. If blocked, preserve a reviewable PR and explicit owner decision. Never treat temporary authority windows as standing permission.

## Return
Changed repo/PR/head SHA, customer gate advanced, commands/results, before/after evidence, review/merge status, verified main state, blockers and next test.
