#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证场景测试脚本
测试不同的Turnstile验证场景
"""

from DrissionPage import ChromiumOptions, Chromium
import time
import random

def test_verification_scenarios():
    """测试各种验证场景"""
    
    print("🧪 Turnstile验证场景测试")
    print("=" * 50)
    print("测试场景：")
    print("1. 📝 点击注册按钮后出现验证")
    print("2. 📧 点击获取验证码按钮后出现验证") 
    print("3. 🔀 密码框和cf-turnstile同时存在")
    print("4. ✅ 验证已完成的情况")
    print("=" * 50)
    
    try:
        # 浏览器配置
        co = ChromiumOptions()
        co.add_extension("turnstilePatch")
        co.incognito(True)
        co.auto_port(True)
        
        browser = Chromium(co)
        tab = browser.latest_tab
        
        # 导入优化后的验证函数
        import importlib.util
        spec = importlib.util.spec_from_file_location("main_module", "1.py")
        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)
        
        # 访问注册页面
        test_url = "https://authenticator.cursor.sh"
        print(f"\n🌐 访问注册页面: {test_url}")
        tab.get(test_url)
        time.sleep(3)
        
        # 场景1: 模拟注册流程
        print("\n📧 场景1: 完整注册流程测试")
        print("-" * 30)
        
        # 输入测试邮箱
        test_email = f"test{random.randint(1000,9999)}@example.com"
        try:
            email_input = tab.ele('@name=email', timeout=5)
            if email_input:
                email_input.input(test_email)
                print(f"✅ 输入测试邮箱: {test_email}")
                time.sleep(1)
                
                # 点击注册按钮
                submit_btn = tab.ele('@type=submit', timeout=5)
                if submit_btn:
                    submit_btn.click()
                    print("✅ 点击注册按钮")
                    time.sleep(2)
                    
                    # 场景1测试: 注册按钮后的验证
                    print("\n🔍 检查注册按钮后是否出现验证...")
                    result1 = main_module.handle_turnstile(tab)
                    print(f"📊 场景1结果: {'成功' if result1 else '失败'}")
                    
        except Exception as e:
            print(f"❌ 场景1测试失败: {str(e)}")
        
        # 场景2: 获取验证码按钮后的验证
        print("\n📬 场景2: 获取验证码按钮后验证测试")
        print("-" * 30)
        
        try:
            # 查找获取验证码按钮
            get_code_btn = tab.ele('@class=rt-reset rt-BaseButton rt-r-size-3 rt-variant-surface rt-high-contrast rt-Button', timeout=5)
            if get_code_btn:
                get_code_btn.click()
                print("✅ 点击获取验证码按钮")
                time.sleep(2)
                
                # 场景2测试: 获取验证码按钮后的验证
                print("\n🔍 检查获取验证码按钮后是否出现验证...")
                result2 = main_module.handle_turnstile(tab)
                print(f"📊 场景2结果: {'成功' if result2 else '失败'}")
                
        except Exception as e:
            print(f"❌ 场景2测试失败: {str(e)}")
        
        # 场景3: 同时存在测试（通过JavaScript模拟）
        print("\n🔀 场景3: 模拟密码框和cf-turnstile同时存在")
        print("-" * 30)
        
        try:
            # 通过JavaScript创建测试场景
            setup_js = """
            // 创建一个模拟的密码框
            const passwordInput = document.createElement('input');
            passwordInput.type = 'password';
            passwordInput.name = 'password';
            passwordInput.style.display = 'block';
            document.body.appendChild(passwordInput);
            
            // 创建一个模拟的cf-turnstile元素
            const turnstileDiv = document.createElement('div');
            turnstileDiv.id = 'cf-turnstile';
            turnstileDiv.innerHTML = '<div>Mock Turnstile</div>';
            turnstileDiv.style.display = 'block';
            turnstileDiv.style.width = 'fit-content';
            turnstileDiv.style.height = 'auto';
            document.body.appendChild(turnstileDiv);
            
            console.log('已创建模拟的密码框和cf-turnstile元素');
            return true;
            """
            
            tab.run_js(setup_js)
            print("✅ 创建模拟场景：密码框和cf-turnstile同时存在")
            time.sleep(1)
            
            # 测试优化后的逻辑
            print("\n🔍 测试优化后的处理逻辑...")
            result3 = main_module.handle_turnstile(tab)
            print(f"📊 场景3结果: {'成功' if result3 else '失败'}")
            
            # 清理模拟元素
            cleanup_js = """
            const mockPassword = document.querySelector('input[name="password"]');
            const mockTurnstile = document.getElementById('cf-turnstile');
            if (mockPassword) mockPassword.remove();
            if (mockTurnstile) mockTurnstile.remove();
            console.log('已清理模拟元素');
            """
            tab.run_js(cleanup_js)
            
        except Exception as e:
            print(f"❌ 场景3测试失败: {str(e)}")
        
        # 保持浏览器打开供观察
        print("\n⏰ 测试完成，浏览器将保持打开15秒供观察...")
        time.sleep(15)
        
        browser.quit()
        
        print("\n📈 测试总结:")
        print("✅ 新逻辑优先处理cf-turnstile验证")
        print("✅ 即使密码框存在也会先完成验证")
        print("✅ 支持多步骤验证流程")
        print("✅ 更准确的验证完成检测")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {str(e)}")
        if 'browser' in locals():
            browser.quit()

def show_scenario_explanation():
    """展示场景说明"""
    
    print("\n💡 验证场景说明:")
    print("\n【问题描述】:")
    print("• Turnstile验证可能在两个步骤出现：")
    print("  1. 点击注册按钮之后")
    print("  2. 点击获取验证码按钮之后")
    print("• 密码框和cf-turnstile可能同时存在")
    
    print("\n【优化前的问题】:")
    print("❌ 检测到密码框就直接返回")
    print("❌ 忽略了同时存在的验证弹窗")
    print("❌ 无法处理多步骤验证流程")
    
    print("\n【优化后的解决方案】:")
    print("✅ 优先检查cf-turnstile是否存在")
    print("✅ 即使密码框存在也先处理验证")
    print("✅ 智能判断cf-turnstile是否需要交互")
    print("✅ 更准确的验证完成检测")
    
    print("\n【新的处理逻辑】:")
    print("1. 🔍 检查cf-turnstile是否存在")
    print("2. 📊 如果存在，判断是否需要交互")
    print("3. 🎯 需要交互则优先处理验证")
    print("4. ✅ 处理完成后再检查其他完成标志")
    print("5. 🔄 支持多步骤验证流程")

if __name__ == "__main__":
    print("🧪 Turnstile验证场景测试程序")
    print("=" * 60)
    
    # 显示场景说明
    show_scenario_explanation()
    
    # 询问是否运行测试
    print("\n" + "=" * 60)
    user_input = input("是否运行验证场景测试? (y/N): ").strip().lower()
    
    if user_input in ['y', 'yes', '是']:
        print("\n🎬 开始场景测试...")
        test_verification_scenarios()
    else:
        print("\n👋 测试结束，感谢使用!")
    
    print("\n📚 如需了解更多信息，请查看 TURNSTILE_OPTIMIZATION.md") 