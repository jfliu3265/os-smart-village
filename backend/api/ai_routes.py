"""
AI相关API路由
"""

from fastapi import APIRouter, HTTPException
from models.schemas import (
    HintRequest, HintResponse,
    FeedbackRequest, FeedbackResponse,
    QuestionRequest, QuestionResponse,
    QuizRequest, QuizResponse
)
from services.ai_service import ai_service

router = APIRouter()


@router.post("/hint", response_model=HintResponse)
async def get_hint(request: HintRequest):
    """获取AI智能提示"""
    try:
        hint = await ai_service.get_hint(
            session_id=request.session_id,
            game_state=request.game_state,
            error_history=request.error_history
        )
        return HintResponse(hint=hint)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/feedback", response_model=FeedbackResponse)
async def get_feedback(request: FeedbackRequest):
    """获取AI个性化反馈"""
    try:
        feedback = await ai_service.get_feedback(session_id=request.session_id)
        return FeedbackResponse(**feedback)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/question", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """向字节叔提问"""
    try:
        answer = await ai_service.answer_question(
            question=request.question,
            context=request.context
        )
        return QuestionResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-quiz", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    """AI生成练习题"""
    try:
        quiz = await ai_service.generate_quiz(
            player_level=request.player_level,
            topic=request.topic
        )
        return QuizResponse(**quiz)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
