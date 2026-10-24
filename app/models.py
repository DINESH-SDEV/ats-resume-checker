from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base

class Experience(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    company = Column(String(150), nullable=False)
    role = Column(String(150))
    start_date = Column(String(20))
    end_date = Column(String(20))
    description = Column(Text)


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    name = Column(String(100), nullable=False)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    link = Column(String(300))
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    analyses = relationship(
        "ResumeAnalysis",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    resumes = relationship(
        "Resume",
        cascade="all, delete-orphan"
    )


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume_text = Column(Text, nullable=False)
    job_text = Column(Text, nullable=False)
    score = Column(Float, nullable=False)

    matched_keywords = Column(Text, nullable=True)
    missing_keywords = Column(Text, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="analyses")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(150), nullable=False)
    full_name = Column(String(100))
    email = Column(String(150))
    phone = Column(String(30))
    summary = Column(Text)

    education = relationship("Education", cascade="all, delete-orphan")
    experience = relationship("Experience", cascade="all, delete-orphan")
    skills = relationship("Skill", cascade="all, delete-orphan")
    projects = relationship("Project", cascade="all, delete-orphan")


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    school = Column(String(150), nullable=False)
    degree = Column(String(150))