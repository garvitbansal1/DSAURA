"""
Tests for DSAURA Mastery Engine (Phase 6)
"""

import pytest
from app.intelligence.mastery_engine import (
    MasteryEngine,
    MasteryLevel,
    ProblemRecord,
    PatternRecord,
    MasteryWeights,
)


def test_insufficient_evidence_guard():
    """Verify that fewer than 3 problems returns insufficient_evidence."""
    engine = MasteryEngine()
    patterns = [
        PatternRecord(pattern_slug="p1", topic_slug="arrays", total_patterns_in_topic=5),
        PatternRecord(pattern_slug="p2", topic_slug="arrays", total_patterns_in_topic=5),
    ]
    # Only 2 problems solved
    problems = [
        ProblemRecord(
            problem_id="prob1",
            platform="leetcode",
            difficulty="easy",
            patterns=["p1"],
            topics=["arrays"],
            status="solved",
            solving_mode="independent",
        ),
        ProblemRecord(
            problem_id="prob2",
            platform="leetcode",
            difficulty="easy",
            patterns=["p1"],
            topics=["arrays"],
            status="solved",
            solving_mode="independent",
        ),
    ]

    res = engine.calculate_topic_mastery(
        topic_slug="arrays",
        problems=problems,
        available_patterns=patterns,
    )

    assert res.mastery_level == MasteryLevel.INSUFFICIENT_EVIDENCE
    assert res.has_sufficient_evidence is False
    assert res.mastery_score == 0.0


def test_sufficient_evidence_mastery_calculation():
    """Verify that >= 3 problems produces multi-dimensional score."""
    engine = MasteryEngine()
    patterns = [
        PatternRecord(pattern_slug="two-sum", topic_slug="arrays", total_patterns_in_topic=3),
        PatternRecord(pattern_slug="prefix-sum", topic_slug="arrays", total_patterns_in_topic=3),
        PatternRecord(pattern_slug="sliding-window", topic_slug="arrays", total_patterns_in_topic=3),
    ]

    problems = [
        ProblemRecord(
            problem_id="prob1",
            platform="leetcode",
            difficulty="easy",
            patterns=["two-sum"],
            topics=["arrays"],
            status="solved",
            solving_mode="independent",
        ),
        ProblemRecord(
            problem_id="prob2",
            platform="leetcode",
            difficulty="medium",
            patterns=["prefix-sum"],
            topics=["arrays"],
            status="solved",
            solving_mode="independent",
        ),
        ProblemRecord(
            problem_id="prob3",
            platform="leetcode",
            difficulty="hard",
            patterns=["sliding-window"],
            topics=["arrays"],
            status="solved",
            solving_mode="hints",
        ),
    ]

    res = engine.calculate_topic_mastery(
        topic_slug="arrays",
        problems=problems,
        available_patterns=patterns,
    )

    assert res.has_sufficient_evidence is True
    assert res.mastery_score > 0.0
    assert 0.0 <= res.mastery_score <= 100.0
    assert "pattern_coverage" in res.score_breakdown
    assert "independent_solving" in res.score_breakdown
    assert "difficulty_progression" in res.score_breakdown
