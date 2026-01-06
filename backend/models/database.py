"""
数据库模型定义
使用SQLAlchemy ORM
"""

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database/os_village.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Player(Base):
    """玩家信息表"""
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_played = Column(DateTime, default=datetime.utcnow)


class GameSession(Base):
    """游戏会话表"""
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(50), unique=True, nullable=False, index=True)
    player_id = Column(String(50), nullable=False)
    game_type = Column(String(50), nullable=False)  # process-scheduling, memory-management, etc.
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    score = Column(Integer, nullable=True)
    stars = Column(Integer, nullable=True)
    completed = Column(Boolean, default=False)
    level = Column(String(20), default="beginner")  # beginner, intermediate, advanced


class ActionLog(Base):
    """操作日志表"""
    __tablename__ = "action_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(50), nullable=False, index=True)
    action_type = Column(String(50), nullable=False)  # start, move, click, error, hint, etc.
    action_data = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class ErrorRecord(Base):
    """错误记录表"""
    __tablename__ = "errors"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(50), nullable=False, index=True)
    error_type = Column(String(100), nullable=False)
    error_context = Column(JSON, nullable=True)
    count = Column(Integer, default=1)
    timestamp = Column(DateTime, default=datetime.utcnow)


class AIInteraction(Base):
    """AI交互记录表"""
    __tablename__ = "ai_interactions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(50), nullable=False)
    interaction_type = Column(String(50), nullable=False)  # hint, feedback, question, quiz
    prompt = Column(String(1000))
    response = Column(String(2000))
    tokens_used = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)


def init_db():
    """初始化数据库"""
    import os
    db_path = os.path.join(os.path.dirname(__file__), "..", "database")
    os.makedirs(db_path, exist_ok=True)

    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
