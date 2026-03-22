from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class RegistrationStatus(str, Enum):
    UNREGISTERED = "unregistered"
    OTP_PENDING = "otp_pending"
    REGISTERED = "registered"

class WalletStatus(str, Enum):
    FREE_CREDIT = "free_credit"
    EXHAUSTED = "exhausted"
    FUNDED = "funded"

class IntentMode(str, Enum):
    CONCERN = "concern"
    MQ_DISCOVERY = "mq_discovery"
    PORTFOLIO_REVIEW = "portfolio_review"
    DIY_INVESTING = "diy_investing"
    MANAGED_PORTFOLIO = "managed_portfolio"
    NET_WORTH_PLANNING = "net_worth_planning"
    CASH_FLOW = "cash_flow"
    EXPERT_CALL = "expert_call"

class MQStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., regex=r"^[0-9]{10}$")
    email: EmailStr

class VerifyOTPRequest(BaseModel):
    phone: str = Field(..., regex=r"^[0-9]{10}$")
    otp: str = Field(..., min_length=6, max_length=6)

class ChatMessage(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    language: str = Field(default="english", regex=r"^(english|hindi|kannada|tamil|telugu|marathi)$")
    user_id: Optional[str] = None

class UserResponse(BaseModel):
    user_id: str
    phone: str
    email: str
    name: str
    registration_status: RegistrationStatus
    created_at: datetime

class UserStateResponse(BaseModel):
    user_id: str
    registration: RegistrationStatus
    wallet: WalletStatus
    language: str
    corpus_band: Optional[str]
    resident_status: Optional[str]
    intent: Optional[IntentMode]
    mq_status: MQStatus
    investment_upload: bool
    expert_interest: Optional[bool]
    escalation_flag: Optional[str]

class ChatResponse(BaseModel):
    message_id: str
    content: str
    language: str
    timestamp: datetime
    user_state: UserStateResponse

class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    redis: str
    gemini_api: str

class ErrorResponse(BaseModel):
    error: str
    detail: str
    code: int