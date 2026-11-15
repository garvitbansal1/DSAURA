import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy import Uuid as UUID
from sqlalchemy.orm import relationship, backref
from app.database import Base


class DSATopic(Base):
    __tablename__ = "dsa_topics"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("dsa_topics.id"), nullable=True)
    sort_order = Column(Integer, default=0)
    description = Column(String(1000), nullable=True)
    children = relationship(
        "DSATopic",
        backref=backref("parent", remote_side="DSATopic.id"),
        foreign_keys="DSATopic.parent_id"
    )
    patterns = relationship("DSAPattern", back_populates="topic")
