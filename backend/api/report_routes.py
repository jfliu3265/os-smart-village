"""
报告相关API路由
"""

from fastapi import APIRouter, HTTPException
from models.schemas import ReportGenerateRequest, ReportResponse
from services.game_service import game_service
from datetime import datetime
import uuid

router = APIRouter()


@router.post("/generate", response_model=ReportResponse)
async def generate_report(request: ReportGenerateRequest):
    """生成学习报告"""
    try:
        # 获取玩家进度数据
        progress = await game_service.get_progress(request.player_id)

        # 生成报告ID
        report_id = str(uuid.uuid4())

        # 构建报告数据
        report = ReportResponse(
            report_id=report_id,
            player_id=request.player_id,
            total_time=0,  # 需要从会话数据计算
            total_games=progress["total_games"],
            overall_score=progress["overall_progress"],
            game_breakdown=progress["games"],
            ai_suggestions=[
                "继续保持学习热情！",
                "建议多练习基础操作",
                "可以尝试更高难度的挑战"
            ],
            created_at=datetime.utcnow()
        )

        return report

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{report_id}")
async def get_report(report_id: str):
    """获取报告详情（简化版）"""
    # 在实际应用中，这里应该从数据库查询已生成的报告
    return {
        "report_id": report_id,
        "message": "报告功能正在开发中",
        "status": "coming_soon"
    }
