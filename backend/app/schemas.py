from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "student"

class UserResponse(UserBase):
    id: int
    role: str
    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    uap_id: str
    name: str
    department: str
    batch: str
    user_id: int

class StudentResponse(BaseModel):
    id: int
    uap_id: str
    name: str
    class Config:
        from_attributes = True

# Course Schemas
class CourseBase(BaseModel):
    course_code: str
    title: str
    credits: int

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    class Config:
        from_attributes = True

# To show a student along with their list of courses
class StudentWithCourses(StudentResponse):
    courses: list[CourseResponse] = []
    class Config:
        from_attributes = True