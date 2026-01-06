"""
OS Smart Village - FastAPI Application
智慧乡村后端主应用
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from dotenv import load_dotenv

from api import game_routes, ai_routes, report_routes

# 加载环境变量
load_dotenv()

# 创建FastAPI应用
app = FastAPI(
    title="OS Smart Village API",
    description="操作系统智慧乡村 - 后端API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
origins = os.getenv("CORS_ORIGINS", '["http://localhost:3000"]').replace('"', "'").split(', ')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(game_routes.router, prefix="/api/game", tags=["Game"])
app.include_router(ai_routes.router, prefix="/api/ai", tags=["AI"])
app.include_router(report_routes.router, prefix="/api/report", tags=["Report"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Welcome to OS Smart Village API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host=host, port=port, reload=True)
