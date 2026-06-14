import unittest
from pathlib import Path

from scripts import check_profile_readme as profile_check
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
        required_internal_links = getattr(profile_check, "REQUIRED_INTERNAL_LINKS", [])
        self.assertIn("docs/private-mimesis-workbench.md", required_internal_links)
        for link in required_internal_links:
            self.assertIn(link, readme)
        for badge_url in REQUIRED_BADGE_URLS:
            self.assertIn(badge_url, readme)
        self.assertIn("private/local research workbench", readme)
        self.assertIn("not public proof", readme)
        self.assertIn("not external validation", readme)
        self.assertIn("Mimesis is the hypothesis", readme)
        self.assertIn("Mimesis v.next Workbench", readme)
        self.assertIn("Current public operating-system surface", readme)
        self.assertNotIn("Current flagship:", readme)
        self.assertIn("public v0 repository is a support surface", readme)
        self.assertNotIn("Mimesis Engineering v0", readme)
        self.assertNotIn("public v0 artifact-level imitation method", readme)
        self.assertIn("Mimesis Visual Failure Packet", readme)
        self.assertIn("Evidence Card Contract", readme)
        self.assertIn("source artifact", readme)
        self.assertIn("baseline output", readme)
        self.assertIn("conditioned output", readme)
        self.assertIn("wrong-anchor or checklist control", readme)
        self.assertIn("gate/scorer", readme)
        self.assertIn("failure cases", readme)
        self.assertIn("proof-surface discipline", readme)
        self.assertIn("Private Workbench Verification Snapshot", readme)
        self.assertIn("Mimesis Verification Relocation Packet", readme)
        self.assertIn("Mimesis Downstream Reinjection Law", readme)
        self.assertIn("Mimesis Minecraft High-Integration Evidence Card", readme)
        self.assertIn("Human-made Feeling Bench", readme)
        self.assertIn("first-pass rubric", readme)
        self.assertIn("not a universal design-quality benchmark", readme)
        self.assertIn("redacted failure artifact", readme)
        self.assertIn("redacted local hygiene artifact", readme)
        self.assertIn("redacted method-boundary artifact", readme)
        self.assertIn("banned-claim boundary", readme)
        self.assertIn("validation does not transfer", readme)
        self.assertIn("underdetermined task plus slop-contaminated prior", readme)
        self.assertIn("redacted local evidence card", readme)
        self.assertIn("not L5 proof", readme)
        self.assertIn("human visual-quality proof", readme)
        self.assertIn("near-Fable proof", readme)
        self.assertIn("public benchmark status", readme)
        self.assertIn("no true wrong-anchor", readme)
        self.assertIn("n=2 per cell", readme)
        self.assertIn("not prove universal output improvement", readme)
        self.assertIn("statistical significance", readme)
        self.assertIn("hallucination suppression", readme)
        self.assertIn("extract-loss", readme)
        self.assertIn("domain-shift", readme)
        self.assertIn("wrong-anchor", readme)
        self.assertIn(
            "https://svy04.github.io/proof-artifacts/mimesis-visual-failure-packet-2026-06-15/",
            readme,
        )
        self.assertIn(
            "https://svy04.github.io/proof-artifacts/digital-factory-workbench-verification-2026-06-15/",
            readme,
        )
        self.assertIn(
            "https://svy04.github.io/proof-artifacts/mimesis-verification-relocation-2026-06-15/",
            readme,
        )
        self.assertIn(
            "https://svy04.github.io/proof-artifacts/mimesis-downstream-reinjection-law-2026-06-15/",
            readme,
        )
        self.assertIn(
            "https://svy04.github.io/proof-artifacts/mimesis-minecraft-high-integration-evidence-card-2026-06-15/",
            readme,
        )
        self.assertIn(
            "https://svy04.github.io/human-made-feeling-bench/",
            readme,
        )
        self.assertIn(
            "https://svy04.github.io/proof-artifacts/github-profile-readme-proof-surface-2026-06-14/",
            readme,
        )
        self.assertIn("GitHub Profile README Proof Surface", readme)
        self.assertIn("CI-checked routing and claim-boundary surface", readme)
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

    def test_validation_catches_old_public_v0_as_primary_surface(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        stale_readme = readme + "\n| [Mimesis Engineering v0](https://github.com/svy04/mimesis-engineering) | public v0 artifact-level imitation method |\n"

        issues = validate_readme_text(stale_readme)

        self.assertTrue(
            any("stale Mimesis v0 primary surface" in issue for issue in issues)
        )

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
        self.assertIn("private-mimesis-workbench.md", proof_doc)
        self.assertIn("private/local evidence map", proof_doc)
        self.assertIn("Mimesis visual route", proof_doc)
        self.assertIn("private workbench route", proof_doc)
        self.assertIn("Mimesis verification-relocation route", proof_doc)
        self.assertIn("Mimesis downstream reinjection route", proof_doc)
        self.assertIn("Mimesis Minecraft high-integration evidence-card route", proof_doc)
        self.assertIn("Human-made Feeling Bench route", proof_doc)
        self.assertIn("profile proof route", proof_doc)
        self.assertIn(
            "https://svy04.github.io/proof-artifacts/github-profile-readme-proof-surface-2026-06-14/",
            proof_doc,
        )
        self.assertIn(
            "https://svy04.github.io/proof-artifacts/digital-factory-workbench-verification-2026-06-15/",
            proof_doc,
        )
        self.assertIn(
            "https://svy04.github.io/proof-artifacts/mimesis-verification-relocation-2026-06-15/",
            proof_doc,
        )
        self.assertIn(
            "https://svy04.github.io/proof-artifacts/mimesis-downstream-reinjection-law-2026-06-15/",
            proof_doc,
        )
        self.assertIn(
            "https://svy04.github.io/proof-artifacts/mimesis-minecraft-high-integration-evidence-card-2026-06-15/",
            proof_doc,
        )
        self.assertIn(
            "https://svy04.github.io/human-made-feeling-bench/",
            proof_doc,
        )
        self.assertIn("redacted failure artifact", proof_doc)
        self.assertIn("redacted local hygiene artifact", proof_doc)
        self.assertIn("redacted method-boundary artifact", proof_doc)
        self.assertIn("first-pass rubric", proof_doc)
        self.assertIn("not a universal design-quality benchmark", proof_doc)
        self.assertIn("validation does not transfer", proof_doc)
        self.assertIn("underdetermined task plus slop-contaminated prior", proof_doc)
        self.assertIn("redacted local evidence card", proof_doc)
        self.assertIn("not L5 proof", proof_doc)
        self.assertIn("near-Fable proof", proof_doc)
        self.assertIn("no true wrong-anchor", proof_doc)
        self.assertIn("not prove universal output improvement", proof_doc)
        self.assertIn("not external validation", proof_doc)
        self.assertIn("not production readiness", proof_doc)
        self.assertIn("docs/profile-proof-surface.md", readme)

    def test_private_mimesis_workbench_surface_is_bounded(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        workbench_path = Path("docs/private-mimesis-workbench.md")

        self.assertIn("docs/private-mimesis-workbench.md", readme)
        self.assertTrue(workbench_path.exists())
        workbench = workbench_path.read_text(encoding="utf-8")
        self.assertIn("Private Mimesis Workbench", workbench)
        self.assertIn("private/local research workbench", workbench)
        self.assertIn("not public proof", workbench)
        self.assertIn("not external validation", workbench)
        self.assertIn("Private source packet", workbench)
        self.assertIn("Private prototype surface", workbench)
        self.assertIn("Claim guardrail notes", workbench)
        self.assertIn("Visual failure records", workbench)
        self.assertIn("Experiment records", workbench)
        self.assertIn("High-integration evidence cards", workbench)
        self.assertIn("Mimesis Minecraft High-Integration Evidence Card", workbench)
        self.assertIn("no true wrong-anchor weakness", workbench)
        self.assertIn("Source queue", workbench)
        self.assertIn("comparison, replication, holdout", workbench)
        self.assertIn("stale local planning notes", workbench)
        self.assertIn("local leaderboard-style notes", workbench)
        self.assertIn("unrelated account-pipeline notes", workbench)
        self.assertIn("Historical", workbench)
        self.assertIn("Public-adjacent but claim-risky", workbench)
        self.assertIn("Adjacent operations planning lane", workbench)
        self.assertIn("The private workbench proves Mimesis Engineering.", workbench)
        self.assertIn("Mimesis suppresses hallucination/fabrication in general.", workbench)

    def test_visual_judgment_gate_is_profile_bounded(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        proof_doc = Path("docs/profile-proof-surface.md").read_text(
            encoding="utf-8"
        )
        workbench = Path("docs/private-mimesis-workbench.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("visual judgment evidence and expert gates", readme)
        self.assertIn("Mimesis Visual Failure Packet", readme)
        self.assertIn("private prototype surface is private", proof_doc)
        self.assertIn("visual judgment evidence and expert gates", proof_doc)
        self.assertIn("visual quality improvement", proof_doc)
        self.assertIn("Mimesis Visual Failure Packet", workbench)
        self.assertIn("external blind panel", workbench)
        self.assertIn("redacted verdict, lint, and margin-gate evidence", workbench)
        self.assertIn("not proof of visual quality improvement", workbench)

    def test_validation_catches_missing_private_workbench_evidence_link(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        readme_without_workbench = readme.replace(
            "docs/private-mimesis-workbench.md",
            "docs/missing-private-mimesis-workbench.md",
        )

        issues = validate_readme_text(readme_without_workbench)

        self.assertTrue(
            any("docs/private-mimesis-workbench.md" in issue for issue in issues)
        )


if __name__ == "__main__":
    unittest.main()
