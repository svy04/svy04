# Public GitHub Surface Hygiene Proof Packet

Status: executable public-surface hygiene gate.

This packet records a narrow check over the public GitHub surface for `@svy04`.
It exists because the profile is now a marketing and proof-routing surface: the
public repos it links should not leak local workstation paths or carry
scanner-unfriendly secret-shaped placeholders.

## What The Gate Runs

```text
python scripts/check_public_github_surface_hygiene.py
```

The script:

- lists public repositories owned by `@svy04` with the GitHub REST API
- skips archived and disabled repositories
- shallow-clones each public default branch into a temporary directory
- scans text files under the public default branches
- ignores Git metadata, dependency folders, build folders, binary-looking files, and files over the local size cap
- reports findings with repository, path, line, rule label, and a redacted excerpt

## Rule Set

The local rule set checks for:

- Windows admin-user path fragments
- macOS/Linux admin-path fragments
- the Korean private-workspace phrase
- Digital Factory path fragments when they look like filesystem paths
- scanner-unfriendly example credentials and token-shaped placeholders
- OpenAI/Anthropic/GitHub-style assignment lines with secret-shaped values
- generic token-shaped values that look like GitHub, OpenAI-style, or Google API keys

Findings are review indicators. They are not automatic proof of a live
credential, exploitability, compromise, or malicious exposure.

## Source Anchors

The packet borrows its structure from primary/public sources:

- GitHub REST repositories docs: public repository listing, pagination, and API versioning shape.
  Source: https://docs.github.com/en/rest/repos/repos
- GitHub secret scanning docs: secret alerts, remediation, validity checks, public repository scanning, and the boundary between this local scan and platform secret scanning.
  Source: https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning
- Gitleaks: rule-based secret detection, redaction, and scan-output posture.
  Source: https://github.com/gitleaks/gitleaks
- OWASP Full Path Disclosure: local path disclosure as information-leakage evidence, not automatic exploitability proof.
  Source: https://owasp.org/www-community/attacks/Full_Path_Disclosure
- SLSA specification: provenance and source-verification vocabulary for bounded claims.
  Source: https://slsa.dev/spec/v1.2/
- OpenSSF Scorecard: repository hygiene as a posture signal, not a security certificate.
  Source: https://github.com/ossf/scorecard

## Bounded Claim

This packet can support this claim:

```text
The recorded public `@svy04` default branches were scanned by the attached
local rule set for local-path disclosure and scanner-unfriendly placeholders.
The scan produced static review indicators for the checked surface.
```

## Explicit Non-Claims

This packet does not prove:

- public repositories contain no secrets
- historical Git refs are clean
- private repositories are clean
- open pull requests, forks, issues, discussions, gists, releases, packages, or wikis are clean
- GitHub secret-scanning alerts are absent or resolved
- detected token-shaped text is a live credential
- the repositories are secure, compliant, production-ready, SLSA-ready, or externally validated

## Remediation Rule

If the gate finds a local path, replace it with a repository-relative path, a
public URL, or a neutral placeholder.

If the gate finds a scanner-unfriendly example credential, replace it with a
non-secret placeholder such as:

```text
OPENAI_API_KEY=<openai-api-key>
GITHUB_TOKEN=<github-token>
```

If the gate finds a real credential, revoke or rotate it before rewriting public
history. Removing the string from the repo is not enough once a credential may
have been exposed.
