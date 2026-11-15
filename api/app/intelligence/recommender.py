"""
DSAURA Personalized Problem Recommendation Engine

Recommends problems based on:
- Topic mastery gaps
- Pattern coverage gaps
- Prerequisite completion
- Difficulty progression
- Learning goal
"""

from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from .mastery_engine import MasteryLevel, TopicMasteryResult


@dataclass
class ProblemRecommendation:
    problem_id: str
    platform: str
    name: str
    url: str
    difficulty: str
    topics: List[str]
    patterns: List[str]
    reason: str
    expected_outcome: str
    priority: int  # 1-10, higher = more urgent


class RecommendationEngine:
    """
    Generates prioritized problem recommendations.

    Learning Progression:
    Foundation → Pattern Recognition → Pattern Practice →
    Pattern Variations → Mixed Problems → Advanced Applications
    """

    def generate_recommendations(
        self,
        user_mastery: Dict[str, TopicMasteryResult],
        solved_problem_ids: Set[str],
        all_problems: List[Dict],
        learning_goal: Optional[str] = None,
        max_recommendations: int = 10,
    ) -> List[ProblemRecommendation]:

        recommendations: List[ProblemRecommendation] = []

        # Priority 1: Topics with insufficient evidence — get started
        for topic, mastery in user_mastery.items():
            if not mastery.minimum_evidence_met:
                recs = self._recommend_foundation(topic, solved_problem_ids, all_problems)
                recommendations.extend(recs[:2])

        # Priority 2: Weak topics — improve pattern coverage
        for topic, mastery in user_mastery.items():
            if mastery.minimum_evidence_met and mastery.mastery_level in [
                MasteryLevel.BEGINNER,
                MasteryLevel.DEVELOPING,
            ]:
                recs = self._recommend_for_weak_topic(
                    topic, mastery, solved_problem_ids, all_problems
                )
                recommendations.extend(recs[:3])

        # Priority 3: Intermediate topics — push to advanced
        for topic, mastery in user_mastery.items():
            if mastery.mastery_level == MasteryLevel.INTERMEDIATE:
                recs = self._recommend_difficulty_push(topic, solved_problem_ids, all_problems)
                recommendations.extend(recs[:2])

        # Deduplicate by problem_id, sort by priority
        seen: Set[str] = set()
        unique_recs: List[ProblemRecommendation] = []
        for rec in sorted(recommendations, key=lambda r: -r.priority):
            if rec.problem_id not in seen and rec.problem_id not in solved_problem_ids:
                seen.add(rec.problem_id)
                unique_recs.append(rec)
                if len(unique_recs) >= max_recommendations:
                    break

        return unique_recs

    def _recommend_foundation(
        self,
        topic: str,
        solved_ids: Set[str],
        problems: List[Dict],
    ) -> List[ProblemRecommendation]:
        easy_unsolved = [
            p for p in problems
            if topic in p.get("topics", [])
            and p.get("difficulty", "").lower() == "easy"
            and p["id"] not in solved_ids
        ]
        return [
            ProblemRecommendation(
                problem_id=p["id"],
                platform=p["platform"],
                name=p["name"],
                url=p.get("url", ""),
                difficulty=p.get("difficulty", "easy"),
                topics=p.get("topics", []),
                patterns=p.get("patterns", []),
                reason=(
                    f"Build your foundation in {topic} — "
                    "this easy problem introduces core concepts."
                ),
                expected_outcome=(
                    f"Understand the basic data structure and operations for {topic}."
                ),
                priority=8,
            )
            for p in easy_unsolved[:2]
        ]

    def _recommend_for_weak_topic(
        self,
        topic: str,
        mastery: TopicMasteryResult,
        solved_ids: Set[str],
        problems: List[Dict],
    ) -> List[ProblemRecommendation]:
        breakdown = mastery.score_breakdown

        if breakdown.get("pattern_coverage", 100) < 40:
            medium_unsolved = [
                p for p in problems
                if topic in p.get("topics", [])
                and p.get("difficulty", "").lower() == "medium"
                and p["id"] not in solved_ids
            ]
            return [
                ProblemRecommendation(
                    problem_id=p["id"],
                    platform=p["platform"],
                    name=p["name"],
                    url=p.get("url", ""),
                    difficulty="medium",
                    topics=p.get("topics", []),
                    patterns=p.get("patterns", []),
                    reason=(
                        f"Your {topic} pattern coverage is limited. "
                        "This problem introduces a new pattern variant."
                    ),
                    expected_outcome=f"Expand your pattern toolkit for {topic}.",
                    priority=7,
                )
                for p in medium_unsolved[:3]
            ]
        return []

    def _recommend_difficulty_push(
        self,
        topic: str,
        solved_ids: Set[str],
        problems: List[Dict],
    ) -> List[ProblemRecommendation]:
        hard_unsolved = [
            p for p in problems
            if topic in p.get("topics", [])
            and p.get("difficulty", "").lower() == "hard"
            and p["id"] not in solved_ids
        ]
        return [
            ProblemRecommendation(
                problem_id=p["id"],
                platform=p["platform"],
                name=p["name"],
                url=p.get("url", ""),
                difficulty="hard",
                topics=p.get("topics", []),
                patterns=p.get("patterns", []),
                reason=(
                    f"You have intermediate {topic} mastery. "
                    "This hard problem will push your understanding further."
                ),
                expected_outcome=f"Develop fluency with complex {topic} applications.",
                priority=6,
            )
            for p in hard_unsolved[:2]
        ]
