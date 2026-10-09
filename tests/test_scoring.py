import pytest

from pr_review_eval.scoring import score_review


def test_perfect_review() -> None:
    result = score_review(matched=4, produced=4, expected=4)
    assert result.precision == 1.0
    assert result.recall == 1.0
    assert result.f1 == 1.0


def test_noisy_bot_has_low_precision() -> None:
    result = score_review(matched=2, produced=10, expected=2)
    assert result.precision == pytest.approx(0.2)
    assert result.recall == 1.0


def test_silent_bot_scores_zero() -> None:
    result = score_review(matched=0, produced=0, expected=5)
    assert result.precision == 0.0
    assert result.recall == 0.0
    assert result.f1 == 0.0


def test_matched_cannot_exceed_produced() -> None:
    with pytest.raises(ValueError):
        score_review(matched=3, produced=2, expected=5)
