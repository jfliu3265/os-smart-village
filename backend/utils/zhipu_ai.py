"""
智谱AI集成工具
"""

import os
from typing import Dict, Any, List
from zhipuai import ZhipuAI
from dotenv import load_dotenv

load_dotenv()


class ZhipuAIService:
    """智谱AI服务封装"""

    def __init__(self):
        self.api_key = os.getenv("ZHIPUAI_API_KEY")
        self.model = os.getenv("ZHIPUAI_MODEL", "glm-4")
        self.client = ZhipuAI(api_key=self.api_key) if self.api_key else None

    def _call_ai(self, prompt: str, temperature: float = 0.7) -> str:
        """调用智谱AI"""
        if not self.client:
            return "AI服务未配置，请设置ZHIPUAI_API_KEY环境变量"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"AI调用失败: {str(e)}")
            return "AI暂时无法响应，请稍后再试"

    def get_hint(self, game_state: Dict[str, Any], error_history: List[Dict]) -> str:
        """生成智能提示"""
        prompt = f"""你是字节叔，一位智慧的乡村管理员和操作系统导师。
玩家正在学习{game_state.get('topic', '操作系统')}，目前在{game_state.get('game_stage', '某个关卡')}阶段遇到了困难。

玩家当前状态：
{game_state}

错误历史：
{error_history if error_history else '无'}

请用乡村生活的比喻，给出一个简洁友好的提示（不超过50字），
帮助玩家理解概念，但不要直接告诉答案。保持字节叔亲切、幽默的风格。"""

        return self._call_ai(prompt, temperature=0.8)

    def get_feedback(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成个性化反馈"""
        prompt = f"""你是字节叔，请分析玩家在{session_data.get('game_name', '游戏')}中的表现。

游戏数据：
- 得分：{session_data.get('score', 0)}
- 完成时间：{session_data.get('time_spent', 0)}秒
- 错误次数：{session_data.get('error_count', 0)}
- 主要错误类型：{session_data.get('error_types', '无')}

请给出（用JSON格式返回）：
{{
  "evaluation": "表现评价（鼓励为主，30字以内）",
  "suggestions": ["改进建议1", "改进建议2", "改进建议3"],
  "review_topics": ["复习知识点1", "复习知识点2"],
  "next_steps": ["下一步学习建议1", "下一步学习建议2"]
}}

语气要亲切鼓励，用乡村生活比喻。"""

        response = self._call_ai(prompt, temperature=0.7)
        # 尝试解析JSON响应
        try:
            import json
            return json.loads(response)
        except:
            # 如果AI返回的不是JSON，返回默认结构
            return {
                "evaluation": "表现不错，继续努力！",
                "suggestions": ["多练习基本操作", "注意时间管理"],
                "review_topics": ["基本概念"],
                "next_steps": ["继续下一关"]
            }

    def answer_question(self, question: str, context: str = "") -> str:
        """回答玩家问题"""
        prompt = f"""你是字节叔，智慧乡村的管理员兼操作系统导师。
玩家提出了关于操作系统的问题："{question}"。
当前上下文：{context if context else '玩家正在学习操作系统'}。

请用乡村生活的比喻解释这个概念，语言要通俗易懂，
保持字节叔亲切、幽默、知识渊博的人设。
回答不超过100字。"""

        return self._call_ai(prompt, temperature=0.8)

    def generate_quiz(self, player_level: str, topic: str) -> Dict[str, Any]:
        """生成练习题"""
        prompt = f"""你是字节叔，需要为玩家生成一道关于{topic}的练习题。
玩家当前水平：{player_level}（初级/中级/高级）

要求：
1. 题目要贴合智慧乡村场景
2. 难度适合玩家当前水平
3. 包含题目、选项、正确答案、解析
4. 用JSON格式返回

格式：
{{
  "question": "题目",
  "options": ["选项A", "选项B", "选项C", "选项D"],
  "correct_answer": "A",
  "explanation": "解析"
}}

注意：只返回JSON，不要有其他文字。"""

        response = self._call_ai(prompt, temperature=0.9)
        try:
            import json
            return json.loads(response)
        except:
            # 返回一个默认题目
            return {
                "question": f"在智慧乡村中，{topic}类似于什么？",
                "options": ["选项A", "选项B", "选项C", "选项D"],
                "correct_answer": "A",
                "explanation": "这是基础知识，请认真学习！"
            }


# 全局实例
zhipu_ai_service = ZhipuAIService()
