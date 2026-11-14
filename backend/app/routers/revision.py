from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, date, timedelta
import uuid

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.revision import RevisionSchedule
from app.models.problem import Problem
from app.intelligence.spaced_repetition import sm2_update

router = APIRouter()


class RevisionItemResponse(BaseModel):
    id: str
    problem_id: str
    problem_title: str
    platform: str
    difficulty: str
    url: Optional[str]
    repetition_count: int
    ease_factor: float
    interval_days: int
    due_date: str
    is_overdue: bool
    status: str  # "due_today", "overdue", "upcoming"


class ReviewPayload(BaseModel):
    revision_id: str
    quality: int  # 0 to 5


class AddToRevisionPayload(BaseModel):
    problem_id: str
    initial_quality: Optional[int] = 4


@router.get("", response_model=List[RevisionItemResponse])
def get_revision_queue(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns the user's active revision schedule sorted by due urgency:
    Overdue -> Due Today -> Upcoming.
    If empty, auto-seeds initial high-yield foundation problems into the revision queue.
    """
    schedules = db.query(RevisionSchedule).filter(
        RevisionSchedule.user_id == current_user.id
    ).order_by(RevisionSchedule.due_date.asc()).all()

    today = date.today()

    # If new user has no revision schedules yet, create initial queue from problems
    if not schedules:
        foundation_problems = db.query(Problem).limit(5).all()
        for idx, prob in enumerate(foundation_problems):
            due = today if idx < 2 else today + timedelta(days=idx + 1)
            sched = RevisionSchedule(
                user_id=current_user.id,
                problem_id=prob.id,
                ease_factor=2.5,
                repetition_count=0,
                interval_days=1,
                due_date=due,
            )
            db.add(sched)
        db.commit()
        schedules = db.query(RevisionSchedule).filter(
            RevisionSchedule.user_id == current_user.id
        ).order_by(RevisionSchedule.due_date.asc()).all()

    results = []
    for s in schedules:
        prob = s.problem
        due = s.due_date
        if due < today:
            status = "overdue"
            is_overdue = True
        elif due == today:
            status = "due_today"
            is_overdue = False
        else:
            status = "upcoming"
            is_overdue = False

        results.append(RevisionItemResponse(
            id=str(s.id),
            problem_id=str(s.problem_id),
            problem_title=prob.name if prob else "Problem",
            platform=prob.platform if prob else "leetcode",
            difficulty=prob.difficulty or "medium" if prob else "medium",
            url=prob.url or f"https://leetcode.com/problems/{prob.platform_id}/" if prob else None,
            repetition_count=s.repetition_count or 0,
            ease_factor=round(float(s.ease_factor or 2.5), 2),
            interval_days=s.interval_days or 1,
            due_date=str(due),
            is_overdue=is_overdue,
            status=status,
        ))

    return results


@router.post("/review")
def record_revision_review(
    payload: ReviewPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Records recall quality (0=Again, 3=Hard, 4=Good, 5=Easy)
    and computes the next optimal review interval using SM-2.
    """
    try:
        r_uuid = uuid.UUID(payload.revision_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid revision ID")

    sched = db.query(RevisionSchedule).filter(
        RevisionSchedule.id == r_uuid,
        RevisionSchedule.user_id == current_user.id
    ).first()

    if not sched:
        raise HTTPException(status_code=404, detail="Revision item not found")

    result = sm2_update(
        ease_factor=float(sched.ease_factor or 2.5),
        repetition_count=sched.repetition_count or 0,
        quality=payload.quality
    )

    sched.ease_factor = result.new_ease_factor
    sched.repetition_count = (sched.repetition_count or 0) + 1 if payload.quality >= 3 else 0
    sched.interval_days = result.next_interval_days
    sched.due_date = result.next_due_date
    sched.last_revised_at = datetime.utcnow()

    db.commit()

    return {
        "success": True,
        "message": f"Next review scheduled in {result.next_interval_days} day(s)",
        "next_due_date": str(result.next_due_date),
        "ease_factor": result.new_ease_factor,
        "interval_days": result.next_interval_days
    }
