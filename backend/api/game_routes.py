"""
游戏相关API路由
"""

from fastapi import APIRouter, Depends, HTTPException
from models.schemas import (
    GameStartRequest, GameStartResponse,
    ActionRequest, ActionResponse,
    GameEndRequest, GameEndResponse,
    ProgressResponse
)
from services.game_service import game_service

router = APIRouter()


@router.post("/start", response_model=GameStartResponse)
async def start_game(request: GameStartRequest):
    """开始新游戏"""
    try:
        session_id = await game_service.start_game(
            player_id=request.player_id,
            game_type=request.game_type,
            level=request.level
        )
        return GameStartResponse(
            session_id=session_id,
            message=f"游戏已开始，会话ID: {session_id}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/action", response_model=ActionResponse)
async def record_action(request: ActionRequest):
    """记录游戏操作"""
    try:
        success = await game_service.record_action(
            session_id=request.session_id,
            action_type=request.action_type,
            action_data=request.action_data
        )
        return ActionResponse(
            success=success,
            message="操作已记录" if success else "操作记录失败"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/end", response_model=GameEndResponse)
async def end_game(request: GameEndRequest):
    """结束游戏"""
    try:
        result = await game_service.end_game(
            session_id=request.session_id,
            score=request.score,
            stars=request.stars,
            completed=request.completed
        )
        return GameEndResponse(
            message="游戏已结束",
            final_score=result["score"],
            stars=result["stars"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/progress/{player_id}", response_model=ProgressResponse)
async def get_progress(player_id: str):
    """获取玩家进度"""
    try:
        progress = await game_service.get_progress(player_id)
        return ProgressResponse(**progress)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{player_id}")
async def get_history(player_id: str, limit: int = 10):
    """获取玩家历史记录"""
    from models.database import SessionLocal, GameSession
    from datetime import datetime

    db = SessionLocal()
    try:
        sessions = db.query(GameSession).filter(
            GameSession.player_id == player_id
        ).order_by(GameSession.start_time.desc()).limit(limit).all()

        history = []
        for session in sessions:
            history.append({
                "session_id": session.session_id,
                "game_type": session.game_type,
                "level": session.level,
                "score": session.score,
                "stars": session.stars,
                "completed": session.completed,
                "start_time": session.start_time.isoformat(),
                "end_time": session.end_time.isoformat() if session.end_time else None
            })

        return {"player_id": player_id, "history": history}

    finally:
        db.close()
