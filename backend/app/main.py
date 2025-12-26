from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database, utils
from . import models, schemas, database, utils, auth

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_pwd = utils.hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_pwd, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/")
def home():
    return {"message": "UAP Student API is running"}

# --- Course Endpoints ---

# Create a new course
@app.post("/courses/", response_model=schemas.CourseResponse)
def create_course(course: schemas.CourseCreate, db: Session = Depends(database.get_db)):
    db_course = models.Course(
        course_code=course.course_code,
        title=course.title,
        credits=course.credits
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

# Enroll the logged-in student into a course
@app.post("/enroll/{course_id}")
def enroll_in_course(
    course_id: int, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Get the student profile linked to the logged-in user
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    # Get the course
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if already enrolled
    if course in student.courses:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")
    
    # Add course to student's courses list (Many-to-Many magic)
    student.courses.append(course)
    db.commit()
    return {"message": f"Successfully enrolled in {course.title}"}

# Get all courses for the logged-in student
@app.get("/my-courses", response_model=list[schemas.CourseResponse])
def get_my_courses(
    current_user: models.User = Depends(auth.get_current_user), 
    db: Session = Depends(database.get_db)
):
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Profile not found")
    return student.courses