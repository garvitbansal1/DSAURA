import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Enum as SAEnum, Text
from sqlalchemy import Uuid as UUID
from sqlalchemy.orm import relationship
from app.database import Base


class SolvingMode(str, enum.Enum):
    independent = "independent"
    hints = "hints"
    editorial = "editorial"
    assisted = "assisted"
    re_solved = "re_solved"
    unknown = "unknown"


class ProblemStatus(str, enum.Enum):
    not_started = "not_started"
    attempted = "attempted"
    solved = "solved"
    needs_revision = "needs_revision"


class UserProblemHistory(Base):
    __tablename__ = "user_problem_history"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    status = Column(SAEnum(ProblemStatus), default=ProblemStatus.attempted)
    solving_mode = Column(SAEnum(SolvingMode), default=SolvingMode.unknown)
    self_reported = Column(Boolean, default=False)
    attempts = Column(Integer, default=1)
    first_solved_at = Column(DateTime, nullable=True)
    last_attempted_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)
    problem = relationship("Problem")
    user = relationship("User")
