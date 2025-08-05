from pydantic import BaseModel
from typing import List, Optional

class ResumeData(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]
    address: Optional[str]
    skills: List[str]
    education: List[str]
    experience: List[str]
    certifications: List[str]
    projects: List[str]
    summary: Optional[str]
