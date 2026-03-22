from sqlalchemy import create_engine, Column, String, DateTime, Integer, Boolean, JSON, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import logging

from app.config import settings
from app.models import RegistrationStatus, WalletStatus, MQStatus

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(String, primary_key=True, index=True)
    phone = Column(String(10), unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    language = Column(String, default="english")
    registration_status = Column(SQLEnum(RegistrationStatus), default=RegistrationStatus.UNREGISTERED)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    conversations = relationship("Conversation", back_populates="user")
    user_state = relationship("UserState", uselist=False, back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")

class UserState(Base):
    __tablename__ = "user_state"
    
    user_id = Column(String, ForeignKey("users.user_id"), primary_key=True)
    registration = Column(SQLEnum(RegistrationStatus), default=RegistrationStatus.UNREGISTERED)
    wallet = Column(SQLEnum(WalletStatus), default=WalletStatus.FREE_CREDIT)
    language = Column(String, default="english")
    corpus_band = Column(String, nullable=True)
    resident_status = Column(String, nullable=True)
    intent = Column(String, nullable=True)
    mq_status = Column(SQLEnum(MQStatus), default=MQStatus.NOT_STARTED)
    investment_upload = Column(Boolean, default=False)
    expert_interest = Column(Boolean, nullable=True)
    escalation_flag = Column(String, nullable=True)
    conversation_count = Column(Integer, default=0)
    last_message_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="user_state")

class Conversation(Base):
    __tablename__ = "conversations"
    
    message_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), index=True)
    content = Column(Text, nullable=False)
    role = Column(String)
    language = Column(String, default="english")
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    user = relationship("User", back_populates="conversations")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    log_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), index=True)
    action = Column(String, nullable=False)
    tool_name = Column(String, nullable=True)
    result = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    user = relationship("User", back_populates="audit_logs")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully")