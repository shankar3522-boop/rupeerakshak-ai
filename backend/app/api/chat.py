from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.models import ChatMessage, ChatResponse
from app.database import get_db, Conversation, User, UserState
from app.services.gemini_orchestrator import GeminiOrchestrator
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
gemini_orchestrator = GeminiOrchestrator()

@router.post("/")
async def chat(message: ChatMessage, db: Session = Depends(get_db)):
    if not message.user_id:
        raise ValueError("user_id is required")
    
    user = db.query(User).filter(User.user_id == message.user_id).first()
    if not user:
        raise ValueError("User not found")
    
    response = await gemini_orchestrator.generate_response(message.content, message.language)
    
    message_id = str(uuid.uuid4())
    conversation = Conversation(
        message_id=message_id,
        user_id=message.user_id,
        content=message.content,
        role="user",
        language=message.language
    )
    db.add(conversation)
    
    response_message = Conversation(
        message_id=str(uuid.uuid4()),
        user_id=message.user_id,
        content=response,
        role="assistant",
        language=message.language
    )
    db.add(response_message)
    db.commit()
    
    user_state = db.query(UserState).filter(UserState.user_id == message.user_id).first()
    
    return ChatResponse(
        message_id=message_id,
        content=response,
        language=message.language,
        timestamp=datetime.utcnow(),
        user_state=user_state
    )

@router.websocket("/ws/{user_id}/{session_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, session_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = await gemini_orchestrator.generate_response(data, "english")
            await websocket.send_text(response)
    except WebSocketDisconnect:
        logger.info(f"Client {user_id} disconnected")