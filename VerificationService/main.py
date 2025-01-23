from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db, SessionLocal
from datetime import datetime, timedelta
import uuid
from email_service import send_verification_email
import os
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.database import wait_for_db

# Wait for database to be ready before creating tables
engine = wait_for_db(os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/verificationdb"))
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Verification Service")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/verify/request", response_model=schemas.VerificationResponse)
async def request_verification(
    verification: schemas.VerificationCreate,
    db: Session = Depends(get_db)
):
    # Generate verification code
    verification_code = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=24)
    
    # Create verification record
    db_verification = models.Verification(
        user_id=verification.user_id,
        email=verification.email,
        code=verification_code,
        expires_at=expires_at
    )
    db.add(db_verification)
    db.commit()
    db.refresh(db_verification)
    
    # Send verification email
    verification_link = f"http://localhost:8002/users/verify/{verification_code}"
    email_sent = send_verification_email(verification.email, verification_code)
    
    if email_sent:
        return {
            "message": "Verification email sent successfully",
            "verification_link": verification_link
        }
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to send verification email"
        )

@app.post("/verify/confirm/{code}")
async def confirm_verification(code: str, db: Session = Depends(get_db)):
    verification = db.query(models.Verification).filter(
        models.Verification.code == code,
        models.Verification.is_verified == False,
        models.Verification.expires_at > datetime.utcnow()
    ).first()
    
    if not verification:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired verification code"
        )
    
    verification.is_verified = True
    verification.verified_at = datetime.utcnow()
    db.commit()
    
    return {
        "message": "Email verified successfully",
        "user_id": verification.user_id
    }
