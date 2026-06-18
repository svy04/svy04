# Private Mimesis Workbench Evidence Map

Status: local/private evidence map.

This document records how the private/local Mimesis research workbench currently informs the public profile README. It is a bridge from local artifacts to public positioning, not a replacement for the public `mimesis-engineering` repository.

## Boundary

The private Mimesis workbench is a private/local research workbench.

It is not public proof.

It is not external validation.

It is not an adoption claim.

It is not evidence that Mimesis Engineering is an industry standard, statistically proven, or universally effective.

Public copy should use it only for bounded claims about current research direction, artifact families, and proof discipline.

## Current Reading

The old public-facing story was too broad:

```text
Mimesis improves AI output.
```

The current evidence-bounded story is narrower:

```text
Mimesis can help in high-slop, underdetermined generative work when it imports
load-bearing structure from verified artifacts.

It does not universally improve AI output.
It can show ceiling, null, or negative effects when the task is already well specified.
```

That is the claim the profile README is allowed to carry.

The current private canon adds one product-shaping constraint:

```text
The useful product is not "Mimesis always wins."

The useful product is a workflow that can decide when artifact conditioning
should be on, when it should be off, which non-LLM or human gate is needed,
and which claim boundary must remain attached.
```

The public profile may describe that operating law. It must not expose private
workbench paths, private branch names, raw transcript snippets, or local-only
module counts as proof.

## Current local snapshot

Snapshot checked on 2026-06-18 KST from the private/local Mimesis workbench:

```text
verify_workbench_surface.py -> passed
verify_leaderboard_claims.py -> passed
verify_readme_claims.py -> passed
verify_claims.py -> passed
verify_evidence_references.py -> passed
verify_public_hygiene.py -> passed
tools/validate_module.py --all -> passed
verify_minecraft_board_v1_gate.py -> passed by confirming a draft skeleton exists and board v1 is not ready
```

This is local-only evidence. It can guide the public profile's direction, but
the profile should not turn the private module count, dirty worktree state, or
local board receipts into a public numeric proof claim until the public proof
route exposes the same evidence with redaction and route checks.

The private plugin checkout inspected for this snapshot was not a public release
artifact. That state is a boundary: the local verifier pass is useful for
direction, but it is not publishable proof, not a public repo state claim, and
not evidence that an npm `verify:all` script is available locally.

## Local Artifact Families

These are the local artifact families currently shaping the public position:

| Local artifact family | What it contributes | Public boundary |
| --- | --- | --- |
| Private source packet | Definition, pipeline, validation framing, roadmap, and asset triage. | Local canon input only; not public proof by itself. |
| Private prototype surface | Plugin shape, expert modules, cases, behavioral gates, visual loops, and provenance-oriented validation tools. | Private/local prototype evidence only; not published adoption proof. |
| Claim guardrail notes | Public-claim guardrails for stronger method language. | Treat as a safety boundary before reusing stronger local copy. |
| Visual failure records | Owner condition-blind visual judgment, obvious-slop checks, and margin-gated comparison notes. | Local failure evidence only; not external validation and not proof of visual quality improvement. |
| Operating map | When artifact conditioning should be on, when it should be off, and which gate or boundary is required. | Planning surface, not proof that the work is shipped or adopted. |
| Method notes | Design-level method extracted from shell failures, load-bearing middle decisions, and non-LLM ship gates. | Thought-method layer, not full method proof. |
| Experiment records | Ceiling/null/negative regimes, competence prechecks, wrong-anchor downside, comparison, replication, holdout, and negative-control evidence. | Local workbench evidence; publish only after redaction and case shaping. |
| External OSS attribution repro cards | Source-level executable attribution for `P-EXT-03` Go `time.Parse` and `P-EXT-06` Eisel-Lemire / float parsing, including source anchor, objective oracle, defect control, wrong-anchor control, and command result. | Redacted summary only; not downstream lift, not maintainer endorsement, not legal clearance, not production readiness, and not external validation. |
| High-integration evidence cards | Source artifact, baseline output, conditioned output, checklist control, gate/scorer, small local blind judging, failure cases, and claim boundary. | Redacted summary only; not L5 proof, external validation, human visual-quality proof, near-Fable proof, public benchmark status, legal clearance, or universal lift. |
| Board readiness gates | Board v1 collection plan, required evidence atoms, stop conditions, `verify_minecraft_board_v1_gate.py` promotion guard, `manifest-preflight.json`, `MANIFEST-CONTRACT.md`, `manifest.schema.json`, `manifest-promotion-blockers.json`, manifest contract/schema, `board-v1-inspection-manifest.json` inspection-only index, aggregate transcript ledger, `scorer-transcript-availability.json`, `raw-transcript-preflight.json`, `raw-transcript-redaction-review-preflight.json`, `public-source-packet-draft.md/.json` future-route source packet draft, local per-arm build/render logs, and a local wrong-anchor execution/render sidecar receipt. | Blocker contract only; board v1 is not ready. `READY.json`, `redacted-screenshots/manifest.json`, full public-safe manifest, public-safe screenshot manifest, route-linked board-v1 entries, comparable wrong-anchor score, raw per-judge score rows, raw comments, redaction-reviewed raw rows, full per-judge scorer transcript, and a live route are still missing, so this does not add external validation or stronger proof. |
| Source queue | Products, standards, OSS repos, patents, papers, and evaluation systems to extract from. | Candidate queue only; not all items are implemented modules. |
| Visual specimens | Rendered website/app specimens and screenshot-style inspection surfaces. | Visual specimen evidence, not customer or production proof. |

