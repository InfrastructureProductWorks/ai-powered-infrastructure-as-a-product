"""Static checks for IPW's reusable executive agent skill contracts.

Intentionally stdlib-only and data-only: it does not execute skill instructions.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
EXPECTED = {
    "ipw-strategic-decisions",
    "ipw-product-discovery",
    "ipw-architecture-review",
    "ipw-security-assurance",
    "ipw-delivery-execution",
    "ipw-environment-operations",
    "ipw-executive-review",
}
CONTRACT = ROOT / "docs/executive/AGENT-SKILLS-OPERATING-CONTRACT.md"


class SkillsContractTests(unittest.TestCase):
    def test_exact_registered_skills(self):
        actual = {d.name for d in SKILLS.iterdir() if d.is_dir()}
        self.assertEqual(EXPECTED, actual)

    def test_portable_frontmatter_and_instructions(self):
        for name in sorted(EXPECTED):
            with self.subTest(name=name):
                p = SKILLS / name / "SKILL.md"
                data = p.read_text(encoding="utf-8")
                self.assertTrue(data.startswith("---\n"))
                parts = data.split("---\n", 2)
                self.assertEqual(len(parts), 3)
                meta = parts[1]
                m = dict(re.findall(r"^(name|description): (.+)$", meta, re.M))
                self.assertEqual(name, m.get("name"))
                self.assertTrue(m.get("description"), "Missing trigger description")
                self.assertTrue(parts[2].strip(), "Missing substantive instructions")
                self.assertFalse(any(x in meta for x in ("<script", "${{", "!!python")))

    def test_index_and_router(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        index = (SKILLS / "README.md").read_text(encoding="utf-8")
        contract = CONTRACT.read_text(encoding="utf-8")
        self.assertIn(".agents/skills/", agents)
        for name in sorted(EXPECTED):
            self.assertIn(name, index)
            self.assertIn(name, contract)

    def test_no_implicit_authority_claim(self):
        contract = CONTRACT.read_text(encoding="utf-8").lower()
        for phrase in ("no skill grants", "human", "customer", "production"):
            self.assertIn(phrase, contract)


if __name__ == "__main__":
    unittest.main()
