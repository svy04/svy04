import argparse
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REQUIRED_LINKS = [
    "https://github.com/svy04/metaforge",
    "https://github.com/svy04/metaforge/blob/main/docs/marketing/metaforge-public-proof-pack-2026-06-14.md",
    "https://github.com/svy04/noiseproof-agent",
    "https://github.com/svy04/noiseproof-agent/blob/main/docs/review/external-reader-phase-897-current-proof-packet-refresh.md",
    "https://github.com/svy04/mimesis-engineering",
    "https://github.com/svy04/mimesis-canvas",
    "https://github.com/svy04/mimesis-casebook",
    "https://github.com/svy04/svy04",
    "https://github.com/svy04/leaderboard-data",
    "https://github.com/svy04/svy04/actions/workflows/profile-readme.yml",
    "https://svy04.github.io/proof-artifacts/github-profile-readme-proof-surface-2026-06-14/",
    "https://svy04.github.io/proof-artifacts/mimesis-visual-failure-packet-2026-06-15/",
    "https://svy04.github.io/proof-artifacts/digital-factory-workbench-verification-2026-06-15/",
    "https://svy04.github.io/proof-artifacts/mimesis-verification-relocation-2026-06-15/",
    "https://svy04.github.io/proof-artifacts/mimesis-downstream-reinjection-law-2026-06-15/",
    "https://svy04.github.io/proof-artifacts/mimesis-minecraft-high-integration-evidence-card-2026-06-15/",
    "https://svy04.github.io/human-made-feeling-bench/",
]

REQUIRED_INTERNAL_LINKS = [
    "docs/profile-proof-surface.md",
    "docs/profile-render-parity-proof-packet.md",
    "docs/private-mimesis-workbench.md",
]

REQUIRED_BADGE_URLS = [
    "https://github.com/svy04/svy04/actions/workflows/profile-readme.yml/badge.svg?branch=main",
    "https://img.shields.io/badge/claim%20boundary-documented-555",
]

REQUIRED_MARKERS = [
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
    "docs/private-mimesis-workbench.md",
    "source first",
    "artifacts before personas",
    "standards before vibes",
    "gates before claims",
    "conditional lift, not universal lift",
    "Not a trading bot",
    "not product-complete",
    "not externally validated",
    "private/local",
    "prototype plugin surfaces",
    "expert modules",
    "Evidence Card Contract",
    "source artifact",
    "baseline output",
    "conditioned output",
    "wrong-anchor or checklist control",
    "gate/scorer",
    "failure cases",
    "proof-surface discipline",
    "Mimesis Visual Failure Packet",
    "Private Workbench Verification Snapshot",
    "Mimesis Verification Relocation Packet",
    "Mimesis Downstream Reinjection Law",
    "Mimesis Minecraft High-Integration Evidence Card",
    "Human-made Feeling Bench",
    "first-pass rubric",
    "not a universal design-quality benchmark",
    "redacted failure artifact",
    "redacted local hygiene artifact",
    "redacted method-boundary artifact",
    "redacted local evidence card",
    "banned-claim boundary",
    "validation does not transfer",
    "underdetermined task plus slop-contaminated prior",
    "not L5 proof",
    "human visual-quality proof",
    "near-Fable proof",
    "public benchmark status",
    "no true wrong-anchor",
    "n=2 per cell",
    "GitHub Profile README Proof Surface",
    "render parity proof packet",
    "CI-checked routing and claim-boundary surface",
    "statistical significance",
    "hallucination suppression",
    "universal hallucination suppression",
    "public framework, reference packs, validators, cases, and proof boundaries",
    "worksheet surface",
    "case surface",
    "visual quality improvement",
    "not external validation",
    "It does not universally improve AI output.",
    "I do not claim Metaforge is production-ready",
    "I do not claim NoiseProof is production-ready",
    "I do not claim Mimesis Engineering is an industry standard",
]

PROHIBITED_MARKERS = [
    "Current flagship:",
    "Mimesis v.next Workbench",
    "Mimesis Engineering v0",
    "public v0 artifact-level imitation method",
]

