"""
DSAURA Evidence-Based Mastery Engine

Calculates mastery scores using multiple evidence dimensions.
Core philosophy: Solving more problems does not equal learning more.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import math
from datetime import datetime, timedelta


class MasteryLevel(str, Enum):
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    BEGINNER = "beginner"
    DEVELOPING = "developing"
    INTERMEDIATE = "intermediate"
    STRONG = "strong"
    ADVANCED = "advanced"


@dataclass
class MasteryWeights:
    """Configurable mastery dimension weights. Must sum to 1.0."""
    pattern_coverage: float = 0.30
    independent_solving: float = 0.25
    difficulty_progression: float = 0.20
    problem_diversity: float = 0.15
    revision_retention: float = 0.10

    def __post_init__(self):
        total = sum([
            self.pattern_coverage, self.independent_solving,
            self.difficulty_progression, self.problem_diversity,
            self.revision_retention
        ])
        assert abs(total - 1.0) < 0.001, f"Weights must sum to 1.0, got {total}"


@dataclass
class ProblemRecord:
    problem_id: str
    platform: str
    difficulty: str  # easy, medium, hard
    patterns: List[str]  # pattern slugs
    topics: List[str]  # topic slugs
    status: str  # solved, attempted, needs_revision
    solving_mode: str  # independent, hints, editorial, assisted, re_solved, unknown
    self_reported: bool = False
    attempts: int = 1
    first_solved_at: Optional[datetime] = None
    last_attempted_at: Optional[datetime] = None


@dataclass
class PatternRecord:
    pattern_slug: str
    topic_slug: str
    total_patterns_in_topic: int


@dataclass
class RevisionRecord:
    problem_id: str
    due_date: datetime
    last_revised: Optional[datetime]
    ease_factor: float
    repetition_count: int


@dataclass
class TopicMasteryResult:
    topic_slug: str
    mastery_score: float  # 0-100
    mastery_level: MasteryLevel
    evidence_confidence: float  # 0-1
    score_breakdown: Dict[str, float]
    evidence_summary: Dict
    has_sufficient_evidence: bool
    minimum_evidence_met: bool


class MasteryEngine:
    """
    Evidence-Based Mastery Calculation Engine

    Evaluates mastery across 5 dimensions:
    1. Pattern Coverage (30%) — how many patterns in the topic have been practiced
    2. Independent Solving Performance (25%) — quality of solving
    3. Difficulty Progression (20%) — progression from easy to hard
    4. Problem Diversity (15%) — variety within topic
    5. Revision Retention (10%) — performance on revision
    """

    MIN_PROBLEMS_FOR_SCORE = 3
    MIN_EVIDENCE_CONFIDENCE = 0.3

    def __init__(self, weights: Optional[MasteryWeights] = None):
        self.weights = weights or MasteryWeights()

    def calculate_topic_mastery(
        self,
        topic_slug: str,
        problems: List[ProblemRecord],
        available_patterns: List[PatternRecord],
        revision_records: Optional[List[RevisionRecord]] = None,
    ) -> TopicMasteryResult:
        """Calculate comprehensive mastery for a topic."""

        topic_problems = [p for p in problems if topic_slug in p.topics]

        if len(topic_problems) < self.MIN_PROBLEMS_FOR_SCORE:
            return TopicMasteryResult(
                topic_slug=topic_slug,
                mastery_score=0.0,
                mastery_level=MasteryLevel.INSUFFICIENT_EVIDENCE,
                evidence_confidence=0.0,
                score_breakdown={},
                evidence_summary={
                    "message": (
                        f"Only {len(topic_problems)} problem(s) recorded. "
                        f"Need at least {self.MIN_PROBLEMS_FOR_SCORE} to estimate mastery."
                    ),
                    "problems_recorded": len(topic_problems),
                    "problems_needed": self.MIN_PROBLEMS_FOR_SCORE,
                },
                has_sufficient_evidence=False,
                minimum_evidence_met=False,
            )

        pattern_score, pattern_evidence = self._calculate_pattern_coverage(
            topic_problems, available_patterns, topic_slug
        )
        solving_score, solving_evidence = self._calculate_solving_performance(topic_problems)
        difficulty_score, difficulty_evidence = self._calculate_difficulty_progression(topic_problems)
        diversity_score, diversity_evidence = self._calculate_problem_diversity(topic_problems)
        revision_score, revision_evidence = self._calculate_revision_retention(
            topic_problems, revision_records or []
        )

        breakdown = {
            "pattern_coverage": round(pattern_score, 2),
            "independent_solving": round(solving_score, 2),
            "difficulty_progression": round(difficulty_score, 2),
            "problem_diversity": round(diversity_score, 2),
            "revision_retention": round(revision_score, 2),
        }

        composite = (
            pattern_score * self.weights.pattern_coverage
            + solving_score * self.weights.independent_solving
            + difficulty_score * self.weights.difficulty_progression
            + diversity_score * self.weights.problem_diversity
            + revision_score * self.weights.revision_retention
        )

        self_reported_ratio = (
            sum(1 for p in topic_problems if p.self_reported) / len(topic_problems)
        )
        volume_factor = min(1.0, len(topic_problems) / 10)
        evidence_confidence = volume_factor * (1.0 - 0.3 * self_reported_ratio)

        level = self._score_to_level(composite)

        return TopicMasteryResult(
            topic_slug=topic_slug,
            mastery_score=round(composite, 2),
            mastery_level=level,
            evidence_confidence=round(evidence_confidence, 2),
            score_breakdown=breakdown,
            evidence_summary={
                "total_problems": len(topic_problems),
                "solved_problems": sum(1 for p in topic_problems if p.status == "solved"),
                "patterns_covered": pattern_evidence.get("covered"),
                "patterns_available": pattern_evidence.get("total"),
                "has_hard_problems": difficulty_evidence.get("has_hard", False),
                "solving_mode_distribution": solving_evidence.get("mode_distribution", {}),
                "self_reported_ratio": round(self_reported_ratio, 2),
                "note": (
                    "Scores are estimates based on available evidence, "
                    "not certified assessments."
                ),
            },
            has_sufficient_evidence=evidence_confidence >= self.MIN_EVIDENCE_CONFIDENCE,
            minimum_evidence_met=True,
        )

    def _calculate_pattern_coverage(
        self,
        problems: List[ProblemRecord],
        available_patterns: List[PatternRecord],
        topic_slug: str,
    ) -> Tuple[float, dict]:
        topic_patterns = [p for p in available_patterns if p.topic_slug == topic_slug]
        total_patterns = len(topic_patterns)
        if total_patterns == 0:
            return 50.0, {"covered": 0, "total": 0}

        practiced_pattern_slugs: set = set()
        for prob in problems:
            if topic_slug in prob.topics:
                practiced_pattern_slugs.update(prob.patterns)

        topic_pattern_slugs = {p.pattern_slug for p in topic_patterns}
        covered = len(practiced_pattern_slugs & topic_pattern_slugs)
        coverage_ratio = covered / total_patterns
        score = coverage_ratio * 100

        return score, {
            "covered": covered,
            "total": total_patterns,
            "ratio": round(coverage_ratio, 2),
        }

    def _calculate_solving_performance(
        self, problems: List[ProblemRecord]
    ) -> Tuple[float, dict]:
        if not problems:
            return 0.0, {}

        mode_scores = {
            "independent": 100,
            "re_solved": 90,
            "hints": 50,
            "editorial": 25,
            "assisted": 10,
            "unknown": 40,
        }

        solved = [p for p in problems if p.status == "solved"]
        if not solved:
            return 10.0, {"message": "No solved problems recorded"}

        total_score = sum(mode_scores.get(p.solving_mode, 40) for p in solved)
        avg_score = total_score / len(solved)

        mode_dist: Dict[str, int] = {}
        for p in solved:
            mode_dist[p.solving_mode] = mode_dist.get(p.solving_mode, 0) + 1

        return avg_score, {"mode_distribution": mode_dist, "solved_count": len(solved)}

    def _calculate_difficulty_progression(
        self, problems: List[ProblemRecord]
    ) -> Tuple[float, dict]:
        solved = [p for p in problems if p.status == "solved"]
        if not solved:
            return 0.0, {"has_hard": False}

        difficulty_map = {"easy": 1, "medium": 2, "hard": 3}
        difficulties = [difficulty_map.get(p.difficulty.lower(), 1) for p in solved]

        has_easy = any(d == 1 for d in difficulties)
        has_medium = any(d == 2 for d in difficulties)
        has_hard = any(d == 3 for d in difficulties)

        if has_hard and has_medium:
            base_score = 85.0
        elif has_hard:
            base_score = 70.0
        elif has_medium:
            base_score = 50.0
        else:
            base_score = 25.0

        hard_ratio = sum(1 for d in difficulties if d == 3) / len(difficulties)
        bonus = hard_ratio * 15

        return min(100.0, base_score + bonus), {
            "has_hard": has_hard,
            "has_medium": has_medium,
            "hard_ratio": round(hard_ratio, 2),
        }

    def _calculate_problem_diversity(
        self, problems: List[ProblemRecord]
    ) -> Tuple[float, dict]:
        if not problems:
            return 0.0, {}

        all_patterns: List[str] = []
        for p in problems:
            all_patterns.extend(p.patterns)

        if not all_patterns:
            return 30.0, {"message": "No pattern classifications available"}

        pattern_counts: Dict[str, int] = {}
        for pattern in all_patterns:
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

        unique_patterns = len(pattern_counts)
        total_instances = len(all_patterns)

        entropy = 0.0
        for count in pattern_counts.values():
            prob = count / total_instances
            if prob > 0:
                entropy -= prob * math.log2(prob)

        max_entropy = math.log2(unique_patterns) if unique_patterns > 1 else 1
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0

        max_concentration = max(pattern_counts.values()) / total_instances
        concentration_penalty = max(0.0, (max_concentration - 0.5) * 100)

        score = normalized_entropy * 100 - concentration_penalty
        return max(0.0, min(100.0, score)), {
            "unique_patterns": unique_patterns,
            "max_concentration": round(max_concentration, 2),
            "most_practiced_pattern": max(pattern_counts, key=lambda k: pattern_counts[k]),
        }

    def _calculate_revision_retention(
        self,
        problems: List[ProblemRecord],
        revision_records: List[RevisionRecord],
    ) -> Tuple[float, dict]:
        if not revision_records:
            return 50.0, {"message": "No revision data — using neutral score"}

        completed = [r for r in revision_records if r.last_revised is not None]
        if not completed:
            return 40.0, {"message": "Revision scheduled but not completed"}

        avg_ease = sum(r.ease_factor for r in completed) / len(completed)
        normalized = (avg_ease - 1.3) / (2.5 - 1.3) * 100

        return max(0.0, min(100.0, normalized)), {
            "revisions_completed": len(completed),
            "avg_ease_factor": round(avg_ease, 2),
        }

    @staticmethod
    def _score_to_level(score: float) -> MasteryLevel:
        if score <= 20:
            return MasteryLevel.BEGINNER
        elif score <= 40:
            return MasteryLevel.DEVELOPING
        elif score <= 60:
            return MasteryLevel.INTERMEDIATE
        elif score <= 80:
            return MasteryLevel.STRONG
        else:
            return MasteryLevel.ADVANCED

    def calculate_pattern_mastery(
        self,
        pattern_slug: str,
        problems: List[ProblemRecord],
    ) -> Dict:
        """Calculate mastery for a specific pattern."""
        pattern_problems = [p for p in problems if pattern_slug in p.patterns]

        if len(pattern_problems) < 2:
            return {
                "pattern_slug": pattern_slug,
                "mastery_score": 0.0,
                "mastery_level": MasteryLevel.INSUFFICIENT_EVIDENCE.value,
                "evidence_confidence": 0.0,
                "problems_attempted": len(pattern_problems),
                "problems_solved": 0,
                "has_sufficient_evidence": False,
            }

        solved = [p for p in pattern_problems if p.status == "solved"]
        solving_score, _ = self._calculate_solving_performance(pattern_problems)
        difficulty_score, _ = self._calculate_difficulty_progression(pattern_problems)

        composite = solving_score * 0.5 + difficulty_score * 0.5
        level = self._score_to_level(composite)

        return {
            "pattern_slug": pattern_slug,
            "mastery_score": round(composite, 2),
            "mastery_level": level.value,
            "evidence_confidence": round(min(1.0, len(pattern_problems) / 5), 2),
            "problems_attempted": len(pattern_problems),
            "problems_solved": len(solved),
            "has_sufficient_evidence": len(pattern_problems) >= 2,
        }
