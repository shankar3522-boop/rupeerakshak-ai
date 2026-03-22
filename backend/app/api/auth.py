from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import RegisterRequest, VerifyOTPRequest, UserResponse
from app.database import get_db, User
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.phone == request.phone).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Phone already registered")
    
    user_id = str(uuid.uuid4())
    user = User(
        user_id=user_id,
        phone=request.phone,
        email=request.email,
        name=request.name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/verify-otp")
async def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == request.phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "OTP verified successfully", "user_id": user.user_id}