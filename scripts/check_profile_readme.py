import argparse
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REQUIRED_LINKS = [
    "https://github.com/svy04/metaforge",
    "https://github.com/svy04/metaforge/blob/main/docs/marketing/metaforge-public-proof-pack-2026-06-18.md",
    "https://github.com/svy04/metaforge/blob/main/docs/product-quality/public-claim-boundary-report.md#public-claim-evidence-map",
    "https://github.com/svy04/noiseproof-agent",
    "https://github.com/svy04/noiseproof-agent/blob/main/docs/review/external-reader-phase-897-current-proof-packet-refresh.md",
    "https://github.com/svy04/mimesis-engineering",
    "https://github.com/svy04/mimesis-canvas",
    "https://github.com/svy04/mimesis-casebook",
    "https://github.com/svy04/svy04",
    "https://github.com/svy04/leaderboard-data",
    "https://github.com/svy04/svy04/actions/workflows/profile-readme.yml",
    "https://svy04.github.io/proof-artifacts/github-profile-readme-proof-surface-2026-06-14/",
    "https://svy04.github.io/proof-artifacts/mimesis-minecraft-high-integration-evidence-card-2026-06-15/",
    "https://svy04.github.io/proof-artifacts/mimesis-minecraft-public-redacted-board-v0-2026-06-15/",
    "https://svy04.github.io/human-made-feeling-bench/",
]

REQUIRED_INTERNAL_LINKS = [
    "docs/profile-proof-surface.md",
    "docs/profile-render-parity-proof-packet.md",
    "docs/private-mimesis-workbench.md",
    "docs/public-github-surface-hygiene-proof-packet.md",
    "docs/public-feedback-hardening.md",
]

REQUIRED_BADGE_URLS = [
    "https://github.com/svy04/svy04/actions/workflows/profile-readme.yml/badge.svg?branch=main",
    "https://img.shields.io/badge/claim%20boundary-documented-555",
]

TRANSIENT_HTTP_STATUSES = {408, 429, 500, 502, 503, 504}

REQUIRED_MARKERS = [
    "I build proof-bounded AI operating systems: evidence before pitch.",
    "검증이 곧 마케팅",
    "Not another wrapper.",
    "Build the proof surface before the pitch",
    "Mimesis Engineering is the front door",
    "artifact-first expert-thinking OS",
    "make expert process visible",
    "cognitive apprenticeship",
    "worked examples",
    "private/local workbench is the current canon input",
    "public Mimesis repos are support surfaces",
    "Metaforge = Meta + MFH + Orchestra OS",
    "Metaforge",
    "Meta for operating memory",
    "MFH for evidence gates",
    "Orchestra for multi-agent routing",
    "Public claim evidence map",
    "allowed claims, explicit non-claims, and unresolved gaps",
    "Metaforge public hardening tracks dependency topology, duplicate-shape ratchets, dead-export triage, public artifact hygiene, provider-id redaction, remote-surface privacy, hosted-trust boundaries, IDE evidence ordering, and public wiring evidence",
    "Metaforge wiring evidence map",
    "runtime import, governance/docs/gates, private/local proof boundary, and manual artifact lane",
    "public wiring evidence",
    "OpenClaude remains the substrate",
    "not the main thesis",
    "Private/local Mimesis Engineering workbench",
    "Public-safe proof routes summarize redacted local hygiene and blockers",
    "Fresh verifier output is required before any stronger module-pass or promotion claim",
    "Mimesis Engineering",
    "AI에게 역할이 아니라 기준을 준다.",
    "give AI standards, not roles",
    "products, papers, patents, standards, and maintained open-source implementations",
    "docs/private-mimesis-workbench.md",
    "source first",
    "artifacts before personas",
    "gates before claims",
    "verification is the marketing",
    "conditional lift, not universal lift",
    "Not a trading bot",
    "not product-complete",
    "not externally validated",
    "private/local",
    "prototype plugin surfaces",
    "expert modules",
    "inspection manifests",
    "redacted local hygiene and blockers",
    "Evidence Card Contract",
    "source artifact",
    "worked example",
    "baseline output",
    "conditioned output",
    "wrong-anchor or checklist control",
    "gate/scorer",
    "failure cases",
    "proof-surface discipline",
    "Public Feedback Hardening",
    "behavioral smoke tests",
    "edge-case checks",
    "side-effect guards",
    "Mimesis Minecraft Public Redacted Board v0",
    "Local Mimesis Research Map",
    "Human-made Feeling Bench",
    "First-pass rubric",
    "Mimesis Minecraft High-Integration Evidence Card",
    "Public redacted board",
    "Public redacted board v0 / incomplete evidence board",
    "Board v1 is not ready",
    "GitHub Profile README Proof Surface",
    "Render parity proof packet",
    "Public GitHub Surface Hygiene Proof Packet",
    "Public GitHub Surface Hygiene Proof Packet",
    "live maintenance-hidden",
    "Source/CI proof and live public rendering stay separate",
    "Public default-branch",
    "scanner-unfriendly placeholders",
    "actual-looking bearer values",
    "raw auth transcript markers",
    "CI-checked routing and claim-boundary surface",
    "statistical significance",
    "hallucination suppression",
    "Public repo map, not adoption proof",
    "Support surface, not current private canon",
    "Public support surface for reference packs, validators, cases, and proof boundaries",
    "Worksheet surface",
    "Case surface",
    "visual quality improvement",
    "externally validated",
    "It does not universally improve AI output.",
    "I do not claim Metaforge is production-ready",
    "I do not claim NoiseProof is production-ready",
    "I do not claim Mimesis Engineering is an industry standard",
    "private workbench evidence is not a public release claim",
]

