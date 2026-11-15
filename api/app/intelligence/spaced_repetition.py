"""
SM-2 Based Spaced Repetition Algorithm for DSAURA Revision System.
"""
from datetime import timedelta, date
from dataclasses import dataclass
from typing import Optional


@dataclass
class SM2Result:
    next_interval_days: int
    new_ease_factor: float
    next_due_date: date


def sm2_update(ease_factor: float, repetition_count: int, quality: int) -> SM2Result:
    """
    SM-2 algorithm update.
    quality: 0-5 (0=complete failure, 3=correct with difficulty, 5=perfect recall)
    """
    MIN_EASE = 1.3

    if quality < 3:
        # Failed — reset interval
        new_interval = 1
        new_repetition = 0
        new_ease = max(
            MIN_EASE,
            ease_factor - 0.8 + 0.28 * quality - 0.02 * quality * quality,
        )
    else:
        new_repetition = repetition_count + 1
        new_ease = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        new_ease = max(MIN_EASE, new_ease)

        if new_repetition == 1:
            new_interval = 1
        elif new_repetition == 2:
            new_interval = 6
        else:
            new_interval = round(repetition_count * ease_factor)

    next_due = date.today() + timedelta(days=new_interval)
    return SM2Result(
        next_interval_days=new_interval,
        new_ease_factor=round(new_ease, 2),
        next_due_date=next_due,
    )


def quality_from_solving_mode(solving_mode: str, is_correct: Optional[bool] = None) -> int:
    """Convert solving mode to SM-2 quality score (0–5)."""
    mapping = {
        "independent": 5,
        "re_solved": 4,
        "hints": 3,
        "editorial": 2,
        "assisted": 1,
        "unknown": 3,
    }
    return mapping.get(solving_mode, 3)


INITIAL_INTERVALS = [1, 3, 7, 14, 30]  # days
