"""
Tests for SuperMemo SM-2 Spaced Repetition Algorithm (Phase 13)
"""

import pytest
from datetime import date, timedelta
from app.intelligence.spaced_repetition import sm2_update, quality_from_solving_mode


def test_sm2_failure_resets_interval():
    """Quality < 3 resets interval to 1 day and repetition count to 0."""
    res = sm2_update(ease_factor=2.5, repetition_count=3, quality=1)
    assert res.next_interval_days == 1
    assert res.next_due_date == date.today() + timedelta(days=1)


def test_sm2_first_successful_review():
    """First successful review sets interval to 1 day and increments reps."""
    res = sm2_update(ease_factor=2.5, repetition_count=0, quality=4)
    assert res.next_interval_days == 1


def test_sm2_second_successful_review():
    """Second successful review sets interval to 6 days."""
    res = sm2_update(ease_factor=2.5, repetition_count=1, quality=4)
    assert res.next_interval_days == 6


def test_sm2_subsequent_review():
    """Third review multiplies interval by ease factor."""
    res = sm2_update(ease_factor=2.5, repetition_count=2, quality=5)
    assert res.next_interval_days >= 5
    assert res.new_ease_factor >= 2.5


def test_sm2_minimum_ease_factor():
    """Ease factor should never drop below 1.3."""
    res = sm2_update(ease_factor=1.3, repetition_count=0, quality=0)
    assert res.new_ease_factor >= 1.3


def test_quality_from_solving_mode():
    assert quality_from_solving_mode("independent") == 5
    assert quality_from_solving_mode("editorial") == 2
    assert quality_from_solving_mode("hints") == 3
