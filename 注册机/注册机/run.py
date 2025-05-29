#!/usr/bin/env python3
"""
智能启动脚本 - 自动找到项目目录并启动邮件客户端
"""

import os
import sys
import subprocess

def find_project_dir():
    """查找项目目录"""
    current_dir = os.getcwd()
    
    # 检查当前目录是否就是项目目录
    if os.path.exists('app.py') and os.path.exists('email_service.py'):
        return current_dir
    
    # 检查是否在上级目录
    possible_paths = [
        '注册机/注册机',
        './注册机/注册机',
        '../注册机/注册机',
    ]
    
    for path in possible_paths:
        full_path = os.path.join(current_dir, path)
        if os.path.exists(os.path.join(full_path, 'app.py')):
            return full_path
    
    return None

def main():
    print("🔍 正在查找Web邮件客户端项目...")
    
    project_dir = find_project_dir()
    
    if project_dir is None:
        print("❌ 找不到项目文件")
        print("💡 请确保您在正确的目录下，或者项目文件存在")
        print("📁 项目应包含以下文件：")
        print("   - app.py")
        print("   - email_service.py")
        print("   - templates/")
        sys.exit(1)
    
    print(f"✅ 找到项目目录: {project_dir}")
    
    # 切换到项目目录
    os.chdir(project_dir)
    print(f"📂 已切换到目录: {os.getcwd()}")
    
    # 启动服务器
    try:
        print("🚀 启动邮件客户端...")
        subprocess.run([sys.executable, 'start_server.py'])
    except KeyboardInterrupt:
        print("\n👋 启动已取消")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main() 