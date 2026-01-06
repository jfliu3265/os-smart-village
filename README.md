# 操作系统智慧乡村 (OS Smart Village)

> 通过寓教于乐的2D小游戏，学习操作系统核心概念

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)
[![Phaser](https://img.shields.io/badge/Phaser-3.80-orange.svg)](https://phaser.io/)

## 📖 项目简介

"操作系统智慧乡村"是一个教育游戏项目，将抽象的操作系统概念与生动的智慧乡村场景相结合。玩家通过玩6个独立的小游戏，在"字节叔"的指导下，轻松掌握操作系统的核心知识。

### 🎮 核心特色

- **寓教于乐**：用乡村生活比喻技术概念
- **AI导师**：智谱AI驱动的"字节叔"提供智能提示和个性化反馈
- **完整追踪**：详细记录学习数据，生成智能学习报告
- **六大游戏**：覆盖操作系统核心概念

## 🎯 六大游戏

| 游戏名称 | OS概念 | 智慧乡村场景 |
|---------|--------|------------|
| 🌾 农田作业调度 | 进程调度 | 农田劳作安排 |
| 🏠 仓库粮食管理 | 内存管理 | 粮仓存储分配 |
| 📁 村庄档案室 | 文件系统 | 文档组织管理 |
| 🤝 村民协作 | 进程同步 | 协同工作协调 |
| ⚖️ 资源争端调解 | 死锁处理 | 资源冲突解决 |
| 🚚 物资运输队 | I/O管理 | 物资配送调度 |

## 🏗️ 技术栈

### 前端
- **游戏引擎**: Phaser 3.80+
- **语言**: JavaScript (ES6+)
- **样式**: CSS3
- **数据可视化**: Chart.js

### 后端
- **框架**: FastAPI (Python 3.10+)
- **数据库**: SQLite + SQLAlchemy
- **AI集成**: 智谱AI GLM-4
- **API文档**: Swagger UI

## 📦 项目结构

```
os-smart-village/
├── frontend/                 # 前端项目
│   ├── index.html           # 主入口（村庄广场）
│   ├── assets/              # 资源文件
│   ├── common/              # 通用模块
│   ├── games/               # 6个游戏模块
│   └── styles/              # 样式文件
├── backend/                 # 后端项目
│   ├── app.py              # FastAPI应用入口
│   ├── api/                # API路由
│   ├── services/           # 业务逻辑
│   ├── models/             # 数据模型
│   └── utils/              # 工具函数
└── docs/                   # 文档
```

## 🚀 快速开始

### 前置要求

- Python 3.10+
- Node.js 16+ (用于前端资源管理，可选)
- 智谱AI API Key

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/jfliu3265/os-smart-village.git
cd os-smart-village
```

#### 2. 配置后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的智谱AI API Key
```

#### 3. 初始化数据库

```bash
python database/init_db.py
```

#### 4. 启动后端服务

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

后端API文档：http://localhost:8000/docs

#### 5. 启动前端

开发模式：直接用浏览器打开 `frontend/index.html`

或使用本地服务器（推荐）：

```bash
cd frontend
python -m http.server 3000
```

访问：http://localhost:3000

## 🎓 使用说明

### 玩家指南

1. **进入村庄广场**：选择想学习的游戏
2. **跟随字节叔学习**：观看概念讲解
3. **挑战关卡**：完成实际任务
4. **查看报告**：了解学习进度和建议

### 教师指南

- 查看学生的学习报告
- 分析全班的学习数据
- 根据AI建议调整教学策略

## 🤖 AI 功能

本项目集成智谱AI，提供以下智能功能：

- **智能提示**：根据玩家状态提供个性化提示
- **个性化反馈**：分析表现，给出改进建议
- **动态出题**：生成适合玩家水平的练习
- **AI问答**：向字节叔提问，获得解答

## 📊 数据与报告

系统自动记录：
- 游戏得分和星级
- 操作日志
- 错误记录
- 学习进度

生成报告：
- 在线可视化报告
- PDF 导出
- JSON/CSV 数据导出

## 🛠️ 开发指南

详见 [开发文档](docs/DEVELOPMENT.md)

### 技术架构

详见 [架构文档](docs/ARCHITECTURE.md)

### API文档

启动后端后访问：http://localhost:8000/docs

## 📝 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE)

## 🤝 贡献

欢迎贡献！请查看 [贡献指南](CONTRIBUTING.md)

## 📮 联系我们

- 项目主页：https://github.com/jfliu3265/os-smart-village
- 问题反馈：[GitHub Issues](https://github.com/jfliu3265/os-smart-village/issues)

## 🙏 致谢

- Phaser 3 - 优秀的HTML5游戏引擎
- FastAPI - 现代化的Python Web框架
- 智谱AI - 提供强大的AI能力支持

---

**让学习操作系统变得有趣！** 🎮✨
