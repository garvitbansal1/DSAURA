"""
DSAURA Knowledge Gap Analyzer

Detects specific knowledge gaps from user's problem-solving history.
Philosophy: High problem count does not equal broad knowledge.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from .mastery_engine import ProblemRecord, PatternRecord, TopicMasteryResult, MasteryLevel


@dataclass
class KnowledgeGap:
    gap_type: str  # pattern_concentration, missing_pattern, insufficient_advanced, narrow_exposure, high_unsolved
    severity: str  # high, medium, low
    topic_slug: str
    pattern_slug: Optional[str]
    title: str
    description: str
    evidence: Dict
    recommendation: str


class GapAnalyzer:
    """
    Identifies specific knowledge gaps from user's coding history.
    Detects where users are stuck in pattern repetition vs. genuine breadth.
    """

    def analyze(
        self,
        topic_slug: str,
        problems: List[ProblemRecord],
        available_patterns: List[PatternRecord],
        mastery_result: Optional[TopicMasteryResult] = None,
    ) -> List[KnowledgeGap]:
        gaps: List[KnowledgeGap] = []
        topic_problems = [p for p in problems if topic_slug in p.topics]

        if not topic_problems:
            return []

        gaps.extend(self._detect_pattern_concentration(topic_slug, topic_problems, available_patterns))
        gaps.extend(self._detect_missing_patterns(topic_slug, topic_problems, available_patterns))
        gaps.extend(self._detect_insufficient_advanced(topic_slug, topic_problems))
        gaps.extend(self._detect_narrow_exposure(topic_slug, topic_problems))
        gaps.extend(self._detect_high_unsolved_ratio(topic_slug, topic_problems))

        return sorted(gaps, key=lambda g: {"high": 0, "medium": 1, "low": 2}[g.severity])

    def _detect_pattern_concentration(
        self,
        topic: str,
        problems: List[ProblemRecord],
        patterns: List[PatternRecord],
    ) -> List[KnowledgeGap]:
        gaps: List[KnowledgeGap] = []
        all_patterns: List[str] = []
        for p in problems:
            all_patterns.extend(p.patterns)

        if not all_patterns or len(problems) < 5:
            return []

        pattern_counts: Dict[str, int] = {}
        for pat in all_patterns:
            pattern_counts[pat] = pattern_counts.get(pat, 0) + 1

        total = len(all_patterns)
        for pattern, count in pattern_counts.items():
            concentration = count / total
            if concentration > 0.5 and len(pattern_counts) > 1:
                gaps.append(KnowledgeGap(
                    gap_type="pattern_concentration",
                    severity="high" if concentration > 0.7 else "medium",
                    topic_slug=topic,
                    pattern_slug=pattern,
                    title=f"High concentration on '{pattern}' pattern",
                    description=(
                        f"You have solved {len(problems)} {topic} problem(s), but {count} of them "
                        f"({int(concentration * 100)}%) belong to the '{pattern}' pattern. "
                        f"Your problem count is high, but your pattern coverage remains limited."
                    ),
                    evidence={
                        "pattern": pattern,
                        "count": count,
                        "total": total,
                        "concentration": round(concentration, 2),
                    },
                    recommendation=(
                        f"Practice other {topic} patterns to build broader understanding. "
                        f"Aim to explore at least 3 different patterns in this topic."
                    ),
                ))
        return gaps

    def _detect_missing_patterns(
        self,
        topic: str,
        problems: List[ProblemRecord],
        available_patterns: List[PatternRecord],
    ) -> List[KnowledgeGap]:
        gaps: List[KnowledgeGap] = []
        topic_patterns = {p.pattern_slug for p in available_patterns if p.topic_slug == topic}
        practiced_patterns: set = set()
        for p in problems:
            practiced_patterns.update(p.patterns)

        missing = topic_patterns - practiced_patterns
        covered = len(practiced_patterns & topic_patterns)

        if missing and len(problems) >= 3:
            missing_list = list(missing)
            gaps.append(KnowledgeGap(
                gap_type="missing_pattern",
                severity="medium" if len(missing) <= 2 else "high",
                topic_slug=topic,
                pattern_slug=None,
                title=f"{len(missing)} pattern(s) not yet explored in {topic}",
                description=(
                    f"You have practiced {covered} out of {len(topic_patterns)} patterns in {topic}. "
                    f"Missing: {', '.join(missing_list[:3])}{'...' if len(missing_list) > 3 else ''}."
                ),
                evidence={
                    "missing": missing_list,
                    "total_patterns": len(topic_patterns),
                    "practiced": covered,
                },
                recommendation=f"Explore the missing patterns in {topic} to build comprehensive knowledge.",
            ))
        return gaps

    def _detect_insufficient_advanced(
        self, topic: str, problems: List[ProblemRecord]
    ) -> List[KnowledgeGap]:
        gaps: List[KnowledgeGap] = []
        solved = [p for p in problems if p.status == "solved"]
        if len(solved) < 5:
            return []

        hard_count = sum(1 for p in solved if p.difficulty.lower() == "hard")
        if hard_count == 0:
            gaps.append(KnowledgeGap(
                gap_type="insufficient_advanced",
                severity="medium",
                topic_slug=topic,
                pattern_slug=None,
                title=f"No hard problems solved in {topic}",
                description=(
                    f"You have solved {len(solved)} {topic} problems but none are classified as Hard. "
                    f"Advanced problem-solving requires tackling harder variants to truly test pattern fluency."
                ),
                evidence={"solved_count": len(solved), "hard_count": 0},
                recommendation=(
                    f"Attempt at least 1–2 hard-difficulty {topic} problems "
                    f"to validate deeper understanding."
                ),
            ))
        return gaps

    def _detect_narrow_exposure(
        self, topic: str, problems: List[ProblemRecord]
    ) -> List[KnowledgeGap]:
        gaps: List[KnowledgeGap] = []
        if len(problems) >= 10:
            unique_patterns: set = set()
            for p in problems:
                unique_patterns.update(p.patterns)
            if len(unique_patterns) <= 2:
                gaps.append(KnowledgeGap(
                    gap_type="narrow_exposure",
                    severity="high",
                    topic_slug=topic,
                    pattern_slug=None,
                    title=f"Wide problem count, narrow pattern range in {topic}",
                    description=(
                        f"Despite solving {len(problems)} {topic} problems, only "
                        f"{len(unique_patterns)} distinct pattern(s) have been practiced. "
                        f"This suggests repetitive practice rather than broad learning."
                    ),
                    evidence={
                        "problem_count": len(problems),
                        "unique_patterns": len(unique_patterns),
                    },
                    recommendation=(
                        "Deliberately seek problems that use different algorithms "
                        "and data structures within this topic."
                    ),
                ))
        return gaps

    def _detect_high_unsolved_ratio(
        self, topic: str, problems: List[ProblemRecord]
    ) -> List[KnowledgeGap]:
        gaps: List[KnowledgeGap] = []
        if len(problems) >= 5:
            unsolved = sum(1 for p in problems if p.status != "solved")
            ratio = unsolved / len(problems)
            if ratio > 0.5:
                gaps.append(KnowledgeGap(
                    gap_type="high_unsolved_ratio",
                    severity="medium",
                    topic_slug=topic,
                    pattern_slug=None,
                    title=f"High unsolved ratio in {topic}",
                    description=(
                        f"{unsolved} out of {len(problems)} attempted {topic} problems "
                        f"remain unsolved or need revision. "
                        f"This may indicate a foundational gap or need to revisit prerequisites."
                    ),
                    evidence={
                        "unsolved": unsolved,
                        "total": len(problems),
                        "ratio": round(ratio, 2),
                    },
                    recommendation=(
                        f"Revisit foundational {topic} concepts before attempting more problems."
                    ),
                ))
        return gaps
