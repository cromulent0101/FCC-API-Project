# pylint: skip-file
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.expression import null
from database import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    # created_at = Column(DateTime, nullable=False)
    