/**
 * OS Smart Village - API客户端
 * 封装所有后端API调用
 */

class APIClient {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
        this.playerID = this.getPlayerID();
    }

    /**
     * 获取或生成玩家ID
     */
    getPlayerID() {
        let playerID = localStorage.getItem('os_village_player_id');
        if (!playerID) {
            playerID = 'player_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('os_village_player_id', playerID);
        }
        return playerID;
    }

    /**
     * 通用请求方法
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        try {
            const response = await fetch(url, { ...defaultOptions, ...options });
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || '请求失败');
            }

            return data;
        } catch (error) {
            console.error('API请求失败:', error);
            throw error;
        }
    }

    /**
     * 开始游戏
     */
    async startGame(gameType, level = 'beginner') {
        return this.request('/api/game/start', {
            method: 'POST',
            body: JSON.stringify({
                player_id: this.playerID,
                game_type: gameType,
                level: level
            })
        });
    }

    /**
     * 记录操作
     */
    async recordAction(sessionID, actionType, actionData = null) {
        return this.request('/api/game/action', {
            method: 'POST',
            body: JSON.stringify({
                session_id: sessionID,
                action_type: actionType,
                action_data: actionData
            })
        });
    }

    /**
     * 结束游戏
     */
    async endGame(sessionID, score, stars, completed) {
        return this.request('/api/game/end', {
            method: 'POST',
            body: JSON.stringify({
                session_id: sessionID,
                score: score,
                stars: stars,
                completed: completed
            })
        });
    }

    /**
     * 获取玩家进度
     */
    async getProgress() {
        return this.request(`/api/game/progress/${this.playerID}`);
    }

    /**
     * 获取历史记录
     */
    async getHistory(limit = 10) {
        return this.request(`/api/game/history/${this.playerID}?limit=${limit}`);
    }

    /**
     * 获取AI提示
     */
    async getHint(sessionID, gameState, errorHistory = null) {
        return this.request('/api/ai/hint', {
            method: 'POST',
            body: JSON.stringify({
                session_id: sessionID,
                game_state: gameState,
                error_history: errorHistory
            })
        });
    }

    /**
     * 获取AI反馈
     */
    async getFeedback(sessionID) {
        return this.request('/api/ai/feedback', {
            method: 'POST',
            body: JSON.stringify({
                session_id: sessionID
            })
        });
    }

    /**
     * 向字节叔提问
     */
    async askQuestion(question, context = '') {
        return this.request('/api/ai/question', {
            method: 'POST',
            body: JSON.stringify({
                question: question,
                context: context
            })
        });
    }

    /**
     * 生成练习题
     */
    async generateQuiz(playerLevel, topic) {
        return this.request('/api/ai/generate-quiz', {
            method: 'POST',
            body: JSON.stringify({
                player_level: playerLevel,
                topic: topic
            })
        });
    }

    /**
     * 生成学习报告
     */
    async generateReport() {
        return this.request('/api/report/generate', {
            method: 'POST',
            body: JSON.stringify({
                player_id: this.playerID
            })
        });
    }
}

// 创建全局实例
const apiClient = new APIClient();

// 导出到全局
if (typeof window !== 'undefined') {
    window.OS_VILLAGE_API = apiClient;
}
