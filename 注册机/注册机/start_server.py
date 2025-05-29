'''
Author: sineom sineom@126.com
Date: 2025-05-29 14:17:02
LastEditors: sineom sineom@126.com
LastEditTime: 2025-05-29 14:22:37
FilePath: /cursorX项目/注册机/注册机/start_server.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#!/usr/bin/env python3
"""
Web邮件客户端启动脚本
"""

import sys
import subprocess
import os
import socket

def check_requirements():
    """检查是否安装了所需的依赖"""
    try:
        import flask
        import requests
        print("✅ 依赖检查通过")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_port(port):
    """检查端口是否可用"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0

def find_available_port(start_port=5001):
    """找到可用的端口"""
    port = start_port
    while port < start_port + 10:  # 尝试10个端口
        if check_port(port):
            return port
        port += 1
    return None

def main():
    print("🚀 Web邮件客户端启动器")
    print("=" * 40)
    
    # 检查依赖
    if not check_requirements():
        sys.exit(1)
    
    # 创建必要的目录
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # 查找可用端口
    port = find_available_port(5001)
    if port is None:
        print("❌ 无法找到可用端口 (尝试了5001-5010)")
        print("💡 请手动关闭占用端口的程序或稍后重试")
        sys.exit(1)
    
    print("📧 正在启动邮件客户端...")
    print(f"📡 服务器地址: http://localhost:{port}")
    print("🔄 按 Ctrl+C 停止服务器")
    
    if port != 5001:
        print(f"⚠️  注意：使用端口 {port} (5001被占用)")
    
    print("=" * 40)
    
    # 启动Flask应用
    try:
        from reset_pwd.app import app
        app.run(debug=True, host='0.0.0.0', port=port)
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("\n💡 故障排除建议:")
        print("1. 确认您在正确的目录下运行脚本")
        print("2. 检查是否已安装所有依赖: pip install -r requirements.txt")
        print("3. 确认网络连接正常")

if __name__ == "__main__":
    main() 