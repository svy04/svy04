# Digital Factory Workbench Evidence Map

Status: local/private evidence map.

This document records how the `Digital Factory` workbench currently informs the public profile README. It is a bridge from local artifacts to public positioning, not a replacement for the public `mimesis-engineering` repository.

## Boundary

The Digital Factory workbench is a private/local research workbench.

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

## Local Artifact Families

These are the local artifact families currently shaping the public position:

| Local artifact family | What it contributes | Public boundary |
| --- | --- | --- |
| `mimesis-source-packet/` | Canonical v.next source packet, definition, pipeline, validation framing, roadmap, and asset triage. | Local canon input only; not public proof by itself. |
| `mimesis-source-packet/00-OVERVIEW.md` | States that the older public v0.1 direction was exploratory and that the source packet is the v.next single source of truth. | Use to avoid treating the old repo as the final method. |
| `mimesis-plugin/` | Prototype plugin shape, expert modules, cases, retina loop, and provenance-oriented validation tools. Latest local reference: `mimesis-plugin@adc3636`, which adds visual judgment evidence and expert gates. | Private/local prototype evidence only; not published adoption proof. |
| `mimesis-plugin/CLAIMS.md` | Current public-claim guardrail for the plugin surface. | Treat as the safety boundary before reusing stronger plugin README language. |
| `mimesis-plugin/README.md` | Public-method draft language around "standards, not roles" and receipt-first positioning. | Some language may overfit prototype claims; keep profile copy narrower. |
| `mimesis-plugin/experts/design-craft/visual_lint.py` | Runnable obvious-slop detector adapted from design-craft priors; flags visual anti-patterns and passes a clean sample. | Slop blocking only; not proof that a design is good. |
| `mimesis-plugin/experts/subjective-quality-evaluator/margin_gated_panel.py` | Runnable margin gate that abstains on cross-family near-ties and ranks only large-margin recorded votes. | Verified on recorded local votes, not a full live judge pipeline or human-validation proof. |
| `mimesis-plugin/cases/004-real-world-visual/HUMAN-VERDICT-003.md` | Owner condition-blind visual judgment: rule-heavy visual module underperformed, example anchors did better, and one retina pass lost to its seed. | n=1 owner signal; not external validation and not proof of visual quality improvement. |
| `MIMESIS-DEPLOYMENT-MAP.md` | Current operating/deployment map for what should be made public next. | Planning surface, not proof that the work is shipped or adopted. |
| `MIMESIS-METHOD.md` | Design-level method extracted from shell failures, load-bearing middle decisions, and non-LLM ship gates. | Thought-method layer, not full method proof. |
| `UNIFYING-LAW.md` | Current self-refined law: conditioning helps where the base output is below the expert region, and can be null or harmful when no headroom exists. | Use as a claim boundary, not as universal law. |
| `FRONTIER-EXP-RESULTS.md` | Local experiment record showing ceiling/null/negative regimes and wrong-anchor downside. | Local experiment record; do not call it external validation. |
| `SOURCES-QUEUE.md` | Source-first queue of products, standards, OSS repos, and evaluation systems to extract from. | Candidate queue only; not all items are implemented modules. |
| `ablation/`, `ablation-r2/`, `replicate/`, `holdout-setB/`, `strongzone/` | Comparison, ablation, replication, holdout, and negative-control style evidence. | Local workbench evidence; publish only after redaction and case shaping. |
| `testbed/` | Rendered website/app specimens and screenshot-style inspection surfaces. | Visual specimen evidence, not customer or production proof. |

## What Counts As Current

Current:

- artifact-level imitation over persona prompting
- source-first extraction from products, papers, standards, open-source repos, patents, and acceptance criteria
- non-LLM checks where possible
- ablations, wrong-anchor controls, holdouts, and failure records
- proof-bound public copy

Outdated or demoted:

- claiming Mimesis universally improves AI output
- treating persona prompting as a serious baseline after it loses to artifact structure
- treating the old public v0 repo as the whole canon
- presenting local workbench records as public proof
- using visual polish without screenshot/pixel/runtime inspection
- treating visual_lint.py or margin_gated_panel.py as visual-quality oracles
- treating `mimesis-source-packet/NEXT-ACTIONS.md` as current install or license state
- reusing `mimesis-plugin/bench/LEADERBOARD.md` before reconciling fabrication-suppression wording with `mimesis-plugin/CLAIMS.md`
- reusing `ACCOUNT-PIPELINE-REPORT.md` as Mimesis Engineering proof; it belongs to a separate account-pipeline lane

## Historical or stale surfaces

These local files should not be lifted into public copy as current proof without a boundary patch:

| File | Current classification |
| --- | --- |
| `mimesis-source-packet/NEXT-ACTIONS.md` | Historical planning state. |
| `mimesis-plugin/bench/LEADERBOARD.md` | Public-adjacent but claim-risky until fabrication-suppression wording is reconciled with `mimesis-plugin/CLAIMS.md`. |
| `ACCOUNT-PIPELINE-REPORT.md` | Separate Instagram/account-pipeline planning lane, not Mimesis Engineering proof. |

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
The Digital Factory workbench is a private/local research workbench rebuilding Mimesis Engineering from experiments, ablations, source scouting, and failure records.
```

The profile README must not say:

```text
Digital Factory proves Mimesis Engineering.
Mimesis Engineering is externally validated.
Mimesis universally improves AI output.
Mimesis suppresses hallucination/fabrication in general.
```

## Next Public Step

The newest useful public artifact is not a bigger claim.

It is the [Mimesis Visual Failure Packet](https://svy04.github.io/proof-artifacts/mimesis-visual-failure-packet-2026-06-15/): a redacted failure packet that turns one Digital Factory visual loop into a public-safe boundary with:

- source set
- weak artifact
- transformed artifact
- ablation or control
- non-LLM check where possible
- failure boundary
- banned claims

For the visual workbench lane, that route may present `HUMAN-VERDICT-003`, `visual_lint.py`, and `margin_gated_panel.py` only as failure-bounded inspection inputs: what failed, what gate now exists, and what remains unproven.

The next stronger public step is not another stronger claim. It is an external blind panel or redacted condition board that keeps owner verdict, external verdict, and banned claims separate.
