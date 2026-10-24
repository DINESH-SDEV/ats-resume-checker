
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"
    hashed_password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)

    analyses = relationship(
        "ResumeAnalysis",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"
    hashed_password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, index=True)
    resume_text = Column(Text, nullable=False)
    job_text = Column(Text, nullable=False)
    score = Column(Float, nullable=False)

    matched_keywords = Column(Text, nullable=True)
    missing_keywords = Column(Text, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="analyses")
