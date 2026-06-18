import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_OWNER = "svy04"
GITHUB_API_ROOT = "https://api.github.com"
MAX_FILE_BYTES = 1_000_000
MAX_EXCERPT_CHARS = 220

SENSITIVE_LOCAL_USER = "".join(("ad", "min"))

SKIPPED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".cache",
}

PATTERN_SPECS = [
    (
        "windows-user-path",
        re.compile("C:" + r"[\\/]+Users[\\/]+" + re.escape(SENSITIVE_LOCAL_USER), re.IGNORECASE),
    ),
    (
        "posix-user-path",
        re.compile("/" + "Users" + "/" + re.escape(SENSITIVE_LOCAL_USER), re.IGNORECASE),
    ),
    ("korean-private-workspace", re.compile("\ub0b4 \uc21c\uc218 \uc7ac\ubbf8")),
    ("non-public-research-path", re.compile("Digital" + r"\s+" + "Factory" + r"[\\/]", re.IGNORECASE)),
    ("non-public-research-name", re.compile(r"\b" + "Digital" + r"\s+" + "Factory" + r"\b", re.IGNORECASE)),
    ("anthropic-placeholder", re.compile("sk-ant-" + "your-key-here", re.IGNORECASE)),
    ("generic-sk-placeholder", re.compile("sk-" + "your-key-here", re.IGNORECASE)),
    ("github-placeholder", re.compile("ghp_" + "your-token-here", re.IGNORECASE)),
    ("master-key-placeholder", re.compile("sk-" + "my-master-key", re.IGNORECASE)),
    ("auth-cache-disclosure", re.compile("Loaded cached " + "credentials", re.IGNORECASE)),
    ("auth-required-disclosure", re.compile("Auth" + "Required", re.IGNORECASE)),
    ("invalid-token-disclosure", re.compile(r"\berror=invalid" + "_token" + r"\b", re.IGNORECASE)),
    (
        "missing-access-token-disclosure",
        re.compile("Missing or invalid " + "access token", re.IGNORECASE),
    ),
    (
        "bearer-token-disclosure",
        re.compile(
            r"Bearer\s+(?!<token>|<redacted>|\[redacted\])[A-Za-z0-9_.=-]{30,}",
            re.IGNORECASE,
        ),
    ),
    (
        "openai-key-assignment",
        re.compile(r"\bOPENAI_API_KEY\s*=\s*" + "sk-" + r"[A-Za-z0-9_\-]*"),
    ),
    (
        "anthropic-key-assignment",
        re.compile(r"\bANTHROPIC_API_KEY\s*=\s*" + "sk-" + r"[A-Za-z0-9_\-]*"),
    ),
    (
        "github-token-assignment",
        re.compile(r"\bGITHUB_TOKEN\s*=\s*" + "ghp_" + r"[A-Za-z0-9_]*"),
    ),
    ("github-pat-token", re.compile("github" + "_pat_" + r"[A-Za-z0-9_]+")),
    ("github-classic-token", re.compile("gh" + r"[pousr]_[A-Za-z0-9_]{20,}")),
    ("generic-openai-style-key", re.compile(r"(?<![\w-])" + "sk-" + r"[A-Za-z0-9]{20,}(?![\w-])")),
    ("google-api-key", re.compile("AIza" + r"[A-Za-z0-9_\-]{20,}")),
]

RAW_RUN_PATH_PATTERN = re.compile(r"(^|/)(bench|cases)/.*/runs/.*\.(md|txt|err)$")
RAW_RUN_MARKER_PATTERN = re.compile(
    r"\b(getAccessToken|refreshAccessToken|UNAUTHENTICATED|Transport channel closed|session id:|tokens used)\b",
    re.IGNORECASE,
)

