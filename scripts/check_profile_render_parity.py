import argparse
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PUBLIC_SURFACES = [
    (
        "raw profile README",
        "https://raw.githubusercontent.com/svy04/svy04/main/README.md",
    ),
    ("rendered GitHub profile", "https://github.com/svy04"),
    ("rendered profile repo README", "https://github.com/svy04/svy04"),
]

ROUTE_URLS = [
    "https://github.com/svy04/svy04/actions/workflows/profile-readme.yml",
    "https://github.com/svy04/svy04/actions/workflows/profile-readme.yml/badge.svg?branch=main",
    "https://svy04.github.io/proof-artifacts/github-profile-readme-proof-surface-2026-06-14/",
    "https://svy04.github.io/proof-artifacts/mimesis-visual-failure-packet-2026-06-15/",
    "https://svy04.github.io/proof-artifacts/mimesis-verification-relocation-2026-06-15/",
    "https://svy04.github.io/proof-artifacts/mimesis-external-oss-attribution-two-repro-cards-2026-06-15/",
    "https://svy04.github.io/proof-artifacts/mimesis-downstream-reinjection-law-2026-06-15/",
    "https://svy04.github.io/proof-artifacts/mimesis-minecraft-high-integration-evidence-card-2026-06-15/",
    "https://svy04.github.io/proof-artifacts/mimesis-minecraft-public-redacted-board-v0-2026-06-15/",
    "https://svy04.github.io/proof-artifacts/mimesis-minecraft-transcript-availability-audit-2026-06-15/",
    "https://svy04.github.io/human-made-feeling-bench/",
    "https://github.com/svy04/mimesis-engineering/blob/main/STATUS.md",
    "https://github.com/svy04/mimesis-engineering/blob/main/PROOF-BOUNDARY.md",
    "https://github.com/svy04/mimesis-engineering/blob/main/docs/PUBLIC-CLAIM-PACK.md",
]

REQUIRED_RENDER_MARKERS = [
    "I build proof-bounded AI operating systems: evidence before pitch.",
    "Current proof ledger",
    "the method layer. It is a Markdown-first",
    "Build the proof surface before the pitch",
    "Markdown-first, artifact-first AI-native work framework",
    "makes expert process visible",
    "Public Status",
    "Proof Boundary",
    "Public Claim Pack",
    "Metaforge = Meta + MFH + Orchestra OS",
    "Metaforge",
    "Meta stores operating memory",
    "MFH gates closure",
    "Orchestra routes agents",
    "representative cross-goal trace pack",
    "validated=2, rejected=1, blocked=1",
    "goal_ids=CG-001,CG-002",
    "OpenClaude is runtime substrate",
    "Claude and Codex routes belong under the OS, not above it",
    "not the main thesis",
    "public repo evidence, not non-public research proof",
    "non-public Mimesis research boundary",
    "Mimesis Engineering",
    "give AI standards, not roles",
    "Evidence Card Contract",
    "conditional lift, not universal lift",
    "fresh verifier output is required before any adoption, benchmark, module-pass, or promotion claim",
    "claim hygiene, evidence-reference checks, module validation, null/negative controls, failure records, and explicit non-readiness gates",
    "I publish the null boundary beside the wins",
    "I do not claim Metaforge is production-ready",
    "I do not claim NoiseProof is production-ready",
    "I do not claim Mimesis Engineering is an industry standard",
]

FORBIDDEN_RENDER_MARKERS = [
    "Current flagship:",
    "Mimesis Engineering is the front door",
    "private/local " + "workbench is the current " + "canon input",
    "Mimesis Engineering is the operating layer I am building now.",
    "Mimesis v.next " + "Workbench",
    "Mimesis Engineering " + "v0",
    "public v0 artifact-level " + "imitation method",
    "OpenClaude is the main thesis",
    "flagship product",
    "Metaforge PRs #",
    "PR #70-#77",
    "Private Workbench Verification Snapshot",
    "digital-factory-workbench-verification",
    "Board v1 is ready",
    "industry standard for AI output improvement",
    "external validation from reviewers",
    "16/16 expert modules",
    "14/14 expert modules",
    "Current local checks pass",
    "Local checks pass",
    "per-arm build logs remain missing",
    "per-arm build logs are still missing",
]

PROOF_ROUTE_HOST = "https://svy04.github.io/"

PROOF_ROUTE_BOUNDARY_MARKERS = [
    "claim boundary",
    "does not prove",
    "not proof",
    "not public proof",
    "not external validation",
    "not production readiness",
    "not production-ready",
    "not stronger proof",
    "not universal",
    "not a universal",
    "board v1 is not ready",
]


def fetch_url(url, timeout=20):
    request = Request(url, headers={"User-Agent": "svy04-profile-render-parity/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            text = response.read().decode("utf-8", "replace")
    except HTTPError as exc:
        return exc.code, ""
    except URLError as exc:
        return None, str(exc.reason)
    return status, text


def validate_text_surface(label, text):
    issues = []
    for marker in REQUIRED_RENDER_MARKERS:
        if marker not in text:
            issues.append(f"{label}: missing render marker: {marker}")
    for marker in FORBIDDEN_RENDER_MARKERS:
        if marker in text:
            issues.append(f"{label}: forbidden render marker: {marker}")
    return issues


def validate_status_url(label, url, fetcher=fetch_url):
    status, body = fetcher(url)
    if status is None:
        return [f"{label}: {url} -> {body}"]
    if not 200 <= status < 400:
        return [f"{label}: {url} -> HTTP {status}"]
    if "data-maintenance-page" in body:
        issues = []
        if not re.search(r'<meta\s+name="?robots"?\s+content="?noindex,\s*nofollow"?', body):
            issues.append(f"{label}: {url} maintenance route missing noindex,nofollow")
        if "공사중입니다" not in body or "아직 완성 전이라 공개하지 않습니다" not in body:
            issues.append(f"{label}: {url} maintenance route missing public disclosure")
        return issues
    if url.startswith(PROOF_ROUTE_HOST):
        normalized_body = body.lower()
        if not any(marker in normalized_body for marker in PROOF_ROUTE_BOUNDARY_MARKERS):
            return [f"{label}: {url} missing proof-boundary marker"]
    return []


def validate_render_parity(readme_path, fetcher=fetch_url):
    issues = []
    local_readme = Path(readme_path).read_text(encoding="utf-8")
    issues.extend(validate_text_surface("local profile README", local_readme))

    for label, url in PUBLIC_SURFACES:
        status, text = fetcher(url)
        if status is None:
            issues.append(f"{label}: {url} -> {text}")
            continue
        if not 200 <= status < 400:
            issues.append(f"{label}: {url} -> HTTP {status}")
            continue
        issues.extend(validate_text_surface(label, text))

    for url in ROUTE_URLS:
        issues.extend(validate_status_url("linked proof route", url, fetcher))

    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check that the profile source, rendered GitHub surfaces, and proof routes agree."
    )
    parser.add_argument("--readme", default="README.md")
    args = parser.parse_args(argv)

    issues = validate_render_parity(args.readme)
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}", file=sys.stderr)
        return 1

    print("Profile render parity checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