The source queue is intentionally broad: products, standards, OSS repos, patents, and evaluation systems are allowed inputs only after they are reduced into bounded source packets.

## What Counts As Current

Current:

- artifact-level imitation over persona prompting
- source-first extraction from products, papers, standards, open-source repos, patents, and acceptance criteria
- non-LLM checks where possible, especially behavioral gates over form-counting gates
- ablations, wrong-anchor controls, holdouts, and failure records
- competence prechecks that measure the naked baseline before deciding whether to inject artifact structure
- proof-bound public copy

Outdated or demoted:

- claiming Mimesis universally improves AI output
- treating persona prompting as a serious baseline after it loses to artifact structure
- treating the old public v0 repo as the whole canon
- presenting local workbench records as public proof
- using visual polish without screenshot/pixel/runtime inspection
- treating local visual lint or margin-gated comparison scripts as visual-quality oracles
- treating stale local planning notes as current install or license state
- reusing local leaderboard-style notes before reconciling their claim wording
- reusing unrelated account-pipeline notes as Mimesis Engineering proof

## Historical or stale surfaces

These local files should not be lifted into public copy as current proof without a boundary patch:

| Surface | Current classification |
| --- | --- |
| Stale planning notes | Historical planning state. |
| Local leaderboard-style notes | Public-adjacent but claim-risky until wording is reconciled with current claim guardrails. |
| Separate account-pipeline notes | Adjacent operations planning lane, not Mimesis Engineering proof. |

## External Source Anchors

These outside references inform the public-surface discipline for this snapshot:

- GitHub profile README docs: a profile README is a public identity and project showcase surface.
- GitHub Actions workflow status badge docs: badges can show workflow status, but they are not proof of product outcomes.
- SLSA provenance: strong artifacts should preserve where, when, and how they were produced.
- OpenAI Evals and simple-evals, plus EleutherAI `lm-evaluation-harness`: evaluation systems should define repeatable task, metric, and record surfaces instead of relying on vibes.
- Prompt-engineering patent filings: prompt systems can be industrial artifacts, but a filing is not evidence that a method works for this project.

## Profile README Rule

The profile README may say:

```text
The private Mimesis workbench is a private/local research workbench rebuilding
Mimesis Engineering from experiments, ablations, source scouting, behavioral
gates, competence prechecks, and failure records.
```

The profile README must not say:

```text
The private workbench proves Mimesis Engineering.
Mimesis Engineering is externally validated.
Mimesis universally improves AI output.
Mimesis suppresses hallucination/fabrication in general.
```

## Current Public Steps

The useful public artifacts are not bigger claims.

