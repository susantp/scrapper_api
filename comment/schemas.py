from sqlalchemy.schema import Column
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime, Integer, String, Text

from app.database import Base


class CommentSchema(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), unique=True, nullable=False)
    body = Column(Text(1000), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
