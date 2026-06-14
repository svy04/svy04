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
        for link in REQUIRED_LINKS:
            self.assertIn(link, readme)
        required_internal_links = getattr(profile_check, "REQUIRED_INTERNAL_LINKS", [])
        self.assertIn("docs/private-mimesis-workbench.md", required_internal_links)
        self.assertIn("docs/profile-render-parity-proof-packet.md", required_internal_links)
        for link in required_internal_links:
            self.assertIn(link, readme)
        for badge_url in REQUIRED_BADGE_URLS:
            self.assertIn(badge_url, readme)

        self.assertIn("Metaforge", readme)
        self.assertIn("Meta for operating memory", readme)
        self.assertIn("MFH for evidence gates", readme)
        self.assertIn("Orchestra for multi-agent routing", readme)
        self.assertIn("OpenClaude is the local CLI/runtime substrate", readme)
        self.assertIn("The active Digital Factory workbench", readme)
        self.assertIn("conditional lift, not universal lift", readme)
        self.assertIn("Evidence Card Contract", readme)
        self.assertIn("source artifact", readme)
        self.assertIn("baseline output", readme)
        self.assertIn("conditioned output", readme)
        self.assertIn("wrong-anchor or checklist control", readme)
        self.assertIn("gate/scorer", readme)
        self.assertIn("failure cases", readme)
        self.assertIn("proof-surface discipline", readme)
        self.assertIn("Human-made Feeling Bench", readme)
        self.assertIn("first-pass rubric", readme)
        self.assertIn("not a universal design-quality benchmark", readme)
        self.assertIn("public framework, reference packs, validators, cases, and proof boundaries", readme)
        self.assertIn("GitHub Profile README Proof Surface", readme)
        self.assertIn("render parity proof packet", readme)
        self.assertIn("public GitHub surface hygiene proof packet", readme)
        self.assertIn("Public GitHub Surface Hygiene Proof Packet", readme)
        self.assertIn("CI-checked routing and claim-boundary surface", readme)
        self.assertIn("Mimesis Visual Failure Packet", readme)
        self.assertIn("Private Workbench Verification Snapshot", readme)
        self.assertIn("Mimesis Verification Relocation Packet", readme)
        self.assertIn("Mimesis Downstream Reinjection Law", readme)
        self.assertIn("Mimesis Minecraft High-Integration Evidence Card", readme)
        self.assertIn("Mimesis Minecraft Public Redacted Board v0", readme)
        self.assertIn("redacted failure artifact", readme)
        self.assertIn("redacted local hygiene artifact", readme)
        self.assertIn("redacted method-boundary artifact", readme)
        self.assertIn("redacted local evidence card", readme)
        self.assertIn("banned-claim boundary", readme)
        self.assertIn("validation does not transfer", readme)
        self.assertIn("underdetermined task plus slop-contaminated prior", readme)
        self.assertIn("not L5 proof", readme)
        self.assertIn("human visual-quality proof", readme)
        self.assertIn("near-Fable proof", readme)
        self.assertIn("public benchmark status", readme)
        self.assertIn("no true wrong-anchor", readme)
        self.assertIn("n=2 per cell", readme)
        self.assertIn("Promotion Blockers", readme)
        self.assertIn("public redacted board", readme)
        self.assertIn("public redacted board v0 / incomplete evidence board", readme)
        self.assertIn("promotion-blocked", readme)
        self.assertIn("source-use boundary", readme)
        self.assertIn("condition board", readme)
        self.assertIn("aggregate scoring", readme)
        self.assertIn("public-safe screenshots or links", readme)
        self.assertIn("public-safe per-arm screenshots", readme)
        self.assertIn("judge protocol", readme)
        self.assertIn("scorer transcript", readme)
        self.assertIn("full scorer transcript", readme)
        self.assertIn("failure record", readme)
        self.assertIn("per-arm build logs remain missing", readme)
        self.assertIn("board v1 collection plan", readme)
        self.assertIn("verify_minecraft_board_v1_gate.py", readme)
        self.assertIn("blocker contract, not stronger proof", readme)
        self.assertIn("board v1 is not ready", readme)
        self.assertIn("It does not universally improve AI output.", readme)
        self.assertIn("I do not claim Metaforge is production-ready", readme)
        self.assertIn("I do not claim Mimesis Engineering is an industry standard", readme)
        self.assertIn("I do not claim NoiseProof is production-ready", readme)
        self.assertNotIn("Current flagship:", readme)
        self.assertNotIn("Mimesis Engineering v0", readme)
        self.assertNotIn("public v0 artifact-level imitation method", readme)
        self.assertNotIn("Mimesis v.next Workbench", readme)
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

    def test_validation_catches_old_public_v0_or_vnext_as_primary_surface(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        stale_readme = (
            readme
            + "\n| [Mimesis Engineering v0](https://github.com/svy04/mimesis-engineering) | public v0 artifact-level imitation method |\n"
            + "\n## Mimesis v.next Workbench\n"
        )

        issues = validate_readme_text(stale_readme)

        self.assertTrue(
            any("prohibited profile marker" in issue for issue in issues)
        )

    def test_validation_catches_local_path_disclosure(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        disclosed_path = (
            "C:"
            + "\\Users\\owner\\"
            + "Private"
            + "\\README.md"
        )
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
        self.assertIn("python scripts/check_public_github_surface_hygiene.py", workflow)
        self.assertIn("Profile README Proof Surface", proof_doc)
        self.assertIn("workflow status badges", proof_doc)
        self.assertIn("Public GitHub Surface Hygiene Proof Packet", proof_doc)
        self.assertIn("scripts/check_public_github_surface_hygiene.py", proof_doc)
        self.assertIn("public default branches", proof_doc)
        self.assertIn("scanner-unfriendly placeholders", proof_doc)
        self.assertIn("not proof that public repositories contain no secrets", proof_doc)
        self.assertIn("private-mimesis-workbench.md", proof_doc)
        self.assertIn("private/local evidence map", proof_doc)
        self.assertIn("Mimesis visual route", proof_doc)
        self.assertIn("private workbench route", proof_doc)
        self.assertIn("Mimesis verification-relocation route", proof_doc)
        self.assertIn("Mimesis downstream reinjection route", proof_doc)
        self.assertIn("Mimesis Minecraft high-integration evidence-card route", proof_doc)
        self.assertIn("Mimesis Minecraft public board v0 route", proof_doc)
        self.assertIn("Human-made Feeling Bench route", proof_doc)
        self.assertIn("profile proof route", proof_doc)
        self.assertIn("Metaforge-first profile framing", proof_doc)
        self.assertIn("local path disclosure", proof_doc)
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
            "https://svy04.github.io/proof-artifacts/mimesis-minecraft-public-redacted-board-v0-2026-06-15/",
            proof_doc,
        )
        self.assertIn(
            "https://svy04.github.io/human-made-feeling-bench/",
            proof_doc,
        )
        self.assertIn("redacted failure artifact", proof_doc)
        self.assertIn("redacted local hygiene artifact", proof_doc)
        self.assertIn("redacted method-boundary artifact", proof_doc)
        self.assertIn("redacted local evidence card", proof_doc)
        self.assertIn("first-pass rubric", proof_doc)
        self.assertIn("not a universal design-quality benchmark", proof_doc)
        self.assertIn("validation does not transfer", proof_doc)
        self.assertIn("underdetermined task plus slop-contaminated prior", proof_doc)
        self.assertIn("not L5 proof", proof_doc)
        self.assertIn("near-Fable proof", proof_doc)
        self.assertIn("no true wrong-anchor", proof_doc)
        self.assertIn("Promotion Blockers", proof_doc)
        self.assertIn("public redacted board", proof_doc)
        self.assertIn("public redacted board v0 / incomplete evidence board", proof_doc)
        self.assertIn("promotion-blocked", proof_doc)
        self.assertIn("source-use boundary", proof_doc)
        self.assertIn("condition board", proof_doc)
        self.assertIn("aggregate scoring", proof_doc)
        self.assertIn("public-safe per-arm screenshots", proof_doc)
        self.assertIn("scorer transcript", proof_doc)
        self.assertIn("full scorer transcript", proof_doc)
        self.assertIn("failure record", proof_doc)
        self.assertIn("per-arm build logs are still missing", proof_doc)
        self.assertIn("board v1 collection plan", proof_doc)
        self.assertIn("verify_minecraft_board_v1_gate.py", proof_doc)
        self.assertIn("blocker contract, not stronger proof", proof_doc)
        self.assertIn("board v1 is not ready", proof_doc)
        self.assertIn("visibility upgrade, not stronger proof", proof_doc)
        self.assertIn("not prove universal output improvement", proof_doc)
        self.assertIn("not external validation", proof_doc)
        self.assertIn("not production readiness", proof_doc)
        self.assertIn("docs/profile-proof-surface.md", readme)
        self.assertIn("docs/profile-render-parity-proof-packet.md", readme)
        self.assertIn("docs/public-github-surface-hygiene-proof-packet.md", readme)

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
        self.assertIn("Mimesis Minecraft Public Redacted Board v0", workbench)
        self.assertIn("no true wrong-anchor weakness", workbench)
        self.assertIn("public redacted board", workbench)
        self.assertIn("incomplete evidence board", workbench)
        self.assertIn("source-use boundary", workbench)
        self.assertIn("condition board", workbench)
        self.assertIn("aggregate scoring", workbench)
        self.assertIn("public-safe per-arm screenshots", workbench)
        self.assertIn("scorer transcript", workbench)
        self.assertIn("failure record", workbench)
        self.assertIn("per-arm build logs are still missing", workbench)
        self.assertIn("Board readiness gates", workbench)
        self.assertIn("board v1 collection plan", workbench)
        self.assertIn("verify_minecraft_board_v1_gate.py", workbench)
        self.assertIn("blocker contract, not stronger proof", workbench)
        self.assertIn("Board v1 is not ready", workbench)
        self.assertIn("Source queue", workbench)
        self.assertIn("products, standards, OSS repos, patents, and evaluation systems", workbench)
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

        self.assertIn("Mimesis Visual Failure Packet", readme)
        self.assertIn("visual quality improvement", readme)
        self.assertIn("private prototype surface is private", proof_doc)
        self.assertIn("visual judgment evidence and expert gates", proof_doc)
        self.assertIn("visual quality improvement", proof_doc)
        self.assertIn("Mimesis Visual Failure Packet", workbench)
        self.assertIn("public redacted board", workbench)
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


if __name__ == "__main__":
    unittest.main()
