# Public Feedback Hardening

Status: active remediation track.

This note records what public feedback changed about the profile and adjacent
Metaforge/Mimesis surfaces. The response is not to make stronger claims. The
response is to make the public surface easier to trust.

## What Changed

- OpenClaude stays the local runtime substrate. Metaforge remains the public
  `Meta + MFH + Orchestra OS` thesis.
- Fork/origin/license boundaries must stay visible before any stronger install
  or release-facing language.
- Korean documentation is first-class because the first feedback loop is
  Korean.
- Public docs must not expose local machine context, private workspace names,
  raw run logs, OAuth/auth metadata, secret-shaped placeholders, or internal
  rule dumps.
- Marker and string checks are routing gates only. Stronger promotion needs
  behavioral smoke tests, edge-case checks, and side-effect guards.
- Duplicate helper clusters, dead exports, circular dependencies, raw artifact
  leaks, and provider trace identifiers belong in cleanup and guardrail lanes,
  not in the launch claim; dependency topology, duplicate-shape ratchets,
  dead-export triage, public artifact hygiene, provider-id redaction,
  remote-surface privacy, hosted-trust boundaries, IDE evidence ordering, and
  public wiring evidence are ratchets, not cleanup-complete claims.
- Recent Metaforge public hardening added remote-surface helper reuse, IDE
  evidence ordering, real VS Code host/workbench success classification,
  claim-blocked protected-action packet handling, hosted-trust check mode,
  AVF/VS Code hygiene tightening, self-contained blocked-claim findings,
  dependency-topology refresh, workspace-path hygiene, and remote-surface
  privacy pattern hardening, plus a public claim evidence map for Meta, MFH,
  Orchestra, OpenClaude runtime, Mimesis Engineering, and AVF Influence Factory;
  this is privacy and claim-surface hardening, not release readiness.

## Tooling Backlog

Use static-analysis tools as evidence routers, then review their findings
before changing code:

| Risk | Candidate tools | Public claim boundary |
| --- | --- | --- |
| Dead exports and unused files | Knip or Fallow | Candidate list only; false positives must be reviewed. |
| Circular dependencies | dependency-cruiser | Architecture signal, not runtime proof. |
| Duplicate script shape | jscpd or Lumin-style topology review | Refactor queue, not proof of behavior. |
| Secret or local-context leakage | GitHub secret scanning, push protection, local hygiene scans | Hygiene signal, not a full security audit. |

## Next Gate Upgrade

The next useful upgrade is not another badge. It is a small set of tests that
prove the public claims carry behavior:

```text
happy path -> edge case -> side-effect guard -> claim boundary
```

Until those tests exist for a claim, the profile should keep that claim in
planning, local, private, or candidate language.