SECRET_REDACTIONS = [
    (re.compile(r"\bOPENAI_API_KEY\s*=\s*" + "sk-" + r"[A-Za-z0-9_\-]*"), "OPENAI_API_KEY=<redacted>"),
    (re.compile(r"\bANTHROPIC_API_KEY\s*=\s*" + "sk-" + r"[A-Za-z0-9_\-]*"), "ANTHROPIC_API_KEY=<redacted>"),
    (re.compile(r"\bGITHUB_TOKEN\s*=\s*" + "ghp_" + r"[A-Za-z0-9_]*"), "GITHUB_TOKEN=<redacted>"),
    (re.compile("github" + "_pat_" + r"[A-Za-z0-9_]+"), "github_pat_<redacted>"),
    (re.compile("gh" + r"[pousr]_[A-Za-z0-9_]{12,}"), "gh*_ <redacted>"),
    (re.compile("sk-" + r"[A-Za-z0-9][A-Za-z0-9_\-]{4,}"), "sk-<redacted>"),
    (re.compile("AIza" + r"[A-Za-z0-9_\-]{12,}"), "AIza<redacted>"),
    (re.compile(r"Bearer\s+(?!<token>|<redacted>|\[redacted\])[A-Za-z0-9_.=-]{12,}", re.IGNORECASE), "Bearer <redacted>"),
]


@dataclass(frozen=True)
class Finding:
    repo: str
    path: str
    line: int
    label: str
    excerpt: str


@dataclass(frozen=True)
class ScanTarget:
    repo: str
    branch: str
    clone_url: str
    is_default_branch: bool

    @property
    def label(self) -> str:
        if self.is_default_branch:
            return self.repo
        return f"{self.repo}@{self.branch}"


@dataclass(frozen=True)
class ScanSummary:
    repos: int
    refs: int
    files: int
    findings: list[Finding]


def should_skip_path(path: Path) -> bool:
    return any(part in SKIPPED_DIRS for part in path.parts)


def is_probably_text_file(path: Path) -> bool:
    try:
        chunk = path.read_bytes()[:4096]
    except OSError:
        return False
    return b"\x00" not in chunk


def read_text_if_safe(path: Path) -> str | None:
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return None
        if not is_probably_text_file(path):
            return None
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def scan_repo_tree(repo: str, root: Path) -> list[Finding]:
    findings = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or should_skip_path(path.relative_to(root)):
            continue

        text = read_text_if_safe(path)
        if text is None:
            continue

        relpath = path.relative_to(root).as_posix()
        for line_number, line in enumerate(text.splitlines(), start=1):
            if RAW_RUN_PATH_PATTERN.search(relpath) and RAW_RUN_MARKER_PATTERN.search(line):
                findings.append(
                    Finding(
                        repo=repo,
                        path=relpath,
                        line=line_number,
                        label="raw-auth-transcript",
                        excerpt=line.strip()[:MAX_EXCERPT_CHARS],
                    )
                )
            for label, pattern in PATTERN_SPECS:
                if pattern.search(line):
                    findings.append(
                        Finding(
                            repo=repo,
                            path=relpath,
                            line=line_number,
                            label=label,
                            excerpt=line.strip()[:MAX_EXCERPT_CHARS],
                        )
                    )
    return findings


def sanitize_excerpt(excerpt: str) -> str:
    sanitized = excerpt
    for pattern, replacement in SECRET_REDACTIONS:
        sanitized = pattern.sub(replacement, sanitized)
    return sanitized


def format_finding(finding: Finding) -> str:
    excerpt = sanitize_excerpt(finding.excerpt)
    return f"ERROR: {finding.repo}:{finding.path}:{finding.line} [{finding.label}] {excerpt}"


def github_api_get_json(url: str, token: str | None = None, timeout: int = 30):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "svy04-public-surface-hygiene/1.0",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API request failed: HTTP {exc.code} {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"GitHub API request failed: {exc.reason}") from exc


def list_public_repositories(owner: str, token: str | None = None) -> list[dict]:
    repos = []
    page = 1
    while True:
        url = (
            f"{GITHUB_API_ROOT}/users/{owner}/repos"
            f"?type=owner&per_page=100&page={page}&sort=full_name"
        )
        page_repos = github_api_get_json(url, token=token)
        if not page_repos:
            break
        repos.extend(
            repo
            for repo in page_repos
            if not repo.get("archived") and not repo.get("disabled")
        )
        page += 1
    return repos


def list_repository_branches(owner: str, repo_name: str, token: str | None = None) -> list[dict]:
    branches = []
    page = 1
    while True:
        url = (
            f"{GITHUB_API_ROOT}/repos/{owner}/{repo_name}/branches"
            f"?per_page=100&page={page}"
        )
        page_branches = github_api_get_json(url, token=token)
        if not page_branches:
            break
        branches.extend(page_branches)
        page += 1
    return branches


