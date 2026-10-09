# pr_review_eval

Evaluating AI pull request review agents with Inspect AI.

Status: scaffold. The task is a hello world. The real dataset, bot step, and judge scorer come next.

## What this repo will answer

(Write your one sentence decision question here. Example: how often does a model judge mislabel a correct review comment, and in which direction?)

## Setup

Requires Python 3.11 or newer and uv.

```
uv sync --extra dev
```

## Run the checks

```
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

Run the offline tests only:

```
uv run pytest -m "not network"
```

One test runs the full Inspect pipeline with the built in mock model, so no API key is needed. It downloads a tokenizer file once, so it needs internet.

## Run the hello world eval

```
uv run inspect eval src/pr_review_eval/tasks.py --model mockllm/model
uv run inspect view
```

## Layout

| Path | Purpose |
| --- | --- |
| `src/pr_review_eval/scoring.py` | Pure precision, recall, and F1 functions |
| `src/pr_review_eval/tasks.py` | Inspect tasks |
| `tests/` | pytest tests |
| `.github/workflows/ci.yml` | Lint, format, types, and tests on every push |

## Next steps

1. Choose your original angle and write the decision question above.
2. Load a public pull request dataset and verify its license.
3. Write the bot review step as an Inspect solver.
4. Write the judge scorer and hand label a sample.
5. Add a results table, cost per run, and a threat model to this README.