PROHIBITED_MARKERS = [
    "Current flagship:",
    "## Current Thesis",
    "## Public Repos",
    "Mimesis Engineering is the operating layer I am building now.",
    "Mimesis v.next Workbench",
    "Mimesis Engineering v0",
    "public v0 artifact-level imitation method",
    "board v1 ready",
    "no true wrong-anchor",
    "16/16 expert modules",
    "14/14 expert modules",
    "Current local checks pass",
    "Local checks pass",
    "per-arm build logs remain missing",
    "per-arm build logs are still missing",
    "Metaforge PRs #",
    "PR #70-#77",
    "Private Workbench Verification Snapshot",
    "digital-factory-workbench-verification",
    "PR #63 adds canonical extension hygiene coverage",
]

ALLOWED_GITHUB_REPOS = [
    "metaforge",
    "noiseproof-agent",
    "mimesis-engineering",
    "mimesis-canvas",
    "mimesis-casebook",
    "svy04",
    "leaderboard-data",
]

WINDOWS_USER_PATH_PATTERN = "C:" + r"[\\/]+Users[\\/]+"
POSIX_ADMIN_PATH_PATTERN = "/" + "Users" + "/" + "admin"
KOREAN_PRIVATE_PATH_PATTERN = "\ub0b4 \uc21c\uc218 \uc7ac\ubbf8"
PRIVATE_WORKBENCH_PATH_PATTERN = "Digital" + r"\s+" + "Factory" + r"[\\/]"
PRIVATE_WORKBENCH_NAME_PATTERN = re.compile(
    r"\b" + "Digital" + r"\s+" + "Factory" + r"\b",
    flags=re.IGNORECASE,
)

LOCAL_PATH_PATTERN = re.compile(
    "|".join(
        [
            WINDOWS_USER_PATH_PATTERN,
            POSIX_ADMIN_PATH_PATTERN,
            KOREAN_PRIVATE_PATH_PATTERN,
            PRIVATE_WORKBENCH_PATH_PATTERN,
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
    if "not just" in lowered:
        return False
    safe_phrases = [
        "do not claim",
        "does not prove",
        "does not universally improve",
        "it is not",
        "this is not",
        "not proof",
        "or external validation",
        "or externally validated",
        "not a full transcript",
        "not public proof",
        "not l5 proof",
        "not production readiness, external validation",
        "not production-ready",
        "not product-complete",
        "not externally validated",
        "not external validation",
        "not the main thesis",
        "not an industry standard",
        "board v1 is not ready",
        "not stronger proof",
        "not a live route",
    ]
    return any(phrase in lowered for phrase in safe_phrases)


def find_non_current_repo_links(text):
    repo_pattern = re.compile(
        r"(?:https?://)?github\.com/svy04/([A-Za-z0-9_.-]+)",
        flags=re.IGNORECASE,
    )
    allowed = {repo.lower() for repo in ALLOWED_GITHUB_REPOS}
    findings = []
    for match in repo_pattern.finditer(text):
        repo = match.group(1).rstrip(").,;:")
        if repo.lower() not in allowed:
            findings.append(match.group(0).rstrip(").,;:"))
    return findings


def validate_readme_text(text):
    issues = []

    for marker in REQUIRED_MARKERS:
        if marker not in text:
            issues.append(f"missing required marker: {marker}")

    for marker in PROHIBITED_MARKERS:
        if marker in text:
            issues.append(f"prohibited profile marker: {marker}")

    for link in find_non_current_repo_links(text):
        if link in text:
            issues.append(f"non-public or non-current repo link: {link}")

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
        ("unbounded Mimesis claim", r"\bMimesis(?: Engineering)?\b.*\b(proven|universally improves|industry standard|statistically proven)\b"),
        ("unbounded product-readiness claim", r"\b(is|are) production-ready\b"),
        ("unbounded external-validation claim", r"\b(external validation|externally validated)\b"),
        ("board-v1 readiness claim", r"\bboard\s+v?1\b.*\b(ready|promotion|promotable|complete|completed)\b"),
        ("OpenClaude-as-main claim", r"\bOpenClaude\b.*\b(main thesis|main product|flagship product)\b"),
    ]

    for line in text.splitlines():
        if PRIVATE_WORKBENCH_NAME_PATTERN.search(line):
            issues.append(f"private workbench name disclosure: {line.strip()}")
        if LOCAL_PATH_PATTERN.search(line):
            issues.append(f"local path disclosure: {line.strip()}")
        for label, pattern in dangerous_patterns:
            if re.search(pattern, line, flags=re.IGNORECASE) and not _line_allows_dangerous_claim(line):
                issues.append(f"{label}: {line.strip()}")

    return issues


def check_url(url, timeout=15, retries=2, opener=urlopen, sleeper=time.sleep):
    attempts = retries + 1

    for attempt in range(attempts):
        request = Request(url, headers={"User-Agent": "svy04-profile-readme-check/1.0"})
        try:
            with opener(request, timeout=timeout) as response:
                status = getattr(response, "status", 200)
        except HTTPError as exc:
            status = exc.code
            exc.close()
        except URLError as exc:
            issue = f"{url} -> {exc.reason}"
            if attempt < attempts - 1:
                sleeper(0.5 * (attempt + 1))
                continue
            return issue

        if 200 <= status < 400:
            return None

        issue = f"{url} -> HTTP {status}"
        if status in TRANSIENT_HTTP_STATUSES and attempt < attempts - 1:
            sleeper(0.5 * (attempt + 1))
            continue
        return issue

    return f"{url} -> unknown link check failure"


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