WINDOWS_USER_PATH_PATTERN = "C:" + r"[\\/]+Users[\\/]+"
POSIX_ADMIN_PATH_PATTERN = "/" + "Users" + "/" + "admin"
KOREAN_PRIVATE_PATH_PATTERN = "\ub0b4 \uc21c\uc218 \uc7ac\ubbf8"
DIGITAL_FACTORY_PATH_PATTERN = "Digital Factory" + r"[\\/]"

LOCAL_PATH_PATTERN = re.compile(
    "|".join(
        [
            WINDOWS_USER_PATH_PATTERN,
            POSIX_ADMIN_PATH_PATTERN,
            KOREAN_PRIVATE_PATH_PATTERN,
            DIGITAL_FACTORY_PATH_PATTERN,
        ]
    )
)


def extract_markdown_links(text):
    link_entries = []
    consumed_spans = []
    for match in re.finditer(r"\[!\[[^\]]+\]\((https?://[^)]+)\)\]\((https?://[^)]+)\)", text):
        image_url, target_url = match.groups()
        link_entries.append((match.start(), 0, image_url))
        link_entries.append((match.start(), 1, target_url))
        consumed_spans.append(match.span())
    for match in re.finditer(r"(!?)\[[^\]]+\]\((https?://[^)]+)\)", text):
        if any(start <= match.start() < end for start, end in consumed_spans):
            continue
        is_image = bool(match.group(1))
        url = match.group(2)
        if not is_image:
            link_entries.append((match.start(), 0, url))
    return [url for _, _, url in sorted(link_entries)]


def _line_allows_dangerous_claim(line):
    lowered = line.lower()
    return (
        "do not claim" in lowered
        or "not " in lowered
        or "does not" in lowered
        or "boundary" in lowered
    )


def validate_readme_text(text):
    issues = []

    for marker in REQUIRED_MARKERS:
        if marker not in text:
            issues.append(f"missing required marker: {marker}")

    for marker in PROHIBITED_MARKERS:
        if marker in text:
            issues.append(f"prohibited profile marker: {marker}")

    for link in REQUIRED_LINKS:
        if link not in text:
            issues.append(f"missing required link: {link}")

    for link in REQUIRED_INTERNAL_LINKS:
        if link not in text:
            issues.append(f"missing required internal link: {link}")

    for badge_url in REQUIRED_BADGE_URLS:
        if badge_url not in text:
            issues.append(f"missing required badge URL: {badge_url}")

    dangerous_patterns = [
        ("unbounded Mimesis claim", r"\bMimesis(?: Engineering)?\b.*\b(proven|universally improves)\b"),
        ("unbounded product-readiness claim", r"\b(is|are) production-ready\b"),
        ("unbounded external-validation claim", r"\b(is|are) externally validated\b"),
    ]

    for line in text.splitlines():
        if LOCAL_PATH_PATTERN.search(line):
            issues.append(f"local path disclosure: {line.strip()}")
        for label, pattern in dangerous_patterns:
            if re.search(pattern, line, flags=re.IGNORECASE) and not _line_allows_dangerous_claim(line):
                issues.append(f"{label}: {line.strip()}")

    return issues


def check_url(url, timeout=15):
    request = Request(url, headers={"User-Agent": "svy04-profile-readme-check/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            status = getattr(response, "status", 200)
    except HTTPError as exc:
        status = exc.code
    except URLError as exc:
        return f"{url} -> {exc.reason}"

    if 200 <= status < 400:
        return None
    return f"{url} -> HTTP {status}"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate the svy04 profile README claim surface and links."
    )
    parser.add_argument("--readme", default="README.md")
    parser.add_argument(
        "--check-links",
        action="store_true",
        help="Perform live HTTP checks for markdown links.",
    )
    args = parser.parse_args(argv)

    readme_path = Path(args.readme)
    text = readme_path.read_text(encoding="utf-8")
    issues = validate_readme_text(text)

    if args.check_links:
        for url in sorted(set(extract_markdown_links(text)) - set(REQUIRED_BADGE_URLS)):
            issue = check_url(url)
            if issue:
                issues.append(issue)

    if issues:
        for issue in issues:
            print(f"ERROR: {issue}", file=sys.stderr)
        return 1

    print("Profile README claim and link surface checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
