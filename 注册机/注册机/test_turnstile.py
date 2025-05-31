#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Turnstile验证测试脚本
用于测试和调试Turnstile验证功能
"""

from DrissionPage import ChromiumOptions, Chromium
import time
import random

def simulate_human_behavior(tab, element):
    """模拟人类行为进行点击"""
    try:
        # 随机等待时间，模拟人类思考
        think_time = random.uniform(0.5, 2.0)
        print(f"模拟思考时间: {think_time:.1f}秒")
        time.sleep(think_time)
        
        # 尝试将元素滚动到视野中
        try:
            tab.run_js("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(random.uniform(0.3, 0.8))
        except:
            pass
        
        # 模拟鼠标悬停
        try:
            element.hover()
            time.sleep(random.uniform(0.2, 0.5))
        except:
            pass
        
        # 执行点击
        element.click()
        
        # 点击后的短暂等待
        time.sleep(random.uniform(0.3, 1.0))
        return True
        
    except Exception as e:
        print(f"模拟人类行为失败: {str(e)}")
        return False

def test_turnstile_only(url):
    """仅测试Turnstile验证功能"""
    print(f"开始测试Turnstile验证: {url}")
    
    try:
        # 浏览器配置
        co = ChromiumOptions()
        co.add_extension("turnstilePatch")
        co.set_pref('credentials_enable_service', False)
        co.set_argument('--hide-crash-restore-bubble') 
        co.incognito(True)
        co.auto_port(True)
        
        browser = Chromium(co)
        tab = browser.latest_tab
        
        # 打开测试页面
        tab.get(url)
        print("页面加载完成")
        
        # 等待页面完全加载
        time.sleep(3)
        
        # 导入handle_turnstile函数（从1.py）
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # 直接导入1.py中的函数
        import importlib.util
        spec = importlib.util.spec_from_file_location("main_module", "1.py")
        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)
        
        # 执行验证测试
        result = main_module.handle_turnstile(tab)
        
        if result:
            print("✅ Turnstile验证测试成功")
        else:
            print("❌ Turnstile验证测试失败")
        
        # 保持浏览器打开一段时间以观察结果
        print("保持浏览器打开30秒以观察结果...")
        time.sleep(30)
        
        browser.quit()
        return result
        
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
        if 'browser' in locals():
            browser.quit()
        return False

if __name__ == "__main__":
    # 测试URL（可以是任何包含Turnstile验证的页面）
    test_url = "https://authenticator.cursor.sh"
    
    print("=== Turnstile验证功能测试 ===")
    print(f"测试URL: {test_url}")
    
    success = test_turnstile_only(test_url)
    
    if success:
        print("\n🎉 测试完成：验证功能正常工作")
    else:
        print("\n⚠️  测试完成：验证功能需要进一步调试") 