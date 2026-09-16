SHELL := /bin/bash

.PHONY: validate docs policy guard provenance provenance-test

validate: ghe04-check guard provenance provenance-test policy docs

guard:
	@./scripts/validate-modern-accelerator.sh

provenance:
	@python3 scripts/verify_portfolio_provenance.py

provenance-test:
	@python3 -m unittest tests/test_portfolio_provenance.py -v

policy:
	@command -v opa >/dev/null 2>&1 && opa check policies/opa || echo "opa not installed; CI performs policy validation"

docs:
	@command -v mkdocs >/dev/null 2>&1 && mkdocs build --strict || echo "mkdocs not installed; CI performs docs validation"

.PHONY: ghe04-check
ghe04-check:
	@python3 scripts/validate_self_hosted_workflow.py
	@python3 -m unittest discover -s tests -p test_self_hosted_workflow.py -v
