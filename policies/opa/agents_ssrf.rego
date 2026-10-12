package agents.ssrf

default allow = false

# The allowlist is operator-owned policy data, never model request fields.
# The trusted transport report must come from the adapter's actual destination
# resolution and pinned connection. This policy cannot perform that enforcement.
blocked_cidrs := {
  "0.0.0.0/8", "10.0.0.0/8", "100.64.0.0/10", "127.0.0.0/8",
  "169.254.0.0/16", "172.16.0.0/12", "192.0.0.0/24",
  "192.0.2.0/24", "192.168.0.0/16", "198.18.0.0/15",
  "198.51.100.0/24", "203.0.113.0/24", "224.0.0.0/4", "240.0.0.0/4",
  "::/128", "::1/128", "64:ff9b::/96",
  "64:ff9b:1::/48", "100::/64", "2001::/23", "2001:db8::/32",
  "2002::/16", "fc00::/7", "fe80::/10", "ff00::/8"
}

valid_ip(ip) {
  is_string(ip)
  not contains(ip, "/")
  net.cidr_contains("0.0.0.0/0", ip)
}

valid_ip(ip) {
  is_string(ip)
  not contains(ip, "/")
  net.cidr_contains("::/0", ip)
}

unsafe_ip(ip) {
  not valid_ip(ip)
}

unsafe_ip(ip) {
  blocked_cidrs[cidr]
  net.cidr_contains(cidr, ip)
}

# Go's IP parser maps ordinary IPv4 into the mapped family for CIDR checks;
# apply this special denial only to an explicitly IPv6-formatted address.
unsafe_ip(ip) {
  is_string(ip)
  contains(ip, ":")
  net.cidr_contains("::ffff:0:0/96", ip)
}

valid_destination {
  is_string(input.tool.action.url)
  # Canonical lowercase DNS hostname, HTTPS, no credentials, no IP literal,
  # no alternate port or fragment. Other representations are default-denied.
  matches := regex.find_all_string_submatch_n(
    `^https://([a-z][a-z0-9-]*(?:\.[a-z0-9-]+)+)(?:/[^\s#]*)?$`,
    input.tool.action.url, 1)
  count(matches) == 1
  host := matches[0][1]
  is_array(data.agents.egress.allowed_hosts)
  data.agents.egress.allowed_hosts[_] == host
  is_object(input.trusted_transport)
  input.trusted_transport.verified == true
  input.trusted_transport.url == input.tool.action.url
  input.trusted_transport.hostname == host
  input.trusted_transport.redirect_policy == "deny"
  input.trusted_transport.connection_pinned == true
  is_array(input.trusted_transport.resolved_ips)
  count(input.trusted_transport.resolved_ips) > 0
  count([ip | ip := input.trusted_transport.resolved_ips[_]; unsafe_ip(ip)]) == 0
}

deny[msg] {
  not valid_destination
  msg := "HTTPS allowlisted destination with verified pinned resolution and denied redirects is required"
}

allow {
  valid_destination
  count(deny) == 0
}
