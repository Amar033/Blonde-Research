from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict,Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.ai_service import ai_service
from app.services.search_service import search_service
from app.models.chat import ChatMessage
from app.models.user import User
import json

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    enable_search: bool = False

@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Streaming chat endpoint
    """
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Build messages array
    messages = []
    
    # Add system prompt if provided
    if request.system_prompt:
        messages.append({"role": "system", "content": request.system_prompt})
    
    # Web search if enabled
    sources = []
    if request.enable_search:
        search_results = await search_service.search(request.message)
        if search_results:
            sources = search_results
            search_context = search_service.format_sources(search_results)
            messages.append({
                "role": "system",
                "content": f"Use the following web search results to answer the user's question:\n{search_context}"
            })
    
    # Add user message
    messages.append({"role": "user", "content": request.message})
    
    # Save user message to DB
    user_msg = ChatMessage(
        user_id=user.id,
        role="user",
        content=request.message,
        model="user-input"
    )
    db.add(user_msg)
    db.commit()
    
    # Stream AI response
    async def generate():
        full_response = ""
        try:
            async for chunk in ai_service.chat_completion(
                messages=messages,
                stream=True,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            ):
                full_response += chunk
                # Send chunk as Server-Sent Event
                yield f"data: {json.dumps({'type': 'content', 'content': chunk})}\n\n"
            
            # Send sources if any
            if sources:
                yield f"data: {json.dumps({'type': 'sources', 'sources': sources})}\n\n"
            
            # Save assistant response to DB
            assistant_msg = ChatMessage(
                user_id=user.id,
                role="assistant",
                content=full_response,
                sources=json.dumps(sources) if sources else None,
                model="llama-3.3-70b",
                tokens_used=len(full_response.split())  # Rough estimate
            )
            db.add(assistant_msg)
            db.commit()
            
            # Send done signal
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@router.get("/history")
async def get_history(
    limit: int = 50,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get chat history for current user
    """
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == user.id
    ).order_by(ChatMessage.created_at.desc()).limit(limit).all()
    
    return [{
        "role": msg.role,
        "content": msg.content,
        "sources": json.loads(msg.sources) if msg.sources else None,
        "created_at": msg.created_at
    } for msg in reversed(messages)]