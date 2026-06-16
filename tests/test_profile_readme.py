import unittest
from pathlib import Path

from scripts import check_profile_readme as profile_check
from scripts.check_profile_render_parity import (
    PUBLIC_SURFACES,
    ROUTE_URLS,
    validate_render_parity,
)
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
        self.assertLess(len(readme), 7000)
        for link in REQUIRED_LINKS:
            self.assertIn(link, readme)
        for link in profile_check.REQUIRED_INTERNAL_LINKS:
            self.assertIn(link, readme)
        for badge_url in REQUIRED_BADGE_URLS:
            self.assertIn(badge_url, readme)

        required_sections = [
            "## Current Thesis",
            "## Mimesis Engineering",
            "## Proof Routes",
            "## Public Repos",
            "## Working Loop",
            "## Claim Boundary",
        ]
        for section in required_sections:
            self.assertIn(section, readme)

        positioning_markers = [
            "Metaforge = Meta + MFH + Orchestra OS",
            "dependency-cruiser topology, jscpd duplication, Knip dead-export triage ledger, first export/type candidate reductions, public artifact hygiene, and provider-id redaction gates",
            "OpenClaude is the runtime substrate",
            "not the main thesis",
            "Digital Factory is the private/local Mimesis Engineering workbench",
            "Public-safe proof routes summarize redacted local hygiene and blockers",
            "Fresh verifier output is required before any stronger module-pass or promotion claim",
            "AI에게 역할이 아니라 기준을 준다.",
            "give AI standards, not roles",
            "products, papers, patents, standards, and maintained open-source implementations",
            "inspection manifests",
            "Public redacted board v0 / incomplete evidence board",
            "Board v1 is not ready",
            "It does not universally improve AI output.",
            "I do not claim Metaforge is production-ready",
            "I do not claim Mimesis Engineering is an industry standard",
            "I do not claim NoiseProof is production-ready",
        ]
        for marker in positioning_markers:
            self.assertIn(marker, readme)

        forbidden_markers = [
            "Current flagship:",
            "Mimesis Engineering v0",
            "public v0 artifact-level imitation method",
            "Mimesis v.next Workbench",
            "16/16 expert modules",
            "14/14 expert modules",
            "Current local checks pass",
            "Local checks pass",
            "OpenClaude is the main thesis",
            "PR #27",
            "PR #28-style raw transcript hygiene hardening",
        ]
        for marker in forbidden_markers:
            self.assertNotIn(marker, readme)

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

    def test_validation_catches_old_public_v0_or_vnext_as_primary_surface(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        stale_readme = (
            readme
            + "\n| [Mimesis Engineering v0](https://github.com/svy04/mimesis-engineering) | public v0 artifact-level imitation method |\n"
            + "\n## Mimesis v.next Workbench\n"
        )

        issues = validate_readme_text(stale_readme)

        self.assertTrue(any("prohibited profile marker" in issue for issue in issues))

    def test_validation_catches_private_or_not_current_repo_links(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        private_link_readme = (
            readme
            + "\n- [mimesis-plugin](https://github.com/svy04/mimesis-plugin) — latest proof surface.\n"
            + "- [old profile checkout](https://github.com/svy04/openclaude) — main product.\n"
        )

        issues = validate_readme_text(private_link_readme)

        self.assertTrue(any("non-public or non-current repo link" in issue for issue in issues))

    def test_validation_catches_contradictory_positive_claim_drift(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        drifted_readme = readme + "\n".join(
            [
                "",
                "Mimesis Engineering is an industry standard for AI output improvement.",
                "Board v1 is ready for promotion.",
                "Metaforge now has external validation from reviewers.",
                "OpenClaude is the main thesis and flagship product.",
                "Mimesis Engineering is proven, not just a promising method.",
            ]
        )

        issues = validate_readme_text(drifted_readme)

        expected_labels = [
            "unbounded Mimesis claim",
            "board-v1 readiness claim",
            "unbounded external-validation claim",
            "OpenClaude-as-main claim",
        ]
        for label in expected_labels:
            self.assertTrue(any(label in issue for issue in issues), label)

    def test_validation_catches_local_path_disclosure(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        disclosed_path = "C:" + "\\Users\\owner\\" + "Private" + "\\README.md"
        disclosed = readme + f"\nLocal path: {disclosed_path}\n"

        issues = validate_readme_text(disclosed)

        self.assertTrue(any("local path disclosure" in issue for issue in issues))

    def test_profile_verification_gate_is_documented_and_ci_wired(self):
        workflow = Path(".github/workflows/profile-readme.yml").read_text(
            encoding="utf-8"
        )
        proof_doc = Path("docs/profile-proof-surface.md").read_text(encoding="utf-8")
        readme = Path("README.md").read_text(encoding="utf-8")

        self.assertIn("python scripts/check_profile_readme.py", workflow)
        self.assertIn("python -m unittest discover -s tests -v", workflow)
        self.assertIn("python scripts/check_profile_readme.py --check-links", workflow)
        self.assertIn("github.ref == 'refs/heads/main'", workflow)
        self.assertIn("python scripts/check_public_github_surface_hygiene.py", workflow)
        self.assertIn("GITHUB_TOKEN: ${{ github.token }}", workflow)

        proof_markers = [
            "Profile README Proof Surface",
            "source/CI proof and live public rendering stay separate",
            "live maintenance-hidden",
            "Public GitHub Surface Hygiene Proof Packet",
            "scripts/check_public_github_surface_hygiene.py",
            "public default branches",
            "scanner-unfriendly placeholders",
            "actual-looking bearer values",
            "raw auth transcript markers",
            "private-mimesis-workbench.md",
            "Metaforge-first profile framing",
            "raw-transcript-preflight.json",
            "raw-transcript-redaction-review-preflight.json",
            "PR #25-#32 blocker and hygiene",
            "redaction-reviewed",
            "local path disclosure",
            "non-public or non-current repo links",
        ]
        for marker in proof_markers:
            self.assertIn(marker, proof_doc)

        for link in profile_check.REQUIRED_INTERNAL_LINKS:
            self.assertIn(link, readme)

    def test_public_feedback_and_private_workbench_docs_are_bounded(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        proof_doc = Path("docs/profile-proof-surface.md").read_text(encoding="utf-8")
        hardening = Path("docs/public-feedback-hardening.md").read_text(
            encoding="utf-8"
        )
        workbench = Path("docs/private-mimesis-workbench.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/public-feedback-hardening.md", readme)
        self.assertIn("docs/private-mimesis-workbench.md", readme)
        self.assertIn("Public Feedback Hardening", hardening)
        self.assertIn("OpenClaude stays the local runtime substrate", hardening)
        self.assertIn("Meta + MFH + Orchestra OS", hardening)
        self.assertIn("behavioral smoke tests", hardening)
        self.assertIn(
            "dependency-cruiser topology, jscpd duplicate-shape, Knip dead-export triage ledger and first candidate reductions, public artifact hygiene, and provider-id redaction gates",
            hardening,
        )
        self.assertIn("not proof that those workstreams are complete", proof_doc)

        workbench_markers = [
            "Private Mimesis Workbench",
            "private/local research workbench",
            "not public proof",
            "not external validation",
            "Current local snapshot",
            "local-only evidence",
            "board-v1-inspection-manifest.json",
            "raw-transcript-preflight.json",
            "raw-transcript-redaction-review-preflight.json",
            "PR #25-#32 blocker and hygiene gates",
            "redaction-reviewed raw rows",
            "Board v1 is not ready",
            "The private workbench proves Mimesis Engineering.",
            "Mimesis suppresses hallucination/fabrication in general.",
        ]
        for marker in workbench_markers:
            self.assertIn(marker, workbench)

    def test_validation_catches_missing_private_workbench_evidence_link(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        readme_without_workbench = readme.replace(
            "docs/private-mimesis-workbench.md",
            "docs/missing-private-mimesis-workbench.md",
        )

        issues = validate_readme_text(readme_without_workbench)

        self.assertTrue(any("docs/private-mimesis-workbench.md" in issue for issue in issues))

    def test_render_parity_validator_checks_public_surfaces_and_routes(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        fetched_urls = []

        def fake_fetcher(url):
            fetched_urls.append(url)
            if url in {surface_url for _, surface_url in PUBLIC_SURFACES}:
                return 200, readme
            if url in ROUTE_URLS:
                return 200, "ok"
            return 404, ""

        self.assertEqual(validate_render_parity("README.md", fake_fetcher), [])
        for _, url in PUBLIC_SURFACES:
            self.assertIn(url, fetched_urls)
        for url in ROUTE_URLS:
            self.assertIn(url, fetched_urls)

    def test_render_parity_validator_checks_maintenance_hidden_routes(self):
        readme = Path("README.md").read_text(encoding="utf-8")

        def fake_fetcher(url):
            if url in {surface_url for _, surface_url in PUBLIC_SURFACES}:
                return 200, readme
            if url in ROUTE_URLS:
                return 200, "<body data-maintenance-page>공사중입니다</body>"
            return 404, ""

        issues = validate_render_parity("README.md", fake_fetcher)

        self.assertTrue(any("maintenance route missing noindex" in issue for issue in issues))

    def test_render_parity_validator_catches_stale_rendered_surface(self):
        readme = Path("README.md").read_text(encoding="utf-8")

        def fake_fetcher(url):
            if url == "https://github.com/svy04":
                return 200, "Mimesis v.next Workbench"
            if url in {surface_url for _, surface_url in PUBLIC_SURFACES}:
                return 200, readme
            if url in ROUTE_URLS:
                return 200, "ok"
            return 404, ""

        issues = validate_render_parity("README.md", fake_fetcher)

        self.assertTrue(any("forbidden render marker" in issue for issue in issues))

    def test_render_parity_validator_catches_positive_claim_drift(self):
        readme = Path("README.md").read_text(encoding="utf-8")

        def fake_fetcher(url):
            if url == "https://github.com/svy04":
                return 200, "OpenClaude is the main thesis and flagship product."
            if url in {surface_url for _, surface_url in PUBLIC_SURFACES}:
                return 200, readme
            if url in ROUTE_URLS:
                return 200, "ok"
            return 404, ""

        issues = validate_render_parity("README.md", fake_fetcher)

        self.assertTrue(any("forbidden render marker" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
