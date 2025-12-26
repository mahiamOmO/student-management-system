from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, database, utils, auth

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "UAP Student API is running"}


# --- Register ---
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = utils.hash_password(user.password)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_pwd,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# --- Login ---
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not user or not utils.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role}
    )
    return {"access_token": access_token, "token_type": "bearer"}


# --- Results ---
@app.post("/results/", response_model=schemas.ResultResponse)
def add_result(
    result: schemas.ResultCreate,
    db: Session = Depends(database.get_db)
):
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
