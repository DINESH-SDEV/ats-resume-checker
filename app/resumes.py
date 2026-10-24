from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Resume, Education, Experience, Skill, Project
from app.schemas import ResumeIn, ResumeOut
from app.auth import get_current_user

router = APIRouter(prefix="/resumes", tags=["resumes"])


def fill_children(resume: Resume, data: ResumeIn):
    resume.education = [Education(**e.model_dump()) for e in data.education]
    resume.experience = [Experience(**e.model_dump()) for e in data.experience]
    resume.skills = [Skill(**s.model_dump()) for s in data.skills]
    resume.projects = [Project(**p.model_dump()) for p in data.projects]


def get_own_resume(resume_id: int, user: User, db: Session) -> Resume:
    resume = db.get(Resume, resume_id)
    if not resume or resume.user_id != user.id:
        raise HTTPException(404, "Resume not found")
    return resume


@router.post("", response_model=ResumeOut)
def create_resume(data: ResumeIn, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    resume = Resume(user_id=user.id, title=data.title, full_name=data.full_name,
                    email=data.email, phone=data.phone, summary=data.summary)
    fill_children(resume, data)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


@router.get("", response_model=List[ResumeOut])
def list_resumes(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Resume).filter(Resume.user_id == user.id).all()


@router.get("/{resume_id}", response_model=ResumeOut)
def read_resume(resume_id: int, user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    return get_own_resume(resume_id, user, db)


@router.put("/{resume_id}", response_model=ResumeOut)
def update_resume(resume_id: int, data: ResumeIn, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    resume = get_own_resume(resume_id, user, db)
    for field in ("title", "full_name", "email", "phone", "summary"):
        setattr(resume, field, getattr(data, field))
    fill_children(resume, data)
    db.commit()
    db.refresh(resume)
    return resume


@router.delete("/{resume_id}")
def delete_resume(resume_id: int, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    resume = get_own_resume(resume_id, user, db)
    db.delete(resume)
    db.commit()
    return {"detail": "Resume deleted"}