The [Mimesis Visual Failure Packet](https://svy04.github.io/proof-artifacts/mimesis-visual-failure-packet-2026-06-15/) turns one private visual workbench loop into a public-safe boundary with:

- source set
- weak artifact
- transformed artifact
- ablation or control
- non-LLM check where possible
- failure boundary
- banned claims

For the visual workbench lane, that route may present redacted verdict, lint, and margin-gate evidence only as failure-bounded inspection inputs: what failed, what gate now exists, and what remains unproven.

The [Mimesis Minecraft High-Integration Evidence Card](https://svy04.github.io/proof-artifacts/mimesis-minecraft-high-integration-evidence-card-2026-06-15/) turns one private/local high-integration case into a public-safe redacted local evidence card with:

- source artifact
- baseline output
- conditioned output
- checklist control
- gate/scorer
- blind 3-judge panel
- n=2 per cell
- failure cases
- claim boundary
- local wrong-anchor execution/render sidecar
- not route-linked board-v1 proof

That route is not L5 proof, external validation, human visual-quality proof, near-Fable proof, public benchmark status, legal clearance, or universal lift.

The [External OSS Attribution: Two Executed Repro Cards](https://svy04.github.io/proof-artifacts/mimesis-external-oss-attribution-two-repro-cards-2026-06-15/) turns two source-level Mimesis attribution records into a public-safe executable attribution packet:

- `P-EXT-03` Go `time.Parse` timezone range guard
- `P-EXT-06` Eisel-Lemire / nearest-even float parsing guard
- source anchor
- objective oracle
- defect control
- wrong-anchor control
- command result
- forbidden claims

That route is source-level executable attribution. It is not downstream lift,
not maintainer endorsement, not legal clearance, not production readiness, and
not external validation.

The [Mimesis Minecraft Public Redacted Board v0](https://svy04.github.io/proof-artifacts/mimesis-minecraft-public-redacted-board-v0-2026-06-15/) is now public as a public redacted board v0 / incomplete evidence board. It keeps source-use boundary, condition board, aggregate scoring, failure record, and claim boundary separate. It can now say that public-safe screenshot sidecars exist without `redacted-screenshots/manifest.json`, `manifest-preflight.json` exists, `MANIFEST-CONTRACT.md` and `manifest.schema.json` define a manifest contract/schema, `board-v1-inspection-manifest.json` exists as an inspection-only blocker index, an aggregate transcript ledger exists, local per-arm build/render logs exist as inventory only, and the local wrong-anchor execution/render sidecar exists as a receipt only.

It remains promotion-blocked because the local wrong-anchor execution/render sidecar, inspection-only manifest, and local per-arm build/render logs are not route-linked board-v1 proof, and because `READY.json`, `redacted-screenshots/manifest.json`, full public-safe manifest, public-safe screenshot manifest, route-linked board gate / route-linked board-v1 entries, comparable wrong-anchor score, full scorer transcript, full per-judge scorer transcript, fuller judge protocol, and public-safe per-arm screenshots or links are still missing.

The latest private plugin gates add a board v1 collection plan, `verify_minecraft_board_v1_gate.py`, one local wrong-anchor execution/render sidecar, local per-arm build/render logs, `MANIFEST-CONTRACT.md`, `manifest.schema.json`, `manifest-promotion-blockers.json`, `board-v1-inspection-manifest.json`, `raw-transcript-preflight.json`, `raw-transcript-redaction-review-preflight.json`, and `public-source-packet-draft.md/.json` as a future-route source packet draft. This is a blocker contract, not stronger proof; the sidecar, manifest contract/schema, promotion blocker record, inspection manifest, raw transcript preflight, redaction-review preflight, and source packet draft are only receipts/contracts/indexes. It is not a live route, not `READY.json`, not `redacted-screenshots/manifest.json`, not a public-safe screenshot manifest, and not full transcript/scorer evidence. It lists evidence atoms, required route-linked wrong-anchor scoring evidence, scoring transcript fields, raw transcript row fields, public-safe artifact requirements, redaction checks, and stop conditions before any board v1 claim can be made. Board v1 is not ready.

The [Mimesis Minecraft Transcript Availability Audit](https://svy04.github.io/proof-artifacts/mimesis-minecraft-transcript-availability-audit-2026-06-15/) is the public-safe route for the latest transcript gap. It can say that `scorer-transcript-availability.json`, `board-v1-inspection-manifest.json`, `manifest-promotion-blockers.json`, `raw-transcript-preflight.json`, `raw-transcript-redaction-review-preflight.json`, sanitized raw-run receipts, and the README proof-gate surface make missing evidence explicit after PR #25-#33 blocker and hygiene gates. It must not say the board is ready, externally validated, stronger, or backed by a full transcript. Raw per-judge score rows, raw comments, redaction-reviewed raw rows, route-linked board-v1 entries, and independent/external panel evidence remain missing.
