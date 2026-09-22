import time

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.cache.redis_client import get_cached_answer, set_cached_answer
from app.database import get_db
from app.llm.service import ask_llm
from app.models import ChatMessage


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    question: str


@router.post("")
def chat(
    request: ChatRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    start_time = time.perf_counter()

    cached_answer = get_cached_answer(request.question)

    if cached_answer:
        latency = round(time.perf_counter() - start_time, 3)

        chat_message = ChatMessage(
            username=current_user["username"],
            question=request.question,
            answer=cached_answer,
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
            latency_seconds=latency,
        )

        db.add(chat_message)
        db.commit()
        db.refresh(chat_message)

        return {
            "question": request.question,
            "answer": cached_answer,
            "username": current_user["username"],
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "latency_seconds": latency,
            "cache": "HIT",
        }

    result = ask_llm(request.question)

    latency = round(time.perf_counter() - start_time, 3)

    set_cached_answer(
        request.question,
        result["answer"],
        ttl=3600,
    )

    chat_message = ChatMessage(
        username=current_user["username"],
        question=request.question,
        answer=result["answer"],
        input_tokens=result["input_tokens"],
        output_tokens=result["output_tokens"],
        total_tokens=result["total_tokens"],
        latency_seconds=latency,
    )

    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)

    return {
        "question": request.question,
        "answer": result["answer"],
        "username": current_user["username"],
        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"],
        "total_tokens": result["total_tokens"],
        "latency_seconds": latency,
        "cache": "MISS",
    }
