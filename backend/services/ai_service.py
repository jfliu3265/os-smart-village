"""
AI服务层
处理所有AI相关的业务逻辑
"""

from typing import Dict, Any, List
from models.database import SessionLocal, GameSession, AIInteraction
from utils.zhipu_ai import zhipu_ai_service
import json


class AIService:
    """AI服务类"""

    @staticmethod
    async def get_hint(session_id: str, game_state: Dict[str, Any],
                      error_history: List[Dict] = None) -> str:
        """获取AI智能提示"""
        # 调用AI生成提示
        hint = zhipu_ai_service.get_hint(game_state, error_history or [])

        # 记录AI交互
        db = SessionLocal()
        try:
            ai_interaction = AIInteraction(
                session_id=session_id,
                interaction_type="hint",
                prompt=json.dumps({"game_state": game_state, "errors": error_history}),
                response=hint
            )
            db.add(ai_interaction)
            db.commit()
        except Exception as e:
            print(f"记录AI交互失败: {e}")
        finally:
            db.close()

        return hint

    @staticmethod
    async def get_feedback(session_id: str) -> Dict[str, Any]:
        """获取AI个性化反馈"""
        db = SessionLocal()
        try:
            # 获取游戏会话数据
            session = db.query(GameSession).filter(
                GameSession.session_id == session_id
            ).first()

            if not session:
                return {
                    "evaluation": "未找到游戏记录",
                    "suggestions": [],
                    "review_topics": [],
                    "next_steps": []
                }

            # 构建会话数据
            session_data = {
                "game_name": session.game_type,
                "score": session.score,
                "time_spent": 0,  # 需要计算
                "error_count": 0,  # 需要从错误表查询
                "error_types": []
            }

            # 调用AI生成反馈
            feedback = zhipu_ai_service.get_feedback(session_data)

            # 记录AI交互
            ai_interaction = AIInteraction(
                session_id=session_id,
                interaction_type="feedback",
                prompt=json.dumps(session_data),
                response=json.dumps(feedback)
            )
            db.add(ai_interaction)
            db.commit()

            return feedback

        except Exception as e:
            print(f"生成反馈失败: {e}")
            return {
                "evaluation": "反馈生成失败，请稍后再试",
                "suggestions": [],
                "review_topics": [],
                "next_steps": []
            }
        finally:
            db.close()

    @staticmethod
    async def answer_question(question: str, context: str = "") -> str:
        """字节叔AI问答"""
        answer = zhipu_ai_service.answer_question(question, context)
        return answer

    @staticmethod
    async def generate_quiz(player_level: str, topic: str) -> Dict[str, Any]:
        """AI生成练习题"""
        quiz = zhipu_ai_service.generate_quiz(player_level, topic)
        return quiz


# 全局实例
ai_service = AIService()
