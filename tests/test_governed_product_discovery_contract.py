"""Deterministic positive and fail-closed negative tests for the Governed Product Discovery Contract.

Validates docs/contracts/governed-product-discovery.schema.json directly using both a strict
stdlib Draft 2020-12 subset validator and jsonschema.Draft202012Validator when installed.
"""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import re
import unittest

try:
    import jsonschema  # type: ignore
except ImportError:  # pragma: no cover - stdlib-only environments
    jsonschema = None

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs" / "contracts" / "governed-product-discovery.schema.json"
CONTRACT_README_PATH = ROOT / "docs" / "contracts" / "README.md"
INTEROP_DOC_PATH = ROOT / "docs" / "GOVERNED-AGENTIC-INTEROPERABILITY.md"
BOUNDARY_SCRIPT_PATH = ROOT / "scripts" / "audit_publication_boundary.py"

CANONICAL_PRODUCT_FIELDS = (
    "productId",
    "version",
    "lifecycleStatus",
    "capabilities",
    "supportedClouds",
    "securityBaseline",
    "networkProfiles",
    "entitlementRequirements",
    "costClassification",
    "inputContract",
    "evidenceRequirements",
)

CANONICAL_LIFECYCLE_STATUSES = (
    "DRAFT",
    "PREVIEW",
    "ACTIVE",
    "DEPRECATED",
    "RETIRED",
)

CANONICAL_MCP_TOOLS = (
    "list_products",
    "search_products",
    "get_product",
    "get_product_version",
    "get_product_requirements",
    "check_entitlement",
    "get_product_evidence",
    "get_lifecycle_status",
)

AUTHORITY_FLAG_KEYS = (
    "mayApprove",
    "mayMerge",
    "mayApply",
    "mayProvision",
    "mayGrantPrivilege",
    "mayChangePolicy",
)

REQUIRED_EP18_SCOPE_FIELDS = (
    "customerId",
    "organizationId",
    "environmentId",
)

MANDATORY_HARD_DENY_IDS = (
    "CROSSPLANE_ADMIN_MUTATION",
    "TERRAFORM_APPLY_OR_STATE",
    "PROVIDER_PRIVILEGED_API",
    "IAM_MODIFICATION",
    "DIRECT_INFRASTRUCTURE_PROVISION",
    "SELF_APPROVAL",
    "CREDENTIAL_OR_SECRET_ACCESS",
)

FORBIDDEN_INTERNAL_FIELDS = (
    "fulfillmentBinding",
    "crossplaneAdmin",
    "xrdRef",
    "compositionRef",
    "providerConfigRef",
    "terraformState",
    "terraformApply",
    "iamPolicy",
    "credentials",
    "secretRef",
)


def _strict_equals(left, right) -> bool:
    """JSON-strict equality where booleans never equal integers (False != 0, True != 1)."""
    if type(left) is bool or type(right) is bool:
        return type(left) is type(right) and left == right
    if isinstance(left, dict) and isinstance(right, dict):
        if set(left.keys()) != set(right.keys()):
            return False
        return all(_strict_equals(left[k], right[k]) for k in left)
    if isinstance(left, list) and isinstance(right, list):
        if len(left) != len(right):
            return False
        return all(_strict_equals(a, b) for a, b in zip(left, right))
    return type(left) is type(right) and left == right


def _resolve_ref(ref: str, root_schema: dict) -> dict:
    if not ref.startswith("#/"):
        raise ValueError(f"Only local JSON pointer $ref is supported: {ref}")
    target = root_schema
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        target = target[part]
    return target


