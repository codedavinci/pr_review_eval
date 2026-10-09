import pytest
from inspect_ai import eval
from inspect_ai.model import ModelOutput, get_model

from pr_review_eval.tasks import hello_review


def test_task_definition_is_valid() -> None:
    task = hello_review()
    assert len(task.dataset) == 1
    assert task.scorer is not None


@pytest.mark.network
def test_hello_review_runs_with_mock_model() -> None:
    """Runs the full pipeline. Needs internet once, to fetch a tokenizer file."""
    model = get_model(
        "mockllm/model",
        custom_outputs=[ModelOutput.from_content(model="mockllm/model", content="hello")],
    )
    logs = eval(hello_review(), model=model, display="none", log_dir="logs")
    assert logs[0].status == "success"
    assert logs[0].results is not None
    scores = logs[0].results.scores
    assert scores[0].metrics["accuracy"].value == 1.0
