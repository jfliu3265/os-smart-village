"""
数据库初始化脚本
"""

import sys
import os

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import init_db


if __name__ == "__main__":
    print("初始化数据库...")
    init_db()
    print("数据库初始化完成！")
