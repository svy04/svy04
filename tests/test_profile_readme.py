import unittest
from pathlib import Path

from scripts import check_profile_readme as profile_check
from scripts.check_profile_render_parity import (
    PUBLIC_SURFACES,
    ROUTE_URLS,
    PROOF_ROUTE_HOST,
    validate_render_parity,
)
from scripts.check_profile_readme import (
    REQUIRED_BADGE_URLS,
    REQUIRED_LINKS,
    extract_markdown_links,
    validate_readme_text,
)


class ProfileReadmeTests(unittest.TestCase):
    LIVE_PROOF_ROUTE_BODY = "Claim Boundary: this route does not prove production readiness."

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

    def test_live_link_checker_retries_transient_5xx(self):
        class Response:
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, traceback):
                return False

        calls = []

        def fake_urlopen(request, timeout):
            calls.append((request.full_url, timeout))
            if len(calls) == 1:
                raise profile_check.HTTPError(
                    request.full_url,
                    503,
                    "Service Unavailable",
                    hdrs=None,
                    fp=None,
                )
            return Response()

        issue = profile_check.check_url(
            "https://svy04.github.io/proof-artifacts/example/",
            timeout=1,
            retries=1,
            opener=fake_urlopen,
            sleeper=lambda _seconds: None,
        )

        self.assertIsNone(issue)
        self.assertEqual(len(calls), 2)

    def test_live_link_checker_does_not_retry_non_transient_4xx(self):
        calls = []

        def fake_urlopen(request, timeout):
            calls.append((request.full_url, timeout))
            raise profile_check.HTTPError(
                request.full_url,
                404,
                "Not Found",
                hdrs=None,
                fp=None,
            )

        issue = profile_check.check_url(
            "https://svy04.github.io/proof-artifacts/missing/",
            timeout=1,
            retries=2,
            opener=fake_urlopen,
            sleeper=lambda _seconds: None,
        )

        self.assertEqual(
            issue,
            "https://svy04.github.io/proof-artifacts/missing/ -> HTTP 404",
        )
        self.assertEqual(len(calls), 1)

    def test_current_readme_has_required_links_and_claim_boundaries(self):
        readme = Path("README.md").read_text(encoding="utf-8")

        issues = validate_readme_text(readme)

        self.assertEqual(issues, [])
        self.assertLess(len(readme), 8200)
        for link in REQUIRED_LINKS:
            self.assertIn(link, readme)
        for link in profile_check.REQUIRED_INTERNAL_LINKS:
            self.assertIn(link, readme)
        for badge_url in REQUIRED_BADGE_URLS:
            self.assertIn(badge_url, readme)

        current_metaforge_links = [
            "https://github.com/svy04/metaforge/blob/main/docs/product-quality/public-feedback-snapshot-2026-06-19.md",
            "https://github.com/svy04/metaforge/blob/main/docs/product-quality/goal-trace-validation-report.md",
            "https://github.com/svy04/metaforge/blob/main/docs/goals/traces/CG-001-goal-kernel-mvp.trace.json",
        ]
        for link in current_metaforge_links:
            self.assertIn(link, readme)

        required_sections = [
            "## Current Build",
            "## Public Systems",
            "## Proof Routes",
            "## Operating Law",
            "## Claim Boundary",
        ]
        for section in required_sections:
            self.assertIn(section, readme)

        positioning_markers = [
            "Current proof ledger",
            "Mimesis Engineering is the method layer",
            "I build proof-bounded AI operating systems: evidence before pitch.",
            "Build the proof surface before the pitch",
            "Metaforge is the headline",
            "OpenClaude is not the headline",
            "artifact-first expert-thinking OS",
            "make expert process visible",
            "cognitive apprenticeship",
            "worked examples",
            "Public repo evidence, not non-public research proof",
            "public Mimesis repos are support surfaces",
            "Metaforge = Meta + MFH + Orchestra OS",
            "Metaforge is the public operating-system repo",
            "OpenClaude is runtime substrate",
            "Public claim evidence map",
            "allowed claims, explicit non-claims, and unresolved gaps",
            "Metaforge public hardening tracks dependency topology, duplicate-shape ratchets, dead-export triage, public artifact hygiene, provider-id redaction, remote-surface privacy, hosted-trust boundaries, IDE evidence ordering, and public wiring evidence",
            "Metaforge wiring evidence map",
            "runtime import, governance/docs/gates, non-public research boundary, and manual artifact lane",
            "not the main thesis",
            "2026-06-19 public feedback packet",
            "provenance is a trust surface",
            "MFH goal-trace validation report",
            "local no-provider behavioral governance evidence",
            "Goal Kernel closure",
            "non-public Mimesis research boundary",
            "Public-safe proof routes summarize redacted local hygiene and blockers",
            "Fresh verifier output is required before any stronger module-pass or promotion claim",
            "AI에게 역할이 아니라 기준을 준다.",
            "give AI standards, not roles",
            "products, papers, patents, standards, and maintained open-source implementations",
            "inspection manifests",
            "worked example",
            "Proof ledger",
            "Mimesis Minecraft High-Integration Evidence Card",
            "Public redacted board v0 / incomplete evidence board",
            "Non-Public Mimesis Research Boundary",
            "Board v1 is not ready",
            "It does not universally improve AI output.",
            "I do not claim Metaforge is production-ready",
            "I do not claim Mimesis Engineering is an industry standard",
            "I do not claim NoiseProof is production-ready",
            "Support surface, not a hidden canon claim",
            "Public repo map, not adoption proof",
            "Public support surface for reference packs, validators, cases, and proof boundaries",
            "Worksheet surface",
            "Case surface",
            "Non-public research notes are not a public release claim",
            "happy path -> edge case -> side-effect guard -> claim boundary",
        ]
        for marker in positioning_markers:
            self.assertIn(marker, readme)

        forbidden_markers = [
            "Current flagship:",
            "Mimesis Engineering is the front door",
            "private/local " + "workbench is the current " + "canon input",
            "Mimesis Engineering " + "v0",
            "public v0 artifact-level " + "imitation method",
            "Mimesis v.next " + "Workbench",
            "16/16 expert modules",
            "14/14 expert modules",
            "Current local checks pass",
            "Local checks pass",
            "OpenClaude is the main thesis",
            "Metaforge PRs #70-#77",
            "digital-factory-workbench-verification",
            "PR #27",
            "PR #28-style raw transcript hygiene hardening",
            "PR #63 adds canonical extension hygiene coverage",
            "## Current Thesis",
            "## Public Repos",
            "Mimesis Engineering is the operating layer I am building now.",
        ]
        for marker in forbidden_markers:
            self.assertNotIn(marker, readme)
        self.assertNotIn(
            "https://svy04.github.io/proof-artifacts/digital-factory-workbench-verification-2026-06-15/",
            profile_check.REQUIRED_LINKS,
        )

    def test_public_surfaces_use_neutral_non_public_research_boundary_language(self):
        stale_surface_markers = [
            "private-" + "workbench",
            "private " + "workbench",
            "private/local " + "workbench",
            "private/local Mimesis Engineering " + "workbench",
            "private Mimesis " + "workbench",
            "private " + "workbench evidence",
            "private " + "plugin gate",
            "current private " + "canon",
            "current " + "canon",
            "Mimesis v.next " + "Workbench",
            "Mimesis Engineering " + "v0",
            "public v0 artifact-level " + "imitation method",
        ]
        scanned_paths = [
            "README.md",
            "docs/profile-proof-surface.md",
            "docs/profile-render-parity-proof-packet.md",
            "docs/non-public-mimesis-research-boundary.md",
            "scripts/check_profile_readme.py",
            "scripts/check_profile_render_parity.py",
        ]

        for path in scanned_paths:
            text = Path(path).read_text(encoding="utf-8")
            for marker in stale_surface_markers:
                self.assertNotIn(marker, text, path)

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
            + "\n| [Mimesis Engineering "
            + "v0](https://github.com/svy04/mimesis-engineering) | public v0 artifact-level "
            + "imitation method |\n"
            + "\n## Mimesis v.next "
            + "Workbench\n"
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

    def test_validation_catches_private_workbench_name_disclosure(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        private_workbench_name = "Digital" + " Factory"
        disclosed = readme + f"\n{private_workbench_name} is the active workbench.\n"

        issues = validate_readme_text(disclosed)

        self.assertTrue(
            any("non-public research name disclosure" in issue for issue in issues)
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
        self.assertIn("github.ref == 'refs/heads/main'", workflow)
        self.assertIn("python scripts/check_public_github_surface_hygiene.py", workflow)
        self.assertIn(
            "python scripts/check_public_github_surface_hygiene.py --repo svy04 --include-non-default-branches",
            workflow,
        )
        self.assertIn("GITHUB_TOKEN: ${{ github.token }}", workflow)

        proof_markers = [
            "Profile README Proof Surface",
            "source/CI proof and live public rendering stay separate",
            "live maintenance-hidden",
            "Public GitHub Surface Hygiene Proof Packet",
            "scripts/check_public_github_surface_hygiene.py",
            "public default branches",
            "stale profile branches",
            "non-public research name disclosure",
            "scanner-unfriendly placeholders",
            "actual-looking bearer values",
            "raw auth transcript markers",
            "python scripts/check_profile_render_parity.py",
            "main, scheduled, and manual workflow runs",
            "python scripts/check_public_github_surface_hygiene.py --repo svy04 --include-non-default-branches",
            "non-public-mimesis-research-boundary.md",
            "Metaforge-first profile framing",
            "current proof ledger",
            "raw-transcript-preflight.json",
            "raw-transcript-redaction-review-preflight.json",
            "non-public research blocker and hygiene",
            "PR #25-#33 blocker and hygiene",
            "manifest-promotion-blockers.json",
            "redaction-reviewed",
            "local path disclosure",
            "non-public or non-current repo links",
        ]
        for marker in proof_markers:
            self.assertIn(marker, proof_doc)

        for link in REQUIRED_LINKS:
            self.assertIn(link, proof_doc)

        for link in profile_check.REQUIRED_INTERNAL_LINKS:
            self.assertIn(link, readme)

    def test_render_parity_packet_documents_checked_routes(self):
        parity_doc = Path("docs/profile-render-parity-proof-packet.md").read_text(
            encoding="utf-8"
        )

        for url in ROUTE_URLS:
            self.assertIn(url, parity_doc)
        for _, url in PUBLIC_SURFACES:
            self.assertIn(url, parity_doc)

    def test_public_feedback_and_non_public_research_docs_are_bounded(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        proof_doc = Path("docs/profile-proof-surface.md").read_text(encoding="utf-8")
        hardening = Path("docs/public-feedback-hardening.md").read_text(
            encoding="utf-8"
        )
        research_boundary = Path("docs/non-public-mimesis-research-boundary.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/public-feedback-hardening.md", readme)
        self.assertIn("docs/non-public-mimesis-research-boundary.md", readme)
        self.assertIn("Public Feedback Hardening", hardening)
        self.assertIn("OpenClaude stays the local runtime substrate", hardening)
        self.assertIn("Meta + MFH + Orchestra OS", hardening)
        self.assertIn("behavioral smoke tests", hardening)
        self.assertIn(
            "dependency topology, duplicate-shape ratchets",
            hardening,
        )
        self.assertIn("public wiring evidence are ratchets", hardening)
        self.assertIn("not proof that those workstreams are complete", proof_doc)

        research_boundary_markers = [
            "Non-Public Mimesis Research Boundary",
            "non-public Mimesis research source",
            "not public proof",
            "not external validation",
            "Current local snapshot",
            "Snapshot checked on 2026-06-18 KST",
            "verify_public_hygiene.py",
            "local-only evidence",
            "board-v1-inspection-manifest.json",
            "manifest-promotion-blockers.json",
            "raw-transcript-preflight.json",
            "raw-transcript-redaction-review-preflight.json",
            "PR #25-#33 blocker and hygiene gates",
            "redaction-reviewed raw rows",
            "Board v1 is not ready",
            "The non-public research source proves Mimesis Engineering.",
            "Mimesis suppresses hallucination/fabrication in general.",
        ]
        for marker in research_boundary_markers:
            self.assertIn(marker, research_boundary)

    def test_validation_catches_missing_non_public_research_boundary_link(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        readme_without_boundary = readme.replace(
            "docs/non-public-mimesis-research-boundary.md",
            "docs/missing-non-public-mimesis-research-boundary.md",
        )

        issues = validate_readme_text(readme_without_boundary)

        self.assertTrue(any("docs/non-public-mimesis-research-boundary.md" in issue for issue in issues))

    def test_render_parity_validator_checks_public_surfaces_and_routes(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        fetched_urls = []

        def fake_fetcher(url):
            fetched_urls.append(url)
            if url in {surface_url for _, surface_url in PUBLIC_SURFACES}:
                return 200, readme
            if url in ROUTE_URLS:
                return 200, self.LIVE_PROOF_ROUTE_BODY
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

    def test_render_parity_validator_catches_live_proof_route_without_boundary(self):
        readme = Path("README.md").read_text(encoding="utf-8")

        def fake_fetcher(url):
            if url in {surface_url for _, surface_url in PUBLIC_SURFACES}:
                return 200, readme
            if url.startswith(PROOF_ROUTE_HOST):
                return 200, "reachable route with product-looking copy"
            if url in ROUTE_URLS:
                return 200, self.LIVE_PROOF_ROUTE_BODY
            return 404, ""

        issues = validate_render_parity("README.md", fake_fetcher)

        self.assertTrue(any("missing proof-boundary marker" in issue for issue in issues))

    def test_render_parity_validator_catches_stale_rendered_surface(self):
        readme = Path("README.md").read_text(encoding="utf-8")

        def fake_fetcher(url):
            if url == "https://github.com/svy04":
                return 200, "Mimesis v.next " + "Workbench"
            if url in {surface_url for _, surface_url in PUBLIC_SURFACES}:
                return 200, readme
            if url in ROUTE_URLS:
                return 200, self.LIVE_PROOF_ROUTE_BODY
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
                return 200, self.LIVE_PROOF_ROUTE_BODY
            return 404, ""

        issues = validate_render_parity("README.md", fake_fetcher)

        self.assertTrue(any("forbidden render marker" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
