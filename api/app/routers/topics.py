from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from app.database import get_db
from app.models.topic import DSATopic
from app.models.pattern import DSAPattern

router = APIRouter()


class PatternSummary(BaseModel):
    id: str
    name: str
    slug: str
    difficulty_level: Optional[str] = "medium"

    class Config:
        from_attributes = True


class TopicResponse(BaseModel):
    id: str
    name: str
    slug: str
    parent_id: Optional[str] = None
    description: Optional[str] = None
    sort_order: int = 0
    patterns: List[PatternSummary] = []

    class Config:
        from_attributes = True


@router.get("", response_model=List[TopicResponse])
def get_topics(db: Session = Depends(get_db)):
    """Get all DSA topics with their associated patterns."""
    topics = db.query(DSATopic).order_by(DSATopic.sort_order).all()
    result = []
    for t in topics:
        patterns = [
            PatternSummary(
                id=str(p.id),
                name=p.name,
                slug=p.slug,
                difficulty_level=p.difficulty_level,
            )
            for p in t.patterns
        ]
        result.append(
            TopicResponse(
                id=str(t.id),
                name=t.name,
                slug=t.slug,
                parent_id=str(t.parent_id) if t.parent_id else None,
                description=t.description,
                sort_order=t.sort_order or 0,
                patterns=patterns,
            )
        )
    return result


@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic_by_id(topic_id: str, db: Session = Depends(get_db)):
    """Get single topic detail."""
    try:
        t_uuid = uuid.UUID(topic_id)
        topic = db.query(DSATopic).filter(DSATopic.id == t_uuid).first()
    except ValueError:
        topic = db.query(DSATopic).filter(DSATopic.slug == topic_id).first()

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    patterns = [
        PatternSummary(
            id=str(p.id),
            name=p.name,
            slug=p.slug,
            difficulty_level=p.difficulty_level,
        )
        for p in topic.patterns
    ]
    return TopicResponse(
        id=str(topic.id),
        name=topic.name,
        slug=topic.slug,
        parent_id=str(topic.parent_id) if topic.parent_id else None,
        description=topic.description,
        sort_order=topic.sort_order or 0,
        patterns=patterns,
    )
