# 部署文档 (Deployment Guide)

本文档介绍如何部署"操作系统智慧乡村"项目。

## 目录

- [开发环境部署](#开发环境部署)
- [生产环境部署](#生产环境部署)
- [Docker部署](#docker部署)
- [云平台部署](#云平台部署)
- [常见问题](#常见问题)

---

## 开发环境部署

### 前置要求

- Python 3.10 或更高版本
- Node.js 16+ (可选，用于前端开发)
- 智谱AI API Key

### 步骤1: 克隆项目

```bash
git clone https://github.com/jfliu3265/os-smart-village.git
cd os-smart-village
```

### 步骤2: 配置后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
```

编辑 `.env` 文件，设置你的智谱AI API Key：

```env
ZHIPUAI_API_KEY=your_actual_api_key_here
ZHIPUAI_MODEL=glm-4
DATABASE_URL=sqlite:///database/os_village.db
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### 步骤3: 初始化数据库

```bash
python database/init_db.py
```

### 步骤4: 启动后端服务

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

后端将运行在: http://localhost:8000

API文档: http://localhost:8000/docs

### 步骤5: 启动前端

打开新终端：

```bash
cd frontend

# 方法1: 使用Python简单HTTP服务器
python -m http.server 3000

# 方法2: 使用Node.js http-server
npx http-server -p 3000
```

前端将运行在: http://localhost:3000

---

## 生产环境部署

### 使用Gunicorn (推荐)

#### 步骤1: 安装Gunicorn

```bash
pip install gunicorn
```

#### 步骤2: 配置环境变量

确保 `.env` 文件中的 `DEBUG=False`：

```env
DEBUG=False
HOST=0.0.0.0
PORT=8000
```

#### 步骤3: 启动服务

```bash
cd backend
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

参数说明：
- `-w 4`: 4个工作进程
- `-k uvicorn.workers.UvicornWorker`: 使用Uvicorn工作器
- `--bind 0.0.0.0:8000`: 绑定地址和端口

#### 步骤4: 使用Nginx反向代理

创建Nginx配置文件 `/etc/nginx/sites-available/os-smart-village`:

```nginx
# 后端API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

# 前端
server {
    listen 80;
    server_name www.yourdomain.com;
    root /path/to/os-smart-village/frontend;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/os-smart-village /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Docker部署

### 构建镜像

#### 后端Dockerfile

创建 `backend/Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 前端Dockerfile

创建 `frontend/Dockerfile`:

```dockerfile
FROM nginx:alpine

COPY . /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
```

### Docker Compose

创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - ZHIPUAI_API_KEY=${ZHIPUAI_API_KEY}
      - DATABASE_URL=sqlite:///database/os_village.db
    volumes:
      - ./backend/database:/app/database
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

### 启动服务

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## 使用Systemd管理服务

创建服务文件 `/etc/systemd/system/os-smart-village.service`:

```ini
[Unit]
Description=OS Smart Village Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/os-smart-village/backend
Environment="PATH=/path/to/os-smart-village/backend/venv/bin"
ExecStart=/path/to/os-smart-village/backend/venv/bin/gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable os-smart-village
sudo systemctl start os-smart-village
sudo systemctl status os-smart-village
```

---

## 环境变量说明

| 变量名 | 说明 | 默认值 |
|-------|------|--------|
| `ZHIPUAI_API_KEY` | 智谱AI API密钥 | 必填 |
| `ZHIPUAI_MODEL` | 使用的AI模型 | glm-4 |
| `DATABASE_URL` | 数据库连接字符串 | sqlite:///database/os_village.db |
| `HOST` | 服务器地址 | 0.0.0.0 |
| `PORT` | 服务器端口 | 8000 |
| `DEBUG` | 调试模式 | True |
| `CORS_ORIGINS` | 允许的跨域来源 | ["http://localhost:3000"] |

---

## 常见问题

### Q1: 数据库初始化失败

**问题**: 运行 `init_db.py` 时报错

**解决方案**:
```bash
# 确保database目录存在
mkdir -p backend/database

# 检查文件权限
chmod +x backend/database/init_db.py

# 手动创建数据库
python -c "from models.database import init_db; init_db()"
```

### Q2: AI调用失败

**问题**: AI功能无法使用

**解决方案**:
1. 检查API Key是否正确配置
2. 确认API Key有足够的额度
3. 检查网络连接是否正常
4. 查看后端日志: `docker-compose logs backend`

### Q3: 前端无法连接后端

**问题**: 前端调用API时出现CORS错误

**解决方案**:
1. 检查 `.env` 中的 `CORS_ORIGINS` 配置
2. 确保前端URL在允许列表中
3. 检查后端是否正常运行

### Q4: 游戏运行缓慢

**问题**: 游戏加载或运行卡顿

**解决方案**:
1. 检查网络连接
2. 清除浏览器缓存
3. 减少同时运行的进程数量
4. 检查服务器资源使用情况

---

## 性能优化建议

### 后端优化

1. **使用缓存**: 为常用数据添加Redis缓存
2. **数据库索引**: 为常用查询字段添加索引
3. **连接池**: 配置数据库连接池
4. **异步处理**: 使用异步路由提高并发能力

### 前端优化

1. **资源压缩**: 使用gzip压缩静态资源
2. **CDN加速**: 将静态资源托管到CDN
3. **懒加载**: 游戏资源按需加载
4. **代码分割**: 使用Webpack进行代码分割

---

## 监控和日志

### 日志配置

后端使用Python logging模块：

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### 监控指标

- API响应时间
- AI调用成功率
- 数据库查询性能
- 服务器资源使用率

---

## 安全建议

1. **API密钥保护**: 不要在代码中硬编码API密钥
2. **输入验证**: 使用Pydantic验证所有用户输入
3. **SQL注入防护**: 使用ORM防止SQL注入
4. **HTTPS**: 生产环境必须使用HTTPS
5. **速率限制**: 添加API速率限制防止滥用

---

## 备份策略

### 数据库备份

```bash
# 手动备份SQLite数据库
cp backend/database/os_village.db backup/os_village_$(date +%Y%m%d).db

# 使用cron定时备份
0 2 * * * cp /path/to/os_village.db /backup/os_village_$(date +\%Y\%m\%d).db
```

### 配置文件备份

定期备份 `.env` 文件和Nginx配置。

---

## 云平台部署

### 部署到 Heroku

#### 1. 准备工作

```bash
# 安装 Heroku CLI
# macOS: brew tap heroku/brew && brew install heroku
# Windows: 下载安装器 https://devcenter.heroku.com/articles/heroku-cli

# 登录 Heroku
heroku login
```

#### 2. 创建应用

```bash
# 创建应用
heroku create os-smart-village

# 添加 PostgreSQL 数据库（可选，也可以用 SQLite）
heroku addons:create heroku-postgresql:mini
```

#### 3. 配置环境变量

```bash
# 设置 API Key
heroku config:set ZHIPUAI_API_KEY=your_api_key_here

# 设置其他配置
heroku config:set ZHIPUAI_MODEL=glm-4
heroku config:set DEBUG=False
```

#### 4. 部署

```bash
# 推送代码
git push heroku main

# 查看日志
heroku logs --tail
```

### 部署到 Railway

#### 1. 访问 Railway

https://railway.app/

#### 2. 新建项目

- 连接 GitHub 仓库
- 选择 `os-smart-village`
- Railway 会自动检测项目类型

#### 3. 配置变量

在 Railway 控制台添加环境变量：
```
ZHIPUAI_API_KEY=your_api_key
ZHIPUAI_MODEL=glm-4
DATABASE_URL=postgresql://...
```

#### 4. 部署

点击 "Deploy" 按钮，Railway 会自动部署。

### 部署到腾讯云/阿里云

#### 使用云服务器

```bash
# 1. 购买云服务器（推荐配置：2核4G）
# 2. 登录服务器
ssh root@your_server_ip

# 3. 安装环境
yum install -y python3 python3-pip nginx

# 4. 克隆代码
git clone https://github.com/jfliu3265/os-smart-village.git
cd os-smart-village

# 5. 按照开发环境步骤部署后端和前端
# 6. 配置 Nginx 反向代理
```

#### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your_domain.com;

    # 前端
    location / {
        root /path/to/os-smart-village/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 更新和升级

### 更新代码

```bash
git pull origin main
cd backend
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### 数据库迁移

```bash
python database/migrate.py
```

### 重启服务

```bash
sudo systemctl restart os-smart-village
# 或
docker-compose down
docker-compose up -d
```

---

## 联系支持

如果遇到问题，请：
1. 查看本文档的常见问题部分
2. 检查GitHub Issues: https://github.com/jfliu3265/os-smart-village/issues
3. 提交新的Issue并提供详细信息

---

**祝部署顺利！** 🚀
