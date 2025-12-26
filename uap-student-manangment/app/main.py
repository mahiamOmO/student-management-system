from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database, utils

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