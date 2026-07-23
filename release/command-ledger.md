# Reproduction command ledger

This ledger records the state-changing, evidence-producing, and release-gate
commands used in the campaign. Read-only inspections were also performed
through `git status`, `git diff`, `git branch -a`, `orx projects`, `orx runs`,
`orx exp status`, `orx exp desc`, `orx logs`, `df`, `ps`, and environment-name
enumeration. Secret values and generated run wrappers are intentionally absent.

## Startup and skill audit

```text
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx skill orx-lit
orx skill orx-reports
orx projects --json
orx runs 4cf28579-1f96-497d-8eca-243c601eb070
git rev-parse HEAD
git status --short
git branch -a
df -h .
```

The paper was retrieved with:

```text
curl -L --fail --user-agent "OpenResearch-Reproduction/1.0 (paper audit; contact via repository)" https://ar5iv.labs.arxiv.org/html/2606.11149
curl -L --fail --user-agent "OpenResearch-Reproduction/1.0 (source audit; contact via repository)" https://export.arxiv.org/e-print/2606.11149
```

The arXiv HTML and source archive were hashed with SHA-256. The verdict dataset
`ICML-2026-agent-repro/verdicts` was downloaded at revision
`82955b3a0094cfb99e5ed56ade19eebeb4f19997` and filtered by exact
`space_id == "DineshAI/418BWmKIzX"`. The Space was cloned and checked out at:

```text
git clone https://huggingface.co/spaces/DineshAI/418BWmKIzX /tmp/418BWmKIzX-judged-space
git -C /tmp/418BWmKIzX-judged-space checkout 5f91ea8e5a386773b73437d8be494480363b0293
```

## Environment and fixed command

```text
uv lock
uv sync --frozen
orx project edit 4cf28579-1f96-497d-8eca-243c601eb070 --run-command "uv run --frozen python repro/src/verify_hs.py"
```

Every formal node inherited this exact command:

```text
uv run --frozen python repro/src/verify_hs.py
```

## Experiment tree construction

```text
orx create-experiment 4cf28579-1f96-497d-8eca-243c601eb070 --title "Frozen judged baseline" --run-command "uv run --frozen python repro/src/verify_hs.py"
orx create-experiment 4cf28579-1f96-497d-8eca-243c601eb070 --title "Exact source contracts" --parent 812ae800-db07-4bd8-a38d-f446148334c4
orx create-experiment 4cf28579-1f96-497d-8eca-243c601eb070 --title "Executable pseudocode audit" --parent 5ab38dde
orx create-experiment 4cf28579-1f96-497d-8eca-243c601eb070 --title "Upper-bound proof certificates" --parent cf613988
orx create-experiment 4cf28579-1f96-497d-8eca-243c601eb070 --title "Lower-bound counterexample certificates" --parent cf613988
orx create-experiment 4cf28579-1f96-497d-8eca-243c601eb070 --title "Cumulative exact claim suite" --parent 4af75495
orx create-experiment 4cf28579-1f96-497d-8eca-243c601eb070 --title "Claim 1 regret proof audit" --parent 0f6d045b
orx create-experiment 4cf28579-1f96-497d-8eca-243c601eb070 --title "Claim 4 corrected RCN lower bound" --parent 0f6d045b
orx create-experiment 4cf28579-1f96-497d-8eca-243c601eb070 --title "Final five-claim cumulative suite" --parent 5aa62c18
orx create-experiment 4cf28579-1f96-497d-8eca-243c601eb070 --title "Release candidate artifacts" --parent c29ffb3d-43c4-4074-b94e-685af9eb1d56
```

The abbreviated parent identifiers above are the unambiguous prefixes printed
by the local experiment records. Each node was checked out, edited, committed,
and pushed before launch using the ordinary sequence:

```text
git fetch origin
git checkout <experiment-branch>
git add <scoped-paths>
git commit -m "<experiment description>"
git push -u origin <experiment-branch>
```

The two cumulative branches additionally used ordinary merge commits on their
new child branches; no completed branch was rebased or rewritten.

## Formal launches, waits, and evidence reads

Each experiment below was launched on the local backend:

```text
orx exp run 812ae800-db07-4bd8-a38d-f446148334c4 --backend local
orx exp run 5ab38dde --backend local
orx exp run cf613988 --backend local
orx exp run 4af75495 --backend local
orx exp run 4aec3e3b --backend local
orx exp run 0f6d045b --backend local
orx exp run 5aa62c18 --backend local
orx exp run 601d7a46 --backend local
orx exp run c29ffb3d-43c4-4074-b94e-685af9eb1d56 --backend local
```

The pseudocode audit was relaunched twice after its first two environment-level
failures exposed shallow-clone ancestor lookup. Each launch was monitored with
`orx exp wait <experiment-id> --timeout 480`. Terminal evidence was read with:

```text
orx logs 3333af42-64a4-49f8-b7d5-bb1848805f8e
orx logs e95ffe40-398d-433f-8acc-432d6976fc88
orx logs c0b5c91d-7a4c-4222-bb29-1cfb0d06b36a
orx logs e9165d72-88b1-40c2-8ace-88cef27ac19d
orx logs 01b757b3-ee8e-4fe0-821e-e81fef5115b8
orx logs b9a59e43-f592-4f04-9568-fa4e6d6b8fa2
orx logs d327ad91-6451-4fe3-bcd9-69b45c951821
orx logs f72af367-d592-43c4-9728-a55abb41cfd9
orx logs fd92940d-db50-419d-a9cd-2db19b224988
orx logs ebe095fc-543a-4576-84e0-e72a8d73770e
orx logs c3eea52a-7cef-44df-b491-c80d2084b682
```

Findings were recorded throughout with `orx exp desc <experiment-id> --set
"<findings>"`.

## Reader and release validation

```text
uv run --frozen python reports/reproduction/generate_report_assets.py
uv run --frozen marimo check --fix notebooks/drifting_halfspaces_reproduction.py
uv run --frozen marimo check --strict notebooks/drifting_halfspaces_reproduction.py
git diff --check
jq empty <candidate>/logbook.json
file --brief --mime-type <each-upload-path>
shasum -a 256 <each-upload-path>
comm -23 <judged-path-list> <candidate-path-list>
```

The exact report images were visually inspected after generation. The candidate
Space tree was formed in a temporary directory by applying
`release/hf-space-overlay/` over the exact judged checkout. No Hugging Face
upload command has been run.
