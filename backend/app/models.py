from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Association table to link Students and Courses (Many-to-Many)
enrollments = Table(
    "enrollments",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="student")
    
    # Link to Student profile
    student_profile = relationship("Student", back_populates="user", uselist=False)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    uap_id = Column(String, unique=True, index=True)
    name = Column(String)
    department = Column(String)
    batch = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Link to User account
    user = relationship("User", back_populates="student_profile")
    
    # Relationship to Courses through the enrollments association table
    courses = relationship("Course", secondary=enrollments, back_populates="students")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, unique=True, index=True) # e.g. CSE-101
    title = Column(String)
    credits = Column(Integer)
    
    # Relationship back to Students
    students = relationship("Student", secondary=enrollments, back_populates="courses")

# Add this to app/models.py
class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    marks = Column(Integer)
    grade = Column(String) # e.g., A+, A, B

    # Relationships to access student and course details easily
    student = relationship("Student")
    course = relationship("Course")