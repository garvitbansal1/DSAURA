"""
DSAURA Cross-Platform Intelligence & Deduplication Engine
Phase 15 Implementation

Handles canonical problem mapping across LeetCode, Codeforces, GeeksforGeeks, and HackerRank.
Avoids inflating problem counts by detecting duplicates across platforms.
"""

from typing import List, Dict, Any, Set, Tuple
import re

# Curated canonical problem aliases across platforms
CANONICAL_PROBLEM_ALIASES: Dict[str, List[str]] = {
    "two-sum": ["two-sum", "key-pair", "pair-with-given-sum", "2sum"],
    "three-sum": ["3sum", "triplet-sum-in-array", "three-sum"],
    "trapping-rain-water": ["trapping-rain-water", "trapping-rain-water-problem"],
    "longest-substring-without-repeating-characters": [
        "longest-substring-without-repeating-characters",
        "length-of-the-longest-substring"
    ],
    "valid-parentheses": ["valid-parentheses", "parenthesis-checker", "balanced-brackets"],
    "merge-k-sorted-lists": ["merge-k-sorted-lists", "merge-k-sorted-linked-lists"],
    "climbing-stairs": ["climbing-stairs", "count-ways-to-reach-the-nth-stair"],
    "coin-change": ["coin-change", "coin-change-problem", "minimum-coins"],
    "course-schedule": ["course-schedule", "prerequisite-tasks", "course-schedule-i"],
    "word-break": ["word-break", "word-break-part-2"],
}


def normalize_title(title: str) -> str:
    """Normalize problem title for fuzzy matching."""
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())
    return '-'.join(cleaned.split())


class CrossPlatformEngine:
    """
    Consolidates problem records from multiple platforms,
    deduplicates identical problems, and analyzes cross-platform synergy.
    """

    def deduplicate_problems(
        self,
        platform_problems: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Deduplicates problem submissions from multiple platforms.
        Returns (unique_problems, duplicate_count).
        """
        seen_canonical: Set[str] = set()
        unique: List[Dict[str, Any]] = []
        duplicates = 0

        for prob in platform_problems:
            raw_title = prob.get("title") or prob.get("name") or ""
            raw_slug = prob.get("slug") or prob.get("platform_id") or normalize_title(raw_title)

            # Match against known canonical aliases
            canonical = None
            for key, aliases in CANONICAL_PROBLEM_ALIASES.items():
                if raw_slug in aliases or any(alias in raw_slug for alias in aliases):
                    canonical = key
                    break

            if not canonical:
                canonical = normalize_title(raw_title)

            if canonical in seen_canonical:
                duplicates += 1
            else:
                seen_canonical.add(canonical)
                unique.append({
                    **prob,
                    "canonical_id": canonical,
                    "is_canonical": True,
                })

        return unique, duplicates

    def calculate_cross_platform_synergy(
        self,
        profiles_stats: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyzes the strengths of each platform in the user's journey.
        e.g., Codeforces boosts Speed & Greedy; LeetCode boosts Core Data Structures.
        """
        synergies = []
        platforms_connected = [p.get("platform") for p in profiles_stats]

        if "leetcode" in platforms_connected and "codeforces" in platforms_connected:
            synergies.append({
                "synergy_title": "Interview & Competitive Equilibrium",
                "description": "Combining LeetCode's structured pattern bank with Codeforces' contest problem-solving under time pressure gives optimal algorithmic speed."
            })
        elif "leetcode" in platforms_connected:
            synergies.append({
                "synergy_title": "Pattern Foundation Established",
                "description": "Solid pattern grounding on LeetCode. Recommend adding Codeforces contests to build speed and edge-case resilience."
            })

        return {
            "connected_platforms": platforms_connected,
            "synergies": synergies,
            "synergy_insights": synergies,
            "topic_strengths": {
                "leetcode": ["Dynamic Programming", "Trees", "Stacks", "Two Pointers"],
                "codeforces": ["Greedy", "Number Theory", "Binary Search", "Constructive Algorithms"],
                "geeksforgeeks": ["Arrays", "Linked Lists", "Standard Traversal Patterns"],
            }
        }
