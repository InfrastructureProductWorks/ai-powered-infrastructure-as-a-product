package agents.actions

default allow = false

# This bounded AI policy permits advisory work only. Owner-authorized source
# maintenance and human production execution use their separate trust boundaries.
advisory_verbs := {"propose", "explain", "diagnose", "evidence"}

valid_request {
  is_object(input.tool)
  is_object(input.tool.action)
  is_string(input.tool.action.verb)
  advisory_verbs[input.tool.action.verb]
  is_string(input.tool.justification)
  count(trim_space(input.tool.justification)) > 0
  is_object(input.model)
  input.model.injection_risk == "low"
}

deny[msg] {
  not valid_request
  msg := "A typed, justified low-risk advisory action is required; approval fields cannot grant AI execution authority"
}

allow {
  valid_request
  count(deny) == 0
}
