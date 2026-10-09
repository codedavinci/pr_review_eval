"""Hello world Inspect task. Replace the dataset with real pull requests later."""

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import includes
from inspect_ai.solver import generate


@task
def hello_review() -> Task:
    """A tiny task that proves the Inspect pipeline runs end to end."""
    return Task(
        dataset=[
            Sample(
                input="Reply with the single word: hello",
                target="hello",
            )
        ],
        solver=generate(),
        scorer=includes(),
    )
