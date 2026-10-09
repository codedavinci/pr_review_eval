"""Pure scoring functions. No model calls, so they are fast to test."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewScore:
    """Precision, recall, and F1 for one review run."""

    precision: float
    recall: float
    f1: float


def score_review(matched: int, produced: int, expected: int) -> ReviewScore:
    """Score a review.

    Args:
        matched: bot comments that match a real finding in the answer key.
        produced: total comments the bot wrote.
        expected: total real findings in the answer key.
    """
    if matched < 0 or produced < 0 or expected < 0:
        raise ValueError("counts must be non negative")
    if matched > produced or matched > expected:
        raise ValueError("matched cannot exceed produced or expected")

    precision = matched / produced if produced else 0.0
    recall = matched / expected if expected else 0.0
    denominator = precision + recall
    f1 = 2 * precision * recall / denominator if denominator else 0.0
    return ReviewScore(precision=precision, recall=recall, f1=f1)
