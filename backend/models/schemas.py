"""
Pydantic模型用于请求和响应数据验证
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


# ============ 玩家相关 ============
class PlayerCreate(BaseModel):
    player_id: str
    name: Optional[str] = None


class PlayerResponse(BaseModel):
    id: int
    player_id: str
    name: Optional[str]
    created_at: datetime
    last_played: datetime

    class Config:
        from_attributes = True


# ============ 游戏会话相关 ============
class GameStartRequest(BaseModel):
    player_id: str
    game_type: str = Field(..., description="游戏类型: process-scheduling, memory-management, etc.")
    level: str = Field(default="beginner", description="难度级别: beginner, intermediate, advanced")


class GameStartResponse(BaseModel):
    session_id: str
    message: str


class ActionRequest(BaseModel):
    session_id: str
    action_type: str
    action_data: Optional[Dict[str, Any]] = None


class ActionResponse(BaseModel):
    success: bool
    message: str


class GameEndRequest(BaseModel):
    session_id: str
    score: int
    stars: int
    completed: bool


class GameEndResponse(BaseModel):
    message: str
    final_score: int
    stars: int


class ProgressResponse(BaseModel):
    player_id: str
    total_games: int
    completed_games: int
    games: Dict[str, Dict[str, Any]]
    overall_progress: float


# ============ AI相关 ============
class HintRequest(BaseModel):
    session_id: str
    game_state: Dict[str, Any]
    error_history: Optional[List[Dict[str, Any]]] = None


class HintResponse(BaseModel):
    hint: str
    character: str = "字节叔"


class FeedbackRequest(BaseModel):
    session_id: str


class FeedbackResponse(BaseModel):
    evaluation: str
    suggestions: List[str]
    review_topics: List[str]
    next_steps: List[str]


class QuestionRequest(BaseModel):
    question: str
    context: Optional[str] = None


class QuestionResponse(BaseModel):
    answer: str
    character: str = "字节叔"


class QuizRequest(BaseModel):
    player_level: str
    topic: str


class QuizResponse(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: str


# ============ 报告相关 ============
class ReportGenerateRequest(BaseModel):
    player_id: str


class ReportResponse(BaseModel):
    report_id: str
    player_id: str
    total_time: float
    total_games: int
    overall_score: float
    game_breakdown: Dict[str, Dict[str, Any]]
    ai_suggestions: List[str]
    created_at: datetime


# ============ 通用响应 ============
class HealthResponse(BaseModel):
    status: str
    version: str


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