def build_scan_targets(
    owner: str,
    selected_repos: set[str] | None = None,
    token: str | None = None,
    include_non_default_branches: bool = False,
) -> tuple[list[dict], list[ScanTarget]]:
    repos = list_public_repositories(owner, token=token)
    if selected_repos is not None:
        repos = [repo for repo in repos if repo["name"] in selected_repos]

    targets = []
    for repo in repos:
        default_branch = repo["default_branch"]
        branch_names = [default_branch]
        if include_non_default_branches:
            discovered = {
                branch["name"]
                for branch in list_repository_branches(owner, repo["name"], token=token)
                if branch.get("name")
            }
            discovered.add(default_branch)
            branch_names = [default_branch] + sorted(discovered - {default_branch})

        targets.extend(
            ScanTarget(
                repo=repo["name"],
                branch=branch_name,
                clone_url=repo["clone_url"],
                is_default_branch=branch_name == default_branch,
            )
            for branch_name in branch_names
        )

    return repos, targets


def sanitize_ref_for_path(value: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9_.-]+", "__", value).strip("._-")
    return sanitized or "ref"


def clone_scan_target(target: ScanTarget, destination: Path, timeout_seconds: int) -> Path:
    repo_dir = destination / f"{sanitize_ref_for_path(target.repo)}__{sanitize_ref_for_path(target.branch)}"
    command = [
        "git",
        "-c",
        "core.longpaths=true",
        "clone",
        "--quiet",
        "--depth",
        "1",
        "--single-branch",
        "--branch",
        target.branch,
        target.clone_url,
        str(repo_dir),
    ]
    subprocess.run(command, check=True, timeout=timeout_seconds)
    return repo_dir


def scan_public_default_branches(
    owner: str,
    selected_repos: set[str] | None = None,
    token: str | None = None,
    timeout_seconds: int = 120,
    include_non_default_branches: bool = False,
) -> ScanSummary:
    repos, targets = build_scan_targets(
        owner=owner,
        selected_repos=selected_repos,
        token=token,
        include_non_default_branches=include_non_default_branches,
    )

    findings = []
    file_count = 0
    with tempfile.TemporaryDirectory(prefix="public-surface-hygiene-") as tmpdir:
        root = Path(tmpdir)
        for target in targets:
            try:
                repo_root = clone_scan_target(target, root, timeout_seconds=timeout_seconds)
            except subprocess.CalledProcessError as exc:
                if not target.is_default_branch:
                    print(
                        f"WARN: skipped unavailable public branch head {target.label}: {exc}",
                        file=sys.stderr,
                    )
                    continue
                raise
            repo_findings = scan_repo_tree(target.label, repo_root)
            findings.extend(repo_findings)
            file_count += sum(
                1
                for path in repo_root.rglob("*")
                if path.is_file() and not should_skip_path(path.relative_to(repo_root))
            )
    return ScanSummary(repos=len(repos), refs=len(targets), files=file_count, findings=findings)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Scan public GitHub branch heads for local path leaks and secret-shaped placeholders."
    )
    parser.add_argument("--owner", default=DEFAULT_OWNER)
    parser.add_argument(
        "--repo",
        action="append",
        dest="repos",
        help="Restrict scan to a public repository name. May be repeated.",
    )
    parser.add_argument(
        "--clone-timeout-seconds",
        type=int,
        default=120,
        help="Timeout for each shallow clone.",
    )
    parser.add_argument(
        "--include-non-default-branches",
        action="store_true",
        help="Also scan public non-default branch heads, not only default branches.",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    selected_repos = set(args.repos) if args.repos else None
    token = os.environ.get("GITHUB_TOKEN")

    try:
        summary = scan_public_default_branches(
            owner=args.owner,
            selected_repos=selected_repos,
            token=token,
            timeout_seconds=args.clone_timeout_seconds,
            include_non_default_branches=args.include_non_default_branches,
        )
    except (RuntimeError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print(f"ERROR: public GitHub surface hygiene scan failed: {exc}", file=sys.stderr)
        return 2

    if summary.findings:
        for finding in summary.findings:
            print(format_finding(finding), file=sys.stderr)
        return 1

    print(
        "Public GitHub surface hygiene checks passed. "
        f"scanned_repos={summary.repos} scanned_refs={summary.refs} scanned_files={summary.files}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
