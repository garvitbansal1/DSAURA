from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from app.database import get_db
from app.models.pattern import DSAPattern
from app.models.problem import Problem

router = APIRouter()


class PatternDetail(BaseModel):
    id: str
    topic_id: str
    name: str
    slug: str
    explanation: Optional[str] = None
    when_to_use: Optional[str] = None
    recognition_clues: Optional[str] = None
    common_keywords: Optional[List[str]] = []
    pseudocode: Optional[str] = None
    java_template: Optional[str] = None
    python_template: Optional[str] = None
    time_complexity: Optional[str] = None
    space_complexity: Optional[str] = None
    common_mistakes: Optional[List[str]] = []
    difficulty_level: Optional[str] = "medium"

    class Config:
        from_attributes = True


class ProblemSummary(BaseModel):
    id: str
    title: str
    slug: str
    platform: str
    difficulty: str
    url: Optional[str] = None

    class Config:
        from_attributes = True


@router.get("", response_model=List[PatternDetail])
def get_patterns(
    topic_slug: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all patterns, optionally filtered by topic slug or difficulty."""
    query = db.query(DSAPattern)
    if difficulty:
        query = query.filter(DSAPattern.difficulty_level == difficulty)
    
    patterns = query.all()
    if topic_slug:
        patterns = [p for p in patterns if p.topic and p.topic.slug == topic_slug]

    return [
        PatternDetail(
            id=str(p.id),
            topic_id=str(p.topic_id),
            name=p.name,
            slug=p.slug,
            explanation=p.explanation,
            when_to_use=p.when_to_use,
            recognition_clues=p.recognition_clues,
            common_keywords=p.common_keywords or [],
            pseudocode=p.pseudocode,
            java_template=p.java_template,
            python_template=p.python_template,
            time_complexity=p.time_complexity,
            space_complexity=p.space_complexity,
            common_mistakes=p.common_mistakes or [],
            difficulty_level=p.difficulty_level,
        )
        for p in patterns
    ]


@router.get("/{pattern_id}", response_model=PatternDetail)
def get_pattern(pattern_id: str, db: Session = Depends(get_db)):
    """Get pattern by id or slug."""
    try:
        p_uuid = uuid.UUID(pattern_id)
        p = db.query(DSAPattern).filter(DSAPattern.id == p_uuid).first()
    except ValueError:
        p = db.query(DSAPattern).filter(DSAPattern.slug == pattern_id).first()

    if not p:
        raise HTTPException(status_code=404, detail="Pattern not found")

    return PatternDetail(
        id=str(p.id),
        topic_id=str(p.topic_id),
        name=p.name,
        slug=p.slug,
        explanation=p.explanation,
        when_to_use=p.when_to_use,
        recognition_clues=p.recognition_clues,
        common_keywords=p.common_keywords or [],
        pseudocode=p.pseudocode,
        java_template=p.java_template,
        python_template=p.python_template,
        time_complexity=p.time_complexity,
        space_complexity=p.space_complexity,
        common_mistakes=p.common_mistakes or [],
        difficulty_level=p.difficulty_level,
    )


@router.get("/{pattern_id}/problems", response_model=List[ProblemSummary])
def get_pattern_problems(pattern_id: str, db: Session = Depends(get_db)):
    """Get problems tagged with this pattern."""
    try:
        p_uuid = uuid.UUID(pattern_id)
        p = db.query(DSAPattern).filter(DSAPattern.id == p_uuid).first()
    except ValueError:
        p = db.query(DSAPattern).filter(DSAPattern.slug == pattern_id).first()

    if not p:
        raise HTTPException(status_code=404, detail="Pattern not found")

    return [
        ProblemSummary(
            id=str(pr.id),
            title=pr.name,
            slug=pr.platform_id,
            platform=str(pr.platform),
            difficulty=str(pr.difficulty or "medium"),
            url=pr.url,
        )
        for pr in p.problems
    ]
