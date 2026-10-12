package agents.security_tests

import future.keywords.every

safe_action := {"tool": {"action": {"verb": "propose"}, "justification": "Bounded fictional proposal"}, "model": {"injection_risk": "low"}}
safe_url := "https://api.example.com/v1"
safe_transport := {"verified": true, "url": safe_url, "hostname": "api.example.com", "redirect_policy": "deny", "connection_pinned": true, "resolved_ips": ["8.8.8.8"]}

test_advisory_actions_allowed {
  every verb in ["propose", "explain", "diagnose", "evidence"] {
    request := object.union(safe_action, {"tool": {"action": {"verb": verb}, "justification": "Bounded work"}})
    data.agents.actions.allow with input as request
  }
}

test_dangerous_and_unknown_actions_denied_even_with_approval {
  every verb in ["delete", "apply", "approve", "merge", "disable_mfa", "unknown", "", 1, null, true] {
    request := {"tool": {"action": {"verb": verb}, "justification": "Requested", "approval": {"human_approved": true}}, "model": {"injection_risk": "low"}}
    not data.agents.actions.allow with input as request
    count(data.agents.actions.deny) > 0 with input as request
  }
}

test_missing_and_wrong_type_action_inputs_denied {
  every request in [{}, {"tool": {"justification": "Has justification"}}, {"tool": []}, {"tool": {"action": null}}, {"tool": {"action": {"verb": "propose"}, "justification": true}, "model": {"injection_risk": "low"}}, {"tool": {"action": {"verb": "propose"}, "justification": " "}, "model": {"injection_risk": "low"}}] {
    not data.agents.actions.allow with input as request
  }
}

test_injection_risk_cannot_be_overridden {
  every risk in ["high", "unknown", null, true, 0] {
    request := object.union(safe_action, {"model": {"injection_risk": risk}, "approval": {"human_approved": true}})
    not data.agents.actions.allow with input as request
  }
}

test_valid_egress_contract_allowed {
  request := {"tool": {"action": {"url": safe_url}}, "trusted_transport": safe_transport}
  data.agents.ssrf.allow with input as request with data.agents.egress.allowed_hosts as ["api.example.com"]
}

test_missing_egress_allowlist_denied {
  request := {"tool": {"action": {"url": safe_url}}, "trusted_transport": safe_transport}
  not data.agents.ssrf.allow with input as request
}

test_request_allowlist_cannot_grant_access {
  request := {"tool": {"action": {"url": safe_url}}, "trusted_transport": safe_transport, "allowed_hosts": ["api.example.com"]}
  not data.agents.ssrf.allow with input as request
}

test_noncanonical_and_alternate_urls_denied {
  every url in ["http://api.example.com/v1", "https://api.example.com.evil.test/v1", "https://api.example.com@evil.test/v1", "https://api.example.com:443/v1", "https://127.0.0.2/v1", "https://2130706433/v1", "https://[::1]/v1", "https://api.example.com./v1", "https://API.EXAMPLE.COM/v1", "https://api.example.com/v1#fragment", "", null, 1] {
    request := {"tool": {"action": {"url": url}}, "trusted_transport": safe_transport}
    not data.agents.ssrf.allow with input as request with data.agents.egress.allowed_hosts as ["api.example.com"]
  }
}

test_private_mixed_and_invalid_resolution_denied {
  every ips in [[], ["127.0.0.2"], ["10.0.0.1"], ["169.254.169.254"], ["100.64.1.2"], ["172.16.1.1"], ["192.168.1.1"], ["::1"], ["fe80::1"], ["fc00::1"], ["::ffff:127.0.0.1"], ["8.8.8.8", "10.0.0.1"], ["not-an-ip"], [null], ["8.8.8.8/32"]] {
    transport := object.union(safe_transport, {"resolved_ips": ips})
    request := {"tool": {"action": {"url": safe_url}}, "trusted_transport": transport}
    not data.agents.ssrf.allow with input as request with data.agents.egress.allowed_hosts as ["api.example.com"]
  }
}

test_forged_unbound_or_incomplete_transport_denied {
  every changes in [{"verified": "true"}, {"verified": false}, {"url": "https://other.example.com/v1"}, {"hostname": "other.example.com"}, {"redirect_policy": "follow"}, {"connection_pinned": "true"}, {"connection_pinned": false}, {"resolved_ips": "8.8.8.8"}] {
    transport := object.union(safe_transport, changes)
    request := {"tool": {"action": {"url": safe_url}}, "trusted_transport": transport}
    not data.agents.ssrf.allow with input as request with data.agents.egress.allowed_hosts as ["api.example.com"]
  }
  not data.agents.ssrf.allow with input as {} with data.agents.egress.allowed_hosts as ["api.example.com"]
}
