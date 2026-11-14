from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.problem import Problem
from app.intelligence.recommender import RecommendationEngine, ProblemRecommendation
from app.intelligence.mastery_engine import MasteryEngine

router = APIRouter()


class RecommendationResponse(BaseModel):
    problem_id: str
    platform: str
    name: str
    url: str
    difficulty: str
    topics: List[str]
    patterns: List[str]
    reason: str
    expected_outcome: str
    priority: int


@router.get("", response_model=List[RecommendationResponse])
def get_user_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get evidence-based problem recommendations for the current user.
    Uses the RecommendationEngine to find high-priority gaps.
    """
    all_db_problems = db.query(Problem).all()

    formatted_problems = []
    for p in all_db_problems:
        formatted_problems.append({
            "id": str(p.id),
            "problem_id": str(p.id),
            "platform": str(p.platform),
            "name": p.name,
            "url": p.url or f"https://leetcode.com/problems/{p.platform_id}/",
            "difficulty": str(p.difficulty or "medium"),
            "topics": [t.slug for t in p.topics],
            "patterns": [pt.slug for pt in p.patterns],
            "prerequisites": [],
        })

    engine = RecommendationEngine()
    mastery_engine = MasteryEngine()
    solved_ids = set()

    # Calculate current mastery for each topic
    from app.models.topic import DSATopic
    from app.models.pattern import DSAPattern
    from app.intelligence.mastery_engine import PatternRecord

    user_mastery = {}
    for t in db.query(DSATopic).all():
        topic_patterns = [
            PatternRecord(
                pattern_slug=p.slug,
                topic_slug=t.slug,
                total_patterns_in_topic=len(t.patterns),
            )
            for p in t.patterns
        ]
        user_mastery[t.slug] = mastery_engine.calculate_topic_mastery(
            topic_slug=t.slug,
            problems=[],
            available_patterns=topic_patterns,
        )

    goal = current_user.learning_goal.value if current_user.learning_goal else "fundamentals"

    recs = engine.generate_recommendations(
        user_mastery=user_mastery,
        solved_problem_ids=solved_ids,
        all_problems=formatted_problems,
        learning_goal=goal,
        max_recommendations=10,
    )

    return [
        RecommendationResponse(
            problem_id=r.problem_id,
            platform=r.platform,
            name=r.name,
            url=r.url,
            difficulty=r.difficulty,
            topics=r.topics,
            patterns=r.patterns,
            reason=r.reason,
            expected_outcome=r.expected_outcome,
            priority=r.priority,
        )
        for r in recs
    ]
