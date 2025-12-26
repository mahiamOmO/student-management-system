from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, database, utils, auth

# Automatically creates tables in the new database file
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "UAP Student API is running"}

# --- Auth: Register & Login ---

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = utils.hash_password(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pwd, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Courses & Enrollment ---

@app.post("/courses/", response_model=schemas.CourseResponse)
def create_course(course: schemas.CourseCreate, db: Session = Depends(database.get_db)):
    db_course = models.Course(course_code=course.course_code, title=course.title, credits=course.credits)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.post("/enroll/{course_id}")
def enroll(course_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    
    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or Course not found")
    
    student.courses.append(course)
    db.commit()
    return {"message": "Enrolled successfully"}

# --- Results Management ---

@app.post("/results/", response_model=schemas.ResultResponse)
def add_result(result: schemas.ResultCreate, db: Session = Depends(database.get_db)):
    final_grade = utils.calculate_grade(result.marks)
    db_result = models.Result(
        student_id=result.student_id, 
        course_id=result.course_id, 
        marks=result.marks, 
        grade=final_grade
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result
# app/main.py এ যোগ করো
@app.post("/students/", response_model=schemas.StudentResponse)
def create_student_profile(
    student: schemas.StudentCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Check if user already has a student profile
    existing_profile = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    new_student = models.Student(**student.dict(), user_id=current_user.id)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student