"""
游戏服务层
处理游戏相关的业务逻辑
"""

from typing import Dict, Any
from models.database import SessionLocal, Player, GameSession, ActionLog, ErrorRecord
from datetime import datetime
import uuid


class GameService:
    """游戏服务类"""

    @staticmethod
    async def start_game(player_id: str, game_type: str, level: str = "beginner") -> str:
        """开始新游戏"""
        db = SessionLocal()
        try:
            # 确保玩家存在
            player = db.query(Player).filter(Player.player_id == player_id).first()
            if not player:
                player = Player(player_id=player_id, name=player_id)
                db.add(player)
                db.commit()

            # 创建游戏会话
            session_id = str(uuid.uuid4())
            game_session = GameSession(
                session_id=session_id,
                player_id=player_id,
                game_type=game_type,
                level=level
            )
            db.add(game_session)

            # 更新玩家最后游戏时间
            player.last_played = datetime.utcnow()

            db.commit()

            return session_id

        except Exception as e:
            db.rollback()
            print(f"开始游戏失败: {e}")
            raise e
        finally:
            db.close()

    @staticmethod
    async def record_action(session_id: str, action_type: str,
                           action_data: Dict[str, Any] = None) -> bool:
        """记录游戏操作"""
        db = SessionLocal()
        try:
            action_log = ActionLog(
                session_id=session_id,
                action_type=action_type,
                action_data=action_data
            )
            db.add(action_log)
            db.commit()
            return True

        except Exception as e:
            print(f"记录操作失败: {e}")
            return False
        finally:
            db.close()

    @staticmethod
    async def end_game(session_id: str, score: int, stars: int, completed: bool) -> Dict[str, Any]:
        """结束游戏"""
        db = SessionLocal()
        try:
            game_session = db.query(GameSession).filter(
                GameSession.session_id == session_id
            ).first()

            if not game_session:
                raise ValueError("游戏会话不存在")

            game_session.end_time = datetime.utcnow()
            game_session.score = score
            game_session.stars = stars
            game_session.completed = completed

            db.commit()

            return {
                "session_id": session_id,
                "score": score,
                "stars": stars,
                "completed": completed
            }

        except Exception as e:
            db.rollback()
            print(f"结束游戏失败: {e}")
            raise e
        finally:
            db.close()

    @staticmethod
    async def get_progress(player_id: str) -> Dict[str, Any]:
        """获取玩家进度"""
        db = SessionLocal()
        try:
            # 获取所有游戏会话
            sessions = db.query(GameSession).filter(
                GameSession.player_id == player_id
            ).all()

            # 统计数据
            total_games = len(set(s.game_type for s in sessions))
            completed_games = len([s for s in sessions if s.completed])

            # 按游戏类型分组
            games_data = {}
            for session in sessions:
                if session.game_type not in games_data:
                    games_data[session.game_type] = {
                        "attempts": 0,
                        "best_score": 0,
                        "best_stars": 0,
                        "completed": False
                    }

                games_data[session.game_type]["attempts"] += 1
                if session.score:
                    games_data[session.game_type]["best_score"] = max(
                        games_data[session.game_type]["best_score"],
                        session.score
                    )
                if session.stars:
                    games_data[session.game_type]["best_stars"] = max(
                        games_data[session.game_type]["best_stars"],
                        session.stars
                    )
                if session.completed:
                    games_data[session.game_type]["completed"] = True

            overall_progress = (completed_games / 6) * 100 if total_games > 0 else 0

            return {
                "player_id": player_id,
                "total_games": total_games,
                "completed_games": completed_games,
                "games": games_data,
                "overall_progress": round(overall_progress, 2)
            }

        finally:
            db.close()


# 全局实例
game_service = GameService()
