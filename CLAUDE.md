# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Evaluation harness for AI pull request review agents, built on [Inspect AI](https://inspect.aisi.org.uk/). Currently a scaffold: the only task is a hello world. The planned pieces (per the README) are a real PR dataset, a bot review step written as an Inspect solver, and a judge scorer validated against hand labels.

## Commands

Uses `uv`; Python 3.12 is pinned in `.python-version` (package supports >=3.11).

```
uv sync --extra dev              # install, including pytest/ruff/mypy
uv run ruff check .              # lint
uv run ruff format --check .     # format check (drop --check to apply)
uv run mypy                      # strict, covers src and tests
uv run pytest                    # all tests
uv run pytest -m "not network"   # offline tests only
uv run pytest tests/test_scoring.py::test_perfect_review   # single test
```

CI (`.github/workflows/ci.yml`) runs lint, format check, mypy, and the full pytest suite, in that order. All four must pass.

Run the eval and browse results:

```
uv run inspect eval src/pr_review_eval/tasks.py --model mockllm/model
uv run inspect view
```

## Architecture

Two layers, deliberately kept apart:

- `src/pr_review_eval/scoring.py` holds pure functions with no model calls and no Inspect imports. `score_review(matched, produced, expected)` returns a frozen `ReviewScore` (precision, recall, F1). It returns 0.0 rather than raising on zero denominators, and raises `ValueError` on negative counts or `matched` exceeding either total. Keep metric maths here so it stays fast to unit test.
- `src/pr_review_eval/tasks.py` holds Inspect `@task` functions that wire a dataset, solver, and scorer together. The judge scorer, when written, should call into `scoring.py` rather than reimplementing the maths.

`scoring.py` is not yet used by any task; `hello_review` scores with Inspect's built in `includes()`.

## Testing notes

- Tests that need internet are marked `@pytest.mark.network`. The marker is registered in `pyproject.toml`; mark any new test that runs a real `inspect_ai.eval()`.
- End to end tests use `mockllm/model` with `custom_outputs`, so no API key is needed. The first run downloads a tokenizer file, which is why they count as network tests.
- Eval runs write `.eval` logs to `logs/`, which is gitignored.
- mypy runs in strict mode over `tests/` as well, so test functions need `-> None` annotations.
- Ruff line length is 100, with rule sets `E`, `F`, `I`, `UP`, `B`.
