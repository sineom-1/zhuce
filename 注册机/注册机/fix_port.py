#!/usr/bin/env python3
"""
端口冲突修复脚本 - 检查端口占用并提供解决方案
"""

import socket
import subprocess
import sys
import platform

def check_port(port):
    """检查端口是否被占用"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0  # True表示端口被占用

def get_port_process(port):
    """获取占用端口的进程信息"""
    try:
        if platform.system() == "Darwin":  # macOS
            result = subprocess.run(['lsof', '-i', f':{port}'], 
                                  capture_output=True, text=True)
            return result.stdout
        elif platform.system() == "Linux":
            result = subprocess.run(['netstat', '-tlnp'], 
                                  capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if f':{port} ' in line:
                    return line
        else:  # Windows
            result = subprocess.run(['netstat', '-ano'], 
                                  capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if f':{port} ' in line:
                    return line
    except:
        pass
    return None

def check_airplay_service():
    """检查macOS AirPlay服务状态"""
    if platform.system() != "Darwin":
        return False
    
    try:
        # 检查AirPlay服务是否在运行
        result = subprocess.run(['pgrep', '-f', 'AirPlayXPCHelper'], 
                              capture_output=True, text=True)
        return len(result.stdout.strip()) > 0
    except:
        return False

def main():
    print("🔧 端口冲突检查和修复工具")
    print("=" * 40)
    
    # 检查常用端口
    ports_to_check = [5000, 5001, 5002, 5003]
    occupied_ports = []
    
    for port in ports_to_check:
        if check_port(port):
            occupied_ports.append(port)
            print(f"❌ 端口 {port} 被占用")
            
            process_info = get_port_process(port)
            if process_info:
                print(f"   进程信息: {process_info.strip()}")
        else:
            print(f"✅ 端口 {port} 可用")
    
    if not occupied_ports:
        print("\n🎉 所有端口都可用！可以正常启动服务器")
        return
    
    print(f"\n⚠️  发现 {len(occupied_ports)} 个端口被占用")
    
    # 特别检查5000端口（macOS AirPlay）
    if 5000 in occupied_ports:
        print("\n🍎 检测到macOS环境，端口5000可能被AirPlay占用")
        
        if check_airplay_service():
            print("✅ 确认AirPlay服务正在运行")
            print("\n💡 解决方案：")
            print("1. 打开 '系统偏好设置' -> '共享'")
            print("2. 取消勾选 'AirPlay接收器'")
            print("3. 或者使用其他端口 (推荐使用 5001)")
        else:
            print("❓ AirPlay服务状态未知")
    
    # 推荐可用端口
    available_ports = [p for p in ports_to_check if p not in occupied_ports]
    if available_ports:
        print(f"\n🚀 推荐使用端口: {available_ports[0]}")
        print(f"   启动命令: python app.py (服务器会自动选择可用端口)")
    
    print("\n🛠️  自动修复建议:")
    print("1. 使用智能启动脚本: python run.py")
    print("2. 使用端口检测启动: python start_server.py")
    print("3. 手动关闭占用端口的服务")

if __name__ == "__main__":
    main() 