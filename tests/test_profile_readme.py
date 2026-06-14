import unittest
from pathlib import Path

from scripts.check_profile_readme import (
    REQUIRED_BADGE_URLS,
    REQUIRED_LINKS,
    extract_markdown_links,
    validate_readme_text,
)


class ProfileReadmeTests(unittest.TestCase):
    def test_extracts_markdown_links(self):
        text = (
            "[Metaforge](https://github.com/svy04/metaforge) and "
            "[NoiseProof](https://github.com/svy04/noiseproof-agent) and "
            "[![Profile README](https://github.com/svy04/svy04/actions/workflows/profile-readme.yml/badge.svg)](https://github.com/svy04/svy04/actions/workflows/profile-readme.yml)"
        )

        self.assertEqual(
            extract_markdown_links(text),
            [
                "https://github.com/svy04/metaforge",
                "https://github.com/svy04/noiseproof-agent",
                "https://github.com/svy04/svy04/actions/workflows/profile-readme.yml/badge.svg",
                "https://github.com/svy04/svy04/actions/workflows/profile-readme.yml",
            ],
        )

    def test_current_readme_has_required_links_and_claim_boundaries(self):
        readme = Path("README.md").read_text(encoding="utf-8")

        issues = validate_readme_text(readme)

        self.assertEqual(issues, [])
        for link in REQUIRED_LINKS:
            self.assertIn(link, readme)
        for badge_url in REQUIRED_BADGE_URLS:
            self.assertIn(badge_url, readme)
        self.assertIn("private/local research workbench", readme)
        self.assertIn("not public proof", readme)
        self.assertIn("not external validation", readme)
        self.assertIn("Mimesis is the hypothesis", readme)
        self.assertNotIn("Phase 897/898 reviewer packet", readme)

    def test_validation_catches_unbounded_mimesis_claim(self):
        text = "\n".join(
            [
                "# 오영웅 · @svy04",
                "Mimesis Engineering is proven and universally improves AI output.",
                "https://github.com/svy04/metaforge",
                "https://github.com/svy04/noiseproof-agent",
                "https://github.com/svy04/mimesis-engineering",
            ]
        )

        issues = validate_readme_text(text)

        self.assertTrue(any("unbounded Mimesis claim" in issue for issue in issues))

    def test_profile_verification_gate_is_documented_and_ci_wired(self):
        workflow = Path(".github/workflows/profile-readme.yml").read_text(
            encoding="utf-8"
        )
        proof_doc = Path("docs/profile-proof-surface.md").read_text(encoding="utf-8")
        readme = Path("README.md").read_text(encoding="utf-8")

        self.assertIn("python scripts/check_profile_readme.py", workflow)
        self.assertIn("python -m unittest discover -s tests -v", workflow)
        self.assertIn("python scripts/check_profile_readme.py --check-links", workflow)
        self.assertIn("Profile README Proof Surface", proof_doc)
        self.assertIn("workflow status badges", proof_doc)
        self.assertIn("not external validation", proof_doc)
        self.assertIn("not production readiness", proof_doc)
        self.assertIn("docs/profile-proof-surface.md", readme)


if __name__ == "__main__":
    unittest.main()