def _check_type(instance, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(instance, dict)
    if expected_type == "array":
        return isinstance(instance, list)
    if expected_type == "string":
        return isinstance(instance, str)
    if expected_type == "boolean":
        return type(instance) is bool
    if expected_type == "integer":
        return type(instance) is int
    if expected_type == "number":
        return type(instance) in (int, float)
    if expected_type == "null":
        return instance is None
    raise ValueError(f"Unsupported JSON Schema type: {expected_type}")


def validate_stdlib(instance, schema: dict, root_schema: dict, path: str = "$") -> list[str]:
    """Strict pure-stdlib Draft 2020-12 subset validator for the discovery schema."""
    errors: list[str] = []

    if "$ref" in schema:
        resolved = _resolve_ref(schema["$ref"], root_schema)
        errors.extend(validate_stdlib(instance, resolved, root_schema, path))

    if "type" in schema:
        expected = schema["type"]
        allowed_types = expected if isinstance(expected, list) else [expected]
        if not any(_check_type(instance, t) for t in allowed_types):
            errors.append(f"{path}: expected type {expected}, got {type(instance).__name__}")
            return errors

    if "const" in schema and not _strict_equals(instance, schema["const"]):
        errors.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")

    if "enum" in schema and not any(_strict_equals(instance, option) for option in schema["enum"]):
        errors.append(f"{path}: value {instance!r} is not in enum {schema['enum']!r}")

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: string shorter than minLength {schema['minLength']}")
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            errors.append(f"{path}: string {instance!r} does not match pattern {schema['pattern']!r}")

    if isinstance(instance, dict):
        for req in schema.get("required", ()):
            if req not in instance:
                errors.append(f"{path}: missing required property {req!r}")
        props = schema.get("properties", {})
        for key, value in instance.items():
            if key in props:
                errors.extend(validate_stdlib(value, props[key], root_schema, f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: additional property {key!r} is forbidden")
            elif isinstance(schema.get("additionalProperties"), dict):
                errors.extend(
                    validate_stdlib(value, schema["additionalProperties"], root_schema, f"{path}.{key}")
                )

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: array length {len(instance)} < minItems {schema['minItems']}")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append(f"{path}: array length {len(instance)} > maxItems {schema['maxItems']}")
        if schema.get("uniqueItems"):
            seen: list = []
            for idx, item in enumerate(instance):
                if any(_strict_equals(item, prev) for prev in seen):
                    errors.append(f"{path}[{idx}]: duplicate item violates uniqueItems")
                else:
                    seen.append(item)

        prefix_items = schema.get("prefixItems", [])
        for idx, subschema in enumerate(prefix_items):
            if idx < len(instance):
                errors.extend(validate_stdlib(instance[idx], subschema, root_schema, f"{path}[{idx}]"))

        if "items" in schema:
            items_schema = schema["items"]
            start = len(prefix_items)
            if items_schema is False:
                if len(instance) > start:
                    errors.append(f"{path}: unexpected extra items beyond prefixItems ({len(instance)} > {start})")
            elif isinstance(items_schema, dict):
                for idx in range(start, len(instance)):
                    errors.extend(validate_stdlib(instance[idx], items_schema, root_schema, f"{path}[{idx}]"))

        if "contains" in schema:
            contains_schema = schema["contains"]
            if not any(not validate_stdlib(item, contains_schema, root_schema, f"{path}[{idx}]") for idx, item in enumerate(instance)):
                errors.append(f"{path}: array does not contain any item matching 'contains'")

    if "allOf" in schema:
        for idx, subschema in enumerate(schema["allOf"]):
            errors.extend(validate_stdlib(instance, subschema, root_schema, f"{path}<allOf:{idx}>"))

    if "anyOf" in schema:
        if not any(not validate_stdlib(instance, subschema, root_schema, path) for subschema in schema["anyOf"]):
            errors.append(f"{path}: value did not satisfy anyOf")

    if "not" in schema:
        if not validate_stdlib(instance, schema["not"], root_schema, path):
            errors.append(f"{path}: value matched forbidden 'not' subschema")

    return errors


def validate_document(instance, schema: dict, root_schema: dict) -> list[str]:
    errors = validate_stdlib(instance, schema, root_schema)
    if jsonschema is not None:  # pragma: no cover - optional extra verification when installed
        wrapped = dict(schema)
        if "$defs" not in wrapped and "$defs" in root_schema:
            wrapped["$defs"] = root_schema["$defs"]
        validator = jsonschema.Draft202012Validator(wrapped)
        for err in validator.iter_errors(instance):
            errors.append(f"jsonschema: {err.message}")
    return errors


def make_authority_flags() -> dict[str, bool]:
    return {flag: False for flag in AUTHORITY_FLAG_KEYS}


def make_valid_product(lifecycle_status: str = "ACTIVE") -> dict:
    return {
        "productId": "governed-network-foundation",
        "version": "1.2.0",
        "lifecycleStatus": lifecycle_status,
        "capabilities": [
            "private-network-segmentation",
            "egress-policy-enforcement",
        ],
        "supportedClouds": ["aws", "azure", "gcp"],
        "securityBaseline": {
            "baselineId": "sec-baseline-network-v1",
            "version": "1.0.0",
            "mandatoryControls": [
                "private-endpoints-only",
                "flow-logging-enabled",
                "encryption-in-transit",
            ],
            "consumerOverridable": False,
        },
        "networkProfiles": [
            {
                "profileId": "restricted-enterprise-v1",
                "connectivityMode": "restricted-egress",
                "restrictedNetworkSupported": True,
            }
        ],
        "entitlementRequirements": {
            "entitlementId": "ent-network-foundation-v1",
            "requiredScopeFields": list(REQUIRED_EP18_SCOPE_FIELDS),
            "allowedEnvironments": ["dev", "staging"],
            "commercialEntitlementGrantsExecution": False,
            "crossCustomerSubstitutionAllowed": False,
        },
        "costClassification": {
            "tier": "standard",
            "currency": "USD",
            "chargebackRequired": True,
            "budgetGuardrailRequired": True,
        },
        "inputContract": {
            "schemaRef": "contracts/governed-network-foundation-input-v1.schema.json",
            "version": "1.2.0",
            "closedObject": True,
            "requiredInputs": ["region", "cidrProfile", "environmentClass"],
        },
        "evidenceRequirements": {
            "requiredArtifacts": [
                "policy-evaluation-summary",
                "security-baseline-attestation",
            ],
            "digestAlgorithm": "sha256",
            "customerScopedLineage": True,
            "humanReviewRequiredForExceptions": True,
        },
    }


def make_valid_mcp_tool(name: str) -> dict:
    return {
        "name": name,
        "readOnly": True,
        "requiresCustomerScope": True,
        "description": f"Read-only governed product discovery operation: {name}",
        "authority": make_authority_flags(),
        "requiredScopeFields": list(REQUIRED_EP18_SCOPE_FIELDS),
        "outputRedaction": {
            "stripFulfillmentBinding": True,
            "stripImplementationPrimitives": True,
        },
    }


def make_valid_mcp_catalog() -> dict:
    return {
        "protocol": "MCP",
        "surfaceMode": "READ_ONLY_DISCOVERY",
        "readOnly": True,
        "authority": make_authority_flags(),
        "tools": [make_valid_mcp_tool(name) for name in CANONICAL_MCP_TOOLS],
    }


def make_valid_hard_deny_list() -> list[dict]:
    rationales = {
        "CROSSPLANE_ADMIN_MUTATION": "Crossplane admin, XRD, and Composition mutations are prohibited on discovery surfaces.",
        "TERRAFORM_APPLY_OR_STATE": "Terraform apply and state access are prohibited on discovery surfaces.",
        "PROVIDER_PRIVILEGED_API": "Direct cloud provider privileged API calls are prohibited on discovery surfaces.",
        "IAM_MODIFICATION": "IAM role, principal, and policy modifications are prohibited on discovery surfaces.",
        "DIRECT_INFRASTRUCTURE_PROVISION": "Direct infrastructure provisioning bypasses governed validation and human review.",
        "SELF_APPROVAL": "Agents and discovery surfaces may never self-approve requests or exceptions.",
        "CREDENTIAL_OR_SECRET_ACCESS": "Discovery surfaces never expose or retrieve credentials, tokens, or secrets.",
    }
    return [
        {
            "operationId": op_id,
            "decision": "DENY",
            "overridePermitted": False,
            "rationale": rationales[op_id],
        }
        for op_id in MANDATORY_HARD_DENY_IDS
    ]


def make_valid_contract() -> dict:
    return {
        "schemaVersion": "ipw.governed-product-discovery/v1alpha1",
        "posture": "SYNTHETIC_ONLY",
        "authority": make_authority_flags(),
        "redactionPolicy": {
            "fulfillmentBindingExposed": False,
            "implementationDetailsExposed": False,
            "failClosedOnUnknownFields": True,
            "forbiddenConsumerFields": list(FORBIDDEN_INTERNAL_FIELDS),
        },
        "entitlementScopeContract": {
            "requiredScopeFields": list(REQUIRED_EP18_SCOPE_FIELDS),
            "crossCustomerAccess": "DENY_FAIL_CLOSED",
            "retainNegativeEvidence": True,
        },
        "mcpDiscoveryCatalog": make_valid_mcp_catalog(),
        "hardDenyList": make_valid_hard_deny_list(),
        "products": [make_valid_product()],
    }


class GovernedProductDiscoveryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.readme_text = CONTRACT_README_PATH.read_text(encoding="utf-8")
        cls.interop_text = INTEROP_DOC_PATH.read_text(encoding="utf-8")

    # ------------------------------------------------------------------
    # Positive tests
    # ------------------------------------------------------------------

    def test_schema_metadata_and_closed_objects(self) -> None:
        self.assertEqual(self.schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(self.schema["additionalProperties"])
        for def_name, def_schema in self.schema["$defs"].items():
            if def_schema.get("type") == "object":
                with self.subTest(definition=def_name):
                    self.assertFalse(
                        def_schema.get("additionalProperties", True),
                        f"$defs.{def_name} must set additionalProperties: false",
                    )

    def test_valid_governed_product_all_lifecycle_statuses(self) -> None:
        product_schema = self.schema["$defs"]["GovernedProduct"]
        for status in CANONICAL_LIFECYCLE_STATUSES:
            with self.subTest(lifecycleStatus=status):
                errors = validate_document(make_valid_product(status), product_schema, self.schema)
                self.assertEqual(errors, [])

    def test_valid_mcp_discovery_catalog(self) -> None:
        catalog_schema = self.schema["$defs"]["McpDiscoveryCatalog"]
        errors = validate_document(make_valid_mcp_catalog(), catalog_schema, self.schema)
        self.assertEqual(errors, [])

    def test_valid_customer_scope(self) -> None:
        scope_schema = self.schema["$defs"]["CustomerScope"]
        scope = {
            "customerId": "cust-synthetic-001",
            "organizationId": "org-synthetic-platform",
            "environmentId": "env-dev-01",
        }
        errors = validate_document(scope, scope_schema, self.schema)
        self.assertEqual(errors, [])

    def test_valid_full_contract_document(self) -> None:
        errors = validate_document(make_valid_contract(), self.schema, self.schema)
        self.assertEqual(errors, [])

    def test_exact_alignment_with_governed_agentic_interoperability_doc(self) -> None:
        product_schema = self.schema["$defs"]["GovernedProduct"]
        self.assertEqual(tuple(product_schema["required"]), CANONICAL_PRODUCT_FIELDS)
        self.assertEqual(set(product_schema["properties"].keys()), set(CANONICAL_PRODUCT_FIELDS))
        self.assertNotIn("fulfillmentBinding", product_schema["properties"])

        # Every canonical consumer field and internal fulfillmentBinding is documented in the architecture spec.
        for field in CANONICAL_PRODUCT_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, self.interop_text)
        self.assertIn("fulfillmentBinding", self.interop_text)

        # Closed 8-tool MCP catalog matches docs/GOVERNED-AGENTIC-INTEROPERABILITY.md verbatim.
        tool_enum = tuple(self.schema["$defs"]["McpDiscoveryToolName"]["enum"])
        self.assertEqual(tool_enum, CANONICAL_MCP_TOOLS)
        for tool_name in CANONICAL_MCP_TOOLS:
            with self.subTest(tool=tool_name):
                self.assertIn(f"`{tool_name}()`", self.interop_text)

        # Hard authority DENY rules from the architecture doc are all represented.
        for required_phrase in (
            "Crossplane admin",
            "Terraform apply",
            "provider privileged API",
            "IAM modification",
            "direct infrastructure provision",
            "self-approval",
        ):
            with self.subTest(deny_rule=required_phrase):
                self.assertIn(required_phrase, self.interop_text)

    def test_contract_readme_documents_invariants_and_claim_boundaries(self) -> None:
        for token in (
            *CANONICAL_PRODUCT_FIELDS,
            "fulfillmentBinding",
            *CANONICAL_MCP_TOOLS,
            *AUTHORITY_FLAG_KEYS,
            *REQUIRED_EP18_SCOPE_FIELDS,
            *MANDATORY_HARD_DENY_IDS,
            "SYNTHETIC_ONLY",
            "additionalProperties: false",
            "governed-product-discovery.schema.json",
            "../GOVERNED-AGENTIC-INTEROPERABILITY.md",
        ):
            with self.subTest(token=token):
                self.assertIn(token, self.readme_text)

    def test_publication_boundary_cleanliness(self) -> None:
        spec = importlib.util.spec_from_file_location("audit_publication_boundary", BOUNDARY_SCRIPT_PATH)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)

        for target in (SCHEMA_PATH, CONTRACT_README_PATH, Path(__file__).resolve()):
            with self.subTest(path=str(target.relative_to(ROOT))):
                text = target.read_text(encoding="utf-8")
                self.assertFalse(
                    module.restricted(text),
                    f"Public publication boundary violation detected in {target}",
                )

    # ------------------------------------------------------------------
    # Fail-closed negative tests
    # ------------------------------------------------------------------

    def test_reject_forbidden_mutation_and_privileged_tool_names(self) -> None:
        tool_schema = self.schema["$defs"]["McpDiscoveryToolDescriptor"]
        catalog_schema = self.schema["$defs"]["McpDiscoveryCatalog"]
        forbidden_tools = (
            "create_product",
            "update_product",
            "delete_product",
            "approve_request",
            "self_approve",
            "merge_pull_request",
            "provision_infrastructure",
            "apply_terraform",
            "read_terraform_state",
            "mutate_crossplane_xrd",
            "update_composition",
            "modify_iam_policy",
            "call_provider_admin_api",
            "read_secret",
        )
        for bad_name in forbidden_tools:
            with self.subTest(tool=bad_name):
                bad_tool = make_valid_mcp_tool(bad_name)
                self.assertTrue(validate_document(bad_tool, tool_schema, self.schema))

                bad_catalog = make_valid_mcp_catalog()
                bad_catalog["tools"][0] = bad_tool
                self.assertTrue(validate_document(bad_catalog, catalog_schema, self.schema))

    def test_reject_incomplete_duplicate_or_expanded_mcp_catalog(self) -> None:
        catalog_schema = self.schema["$defs"]["McpDiscoveryCatalog"]

        # Missing one required tool (7 items).
        missing_tool = make_valid_mcp_catalog()
        missing_tool["tools"].pop()
        self.assertTrue(validate_document(missing_tool, catalog_schema, self.schema))

        # Duplicate tool replacing another required tool (still 8 items, fails uniqueItems + contains).
        duplicate_tool = make_valid_mcp_catalog()
        duplicate_tool["tools"][-1] = copy.deepcopy(duplicate_tool["tools"][0])
        self.assertTrue(validate_document(duplicate_tool, catalog_schema, self.schema))

        # Extra 9th tool (fails maxItems + uniqueItems).
        extra_tool = make_valid_mcp_catalog()
        extra_tool["tools"].append(make_valid_mcp_tool("list_products"))
        self.assertTrue(validate_document(extra_tool, catalog_schema, self.schema))

    def test_reject_non_readonly_mcp_surface_or_weakened_redaction(self) -> None:
        catalog_schema = self.schema["$defs"]["McpDiscoveryCatalog"]

        writable_catalog = make_valid_mcp_catalog()
        writable_catalog["readOnly"] = False
        self.assertTrue(validate_document(writable_catalog, catalog_schema, self.schema))

        writable_tool = make_valid_mcp_catalog()
        writable_tool["tools"][0]["readOnly"] = False
        self.assertTrue(validate_document(writable_tool, catalog_schema, self.schema))

        unscoped_tool = make_valid_mcp_catalog()
        unscoped_tool["tools"][0]["requiresCustomerScope"] = False
        self.assertTrue(validate_document(unscoped_tool, catalog_schema, self.schema))

        unredacted_binding = make_valid_mcp_catalog()
        unredacted_binding["tools"][0]["outputRedaction"]["stripFulfillmentBinding"] = False
        self.assertTrue(validate_document(unredacted_binding, catalog_schema, self.schema))

        unredacted_impl = make_valid_mcp_catalog()
        unredacted_impl["tools"][0]["outputRedaction"]["stripImplementationPrimitives"] = False
        self.assertTrue(validate_document(unredacted_impl, catalog_schema, self.schema))

    def test_reject_exposed_fulfillment_binding_and_internal_fields(self) -> None:
        product_schema = self.schema["$defs"]["GovernedProduct"]
        for forbidden_field in FORBIDDEN_INTERNAL_FIELDS:
            with self.subTest(forbidden_field=forbidden_field):
                leaked = make_valid_product()
                leaked[forbidden_field] = {"provider": "internal-implementation"}
                errors = validate_document(leaked, product_schema, self.schema)
                self.assertTrue(errors, f"Expected {forbidden_field} to be rejected")

    def test_reject_weakened_redaction_policy(self) -> None:
        policy_schema = self.schema["$defs"]["RedactionPolicy"]
        base_policy = make_valid_contract()["redactionPolicy"]

        for field, bad_value in (
            ("fulfillmentBindingExposed", True),
            ("implementationDetailsExposed", True),
            ("failClosedOnUnknownFields", False),
        ):
            with self.subTest(field=field):
                mutated = copy.deepcopy(base_policy)
                mutated[field] = bad_value
                self.assertTrue(validate_document(mutated, policy_schema, self.schema))

        missing_binding = copy.deepcopy(base_policy)
        missing_binding["forbiddenConsumerFields"].remove("fulfillmentBinding")
        self.assertTrue(validate_document(missing_binding, policy_schema, self.schema))

    def test_reject_any_authority_flag_true_or_non_boolean(self) -> None:
        for flag in AUTHORITY_FLAG_KEYS:
            with self.subTest(scope="root", flag=flag):
                doc = make_valid_contract()
                doc["authority"][flag] = True
                self.assertTrue(validate_document(doc, self.schema, self.schema))

            with self.subTest(scope="catalog", flag=flag):
                doc = make_valid_contract()
                doc["mcpDiscoveryCatalog"]["authority"][flag] = True
                self.assertTrue(validate_document(doc, self.schema, self.schema))

            with self.subTest(scope="tool", flag=flag):
                doc = make_valid_contract()
                doc["mcpDiscoveryCatalog"]["tools"][0]["authority"][flag] = True
                self.assertTrue(validate_document(doc, self.schema, self.schema))

            with self.subTest(scope="non_bool_zero", flag=flag):
                doc = make_valid_contract()
                doc["authority"][flag] = 0
                self.assertTrue(validate_document(doc, self.schema, self.schema))

    def test_reject_missing_or_invalid_ep18_customer_scope(self) -> None:
        product_schema = self.schema["$defs"]["GovernedProduct"]
        scope_schema = self.schema["$defs"]["CustomerScope"]

        for missing_key in REQUIRED_EP18_SCOPE_FIELDS:
            with self.subTest(target="entitlementRequirements", missing=missing_key):
                product = make_valid_product()
                product["entitlementRequirements"]["requiredScopeFields"].remove(missing_key)
                self.assertTrue(validate_document(product, product_schema, self.schema))

            with self.subTest(target="CustomerScope_missing", missing=missing_key):
                scope = {
                    "customerId": "cust-001",
                    "organizationId": "org-001",
                    "environmentId": "env-001",
                }
                del scope[missing_key]
                self.assertTrue(validate_document(scope, scope_schema, self.schema))

            with self.subTest(target="CustomerScope_empty", empty=missing_key):
                scope = {
                    "customerId": "cust-001",
                    "organizationId": "org-001",
                    "environmentId": "env-001",
                }
                scope[missing_key] = ""
                self.assertTrue(validate_document(scope, scope_schema, self.schema))

        # Reordered or extra scope field must fail closed.
        reordered = make_valid_product()
        reordered["entitlementRequirements"]["requiredScopeFields"] = [
            "organizationId",
            "customerId",
            "environmentId",
        ]
        self.assertTrue(validate_document(reordered, product_schema, self.schema))

        cross_customer = make_valid_product()
        cross_customer["entitlementRequirements"]["crossCustomerSubstitutionAllowed"] = True
        self.assertTrue(validate_document(cross_customer, product_schema, self.schema))

        commercial_exec = make_valid_product()
        commercial_exec["entitlementRequirements"]["commercialEntitlementGrantsExecution"] = True
        self.assertTrue(validate_document(commercial_exec, product_schema, self.schema))

        bad_scope_contract = make_valid_contract()
        bad_scope_contract["entitlementScopeContract"]["crossCustomerAccess"] = "ALLOW"
        self.assertTrue(validate_document(bad_scope_contract, self.schema, self.schema))

    def test_reject_extra_unknown_properties(self) -> None:
        cases = [
            ("root", make_valid_contract(), lambda d: d.__setitem__("unexpectedField", "x")),
            ("product", make_valid_contract(), lambda d: d["products"][0].__setitem__("extraProp", "x")),
            ("securityBaseline", make_valid_contract(), lambda d: d["products"][0]["securityBaseline"].__setitem__("extra", 1)),
            ("entitlementRequirements", make_valid_contract(), lambda d: d["products"][0]["entitlementRequirements"].__setitem__("extra", 1)),
            ("costClassification", make_valid_contract(), lambda d: d["products"][0]["costClassification"].__setitem__("extra", 1)),
            ("inputContract", make_valid_contract(), lambda d: d["products"][0]["inputContract"].__setitem__("extra", 1)),
            ("evidenceRequirements", make_valid_contract(), lambda d: d["products"][0]["evidenceRequirements"].__setitem__("extra", 1)),
            ("mcpDiscoveryCatalog", make_valid_contract(), lambda d: d["mcpDiscoveryCatalog"].__setitem__("extra", 1)),
            ("mcpTool", make_valid_contract(), lambda d: d["mcpDiscoveryCatalog"]["tools"][0].__setitem__("extra", 1)),
            ("authority", make_valid_contract(), lambda d: d["authority"].__setitem__("mayExecute", False)),
            ("hardDenyRule", make_valid_contract(), lambda d: d["hardDenyList"][0].__setitem__("extra", 1)),
        ]
        for label, doc, mutator in cases:
            with self.subTest(target=label):
                mutator(doc)
                self.assertTrue(validate_document(doc, self.schema, self.schema))

        scope_extra = {
            "customerId": "cust-001",
            "organizationId": "org-001",
            "environmentId": "env-001",
            "tenantOverride": "cust-002",
        }
        self.assertTrue(validate_document(scope_extra, self.schema["$defs"]["CustomerScope"], self.schema))

    def test_reject_invalid_lifecycle_status(self) -> None:
        product_schema = self.schema["$defs"]["GovernedProduct"]
        for bad_status in ("LIVE", "PRODUCTION", "APPROVED", "active", "draft", "", None, 1):
            with self.subTest(lifecycleStatus=bad_status):
                product = make_valid_product()
                product["lifecycleStatus"] = bad_status
                self.assertTrue(validate_document(product, product_schema, self.schema))

    def test_reject_weakened_hard_deny_list_and_posture(self) -> None:
        # Missing any mandatory hard deny rule fails closed.
        for op_id in MANDATORY_HARD_DENY_IDS:
            with self.subTest(missing_deny=op_id):
                doc = make_valid_contract()
                doc["hardDenyList"] = [r for r in doc["hardDenyList"] if r["operationId"] != op_id]
                self.assertTrue(validate_document(doc, self.schema, self.schema))

        # Changing decision from DENY to ALLOW fails closed.
        allow_rule = make_valid_contract()
        allow_rule["hardDenyList"][0]["decision"] = "ALLOW"
        self.assertTrue(validate_document(allow_rule, self.schema, self.schema))

        # Allowing override fails closed.
        override_rule = make_valid_contract()
        override_rule["hardDenyList"][0]["overridePermitted"] = True
        self.assertTrue(validate_document(override_rule, self.schema, self.schema))

        # Non-SYNTHETIC_ONLY posture fails closed.
        live_posture = make_valid_contract()
        live_posture["posture"] = "PRODUCTION_READY"
        self.assertTrue(validate_document(live_posture, self.schema, self.schema))


if __name__ == "__main__":
    unittest.main()
