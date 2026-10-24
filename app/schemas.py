from pydantic import BaseModel, EmailStr
from typing import List, Optional
from pydantic import BaseModel, EmailStr
class EducationIn(BaseModel):
    school: str
    degree: Optional[str] = None
    start_year: Optional[str] = None
    end_year: Optional[str] = None


class ExperienceIn(BaseModel):
    company: str
    role: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None


class SkillIn(BaseModel):
    name: str


class ProjectIn(BaseModel):
    name: str
    description: Optional[str] = None
    link: Optional[str] = None


class ResumeIn(BaseModel):
    title: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
    education: List[EducationIn] = []
    experience: List[ExperienceIn] = []
    skills: List[SkillIn] = []
    projects: List[ProjectIn] = []


class EducationOut(EducationIn):
    id: int
    model_config = {"from_attributes": True}


class ExperienceOut(ExperienceIn):
    id: int
    model_config = {"from_attributes": True}


class SkillOut(SkillIn):
    id: int
    model_config = {"from_attributes": True}


class ProjectOut(ProjectIn):
    id: int
    model_config = {"from_attributes": True}


class ResumeOut(BaseModel):
    id: int
    title: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
    education: List[EducationOut] = []
    experience: List[ExperienceOut] = []
    skills: List[SkillOut] = []
    projects: List[ProjectOut] = []
    model_config = {"from_attributes": True}
class RegisterIn(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    model_config = {"from_attributes": True}

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"