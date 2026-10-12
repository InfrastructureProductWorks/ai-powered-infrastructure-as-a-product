# Composite-AI Security Evaluations

These fixtures preserve deterministic negative tests for the bounded AI authority model.

- `tool-abuse/danger-verb-without-approval.json` must be denied by `agents.actions`.
- `ssrf/url-compose.json` must be denied by `agents.ssrf`.
- `prompt-injection/hidden-html.md` must retain obvious injection indicators for detection tests.

The tests do not grant the model any execution authority. They verify that proposed tool actions remain bounded by deterministic controls.


## Typed advisory and destination contracts

The action sample now allows only `propose`, `explain`, `diagnose`, and `evidence`, with a nonempty string justification and a low-risk model input. Missing fields, wrong types, unknown verbs, execution verbs, and injection-risk overrides are denied. A `human_approved` field never turns a model request into execution authority. This sample does not govern owner-authorized repository maintenance or impose a second-human gate.

The URL sample defaults to deny without an operator-owned `data.agents.egress.allowed_hosts` array. It requires canonical HTTPS URLs and a separately supplied `trusted_transport` report bound to the exact URL and host: boolean `verified` and `connection_pinned`, `redirect_policy: deny`, and a nonempty array of public resolved IP addresses. Local, private, metadata, reserved, mapped/transition IPv6 and mixed safe/unsafe resolution are denied.

**Runtime boundary:** the adapter must create the trusted report outside model-controlled input, pin the actual connection to the reviewed resolution, deny redirects, validate TLS for the host, and independently enforce customer scope and current authorization. These policies cannot authenticate a report, perform transport enforcement, prevent a transport from resolving again, or prove deployed SSRF protection. No allowlist is shipped, no network request is performed by the tests, and no executor is introduced.

Run `opa check policies/opa` and `opa test policies/opa -v` using CI's pinned OPA version. The prompt-injection grep checks fixture integrity only; runtime injection resistance requires path-specific tests in the bounded implementation repositories.
