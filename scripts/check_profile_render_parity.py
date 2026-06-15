import argparse
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
    "https://svy04.github.io/proof-artifacts/digital-factory-workbench-verification-2026-06-15/",
    "https://svy04.github.io/proof-artifacts/mimesis-verification-relocation-2026-06-15/",
    "https://svy04.github.io/proof-artifacts/mimesis-external-oss-attribution-two-repro-cards-2026-06-15/",
    "https://svy04.github.io/proof-artifacts/mimesis-downstream-reinjection-law-2026-06-15/",
    "https://svy04.github.io/proof-artifacts/mimesis-minecraft-high-integration-evidence-card-2026-06-15/",
    "https://svy04.github.io/human-made-feeling-bench/",
]

REQUIRED_RENDER_MARKERS = [
    "I build proof-bounded AI operating systems.",
    "Metaforge",
    "Meta for operating memory",
    "MFH for evidence gates",
    "Orchestra for multi-agent routing",
    "OpenClaude is the local CLI/runtime substrate",
    "not the main thesis",
    "Mimesis Engineering",
    "Give AI standards, not roles",
    "The active Digital Factory workbench",
    "Evidence Card Contract",
    "conditional lift, not universal lift",
    "I do not claim Metaforge is production-ready",
    "I do not claim NoiseProof is production-ready",
    "I do not claim Mimesis Engineering is an industry standard",
]

FORBIDDEN_RENDER_MARKERS = [
    "Current flagship:",
    "Mimesis v.next Workbench",
    "Mimesis Engineering v0",
    "public v0 artifact-level imitation method",
    "OpenClaude is the main thesis",
    "flagship product",
    "Board v1 is ready",
    "industry standard for AI output improvement",
    "external validation from reviewers",
    "16/16 expert modules",
    "per-arm build logs remain missing",
    "per-arm build logs are still missing",
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
