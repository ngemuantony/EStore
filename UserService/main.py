from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud, models, schemas, auth
from database import SessionLocal, engine, get_db
from datetime import timedelta
import requests
import os
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.database import wait_for_db

# Wait for database to be ready before creating tables
engine = wait_for_db(os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/userdb"))
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    new_user = crud.create_user(db=db, user=user)
    
    # Send verification request
    try:
        verification_response = requests.post(
            "http://localhost:8003/verify/request",
            json={"user_id": new_user.id, "email": new_user.email}
        )
        if verification_response.status_code != 200:
            # Log error but don't fail user creation
            print(f"Failed to send verification request: {verification_response.text}")
    except Exception as e:
        print(f"Error sending verification request: {str(e)}")
    
    return new_user

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user

@app.put("/users/me/", response_model=schemas.User)
async def update_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud.update_user(db=db, user=current_user, user_update=user_update)

@app.post("/users/verify/{verification_code}")
async def verify_user(
    verification_code: str,
    db: Session = Depends(get_db)
):
    # Verify with VerificationService
    try:
        verify_response = requests.post(
            f"http://localhost:8003/verify/confirm/{verification_code}"
        )
        if verify_response.status_code == 200:
            user_data = verify_response.json()
            return crud.verify_user(db=db, user_id=user_data["user_id"])
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid or expired verification code"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Verification failed: {str(e)}"
        )
