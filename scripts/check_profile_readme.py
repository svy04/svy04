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
    "https://github.com/svy04/svy04",
    "https://github.com/svy04/svy04/actions/workflows/profile-readme.yml",
]

REQUIRED_INTERNAL_LINKS = [
    "docs/profile-proof-surface.md",
    "docs/digital-factory-workbench.md",
]

REQUIRED_BADGE_URLS = [
    "https://github.com/svy04/svy04/actions/workflows/profile-readme.yml/badge.svg?branch=main",
    "https://img.shields.io/badge/claim%20boundary-documented-555",
]

REQUIRED_MARKERS = [
    "I build proof-bounded AI operating systems.",
    "source first",
    "artifacts before personas",
    "gates before claims",
    "logs before polish",
    "Not a trading bot",
    "not product-complete",
    "not externally validated",
    "private/local research workbench",
    "visual judgment evidence and expert gates",
    "not proof of visual quality improvement",
    "not public proof",
    "not external validation",
    "Mimesis is the hypothesis",
    "It does not universally improve AI output.",
    "I do not claim Metaforge is production-ready",
    "I do not claim NoiseProof is production-ready",
    "I do not claim Mimesis Engineering is an industry standard",
]


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
