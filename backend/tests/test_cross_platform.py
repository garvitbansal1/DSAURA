"""
Tests for Cross-Platform Intelligence & Deduplication (Phase 15)
"""

import pytest
from app.intelligence.cross_platform import CrossPlatformEngine, normalize_title


def test_normalize_title():
    assert normalize_title("Two Sum") == "two-sum"
    assert normalize_title("3Sum - Triplet") == "3sum-triplet"
    assert normalize_title("Trapping Rain Water!!") == "trapping-rain-water"


def test_cross_platform_deduplication():
    engine = CrossPlatformEngine()
    problems = [
        {"name": "Two Sum", "platform": "leetcode", "slug": "two-sum"},
        {"name": "Key Pair (Two Sum)", "platform": "geeksforgeeks", "slug": "key-pair"},
        {"name": "Valid Parentheses", "platform": "leetcode", "slug": "valid-parentheses"},
        {"name": "Parenthesis Checker", "platform": "geeksforgeeks", "slug": "parenthesis-checker"},
        {"name": "Daily Temperatures", "platform": "leetcode", "slug": "daily-temperatures"},
    ]

    unique, duplicates = engine.deduplicate_problems(problems)

    # "two-sum" and "key-pair" are aliases -> 1 duplicate
    # "valid-parentheses" and "parenthesis-checker" are aliases -> 1 duplicate
    assert duplicates == 2
    assert len(unique) == 3


def test_cross_platform_synergy():
    engine = CrossPlatformEngine()
    profiles = [
        {"platform": "leetcode", "username": "neal_wu", "solved": 250},
        {"platform": "codeforces", "username": "tourist", "solved": 180},
    ]

    synergy = engine.calculate_cross_platform_synergy(profiles)
    assert "leetcode" in synergy["connected_platforms"]
    assert "codeforces" in synergy["connected_platforms"]
    assert len(synergy["synergy_insights"]) > 0
