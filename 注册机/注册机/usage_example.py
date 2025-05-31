#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Turnstile验证优化后的使用示例
展示新的优先级处理逻辑
"""

from DrissionPage import ChromiumOptions, Chromium
import time

def demo_turnstile_optimization():
    """演示优化后的Turnstile验证流程"""
    
    print("=== Turnstile验证优化演示 ===")
    print("\n🔄 新的处理逻辑:")
    print("1. ✅ 优先检查 cf-turnstile 元素是否存在")
    print("2. 🎯 如果存在，专注处理该元素（4种方法）")
    print("3. 🔀 如果不存在，尝试其他验证方法")
    print("4. ⏱️ 智能等待验证完成")
    print("5. 🔁 失败后自动重试")
    
    try:
        # 浏览器配置
        co = ChromiumOptions()
        co.add_extension("turnstilePatch")
        co.incognito(True)
        co.auto_port(True)
        
        browser = Chromium(co)
        tab = browser.latest_tab
        
        # 访问包含Turnstile的页面
        test_url = "https://authenticator.cursor.sh"
        print(f"\n🌐 访问测试页面: {test_url}")
        tab.get(test_url)
        
        # 等待页面加载
        time.sleep(3)
        
        # 导入优化后的验证函数
        import importlib.util
        spec = importlib.util.spec_from_file_location("main_module", "1.py")
        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)
        
        print("\n🚀 开始执行优化后的验证流程...")
        print("=" * 50)
        
        # 执行验证
        success = main_module.handle_turnstile(tab)
        
        print("=" * 50)
        if success:
            print("🎉 验证成功完成！")
            print("✅ 优化后的流程工作正常")
        else:
            print("⚠️ 验证未完成")
            print("💡 可能需要手动处理或检查页面")
        
        # 保持浏览器打开以观察结果
        print("\n⏰ 浏览器将保持打开10秒供观察...")
        time.sleep(10)
        
        browser.quit()
        return success
        
    except Exception as e:
        print(f"❌ 演示过程中发生错误: {str(e)}")
        if 'browser' in locals():
            browser.quit()
        return False

def show_optimization_benefits():
    """展示优化带来的好处"""
    
    print("\n💡 优化前后对比:")
    print("\n【优化前】:")
    print("❌ 盲目尝试多种方法")
    print("❌ 没有优先级策略") 
    print("❌ 效率低下")
    print("❌ 成功率不稳定")
    
    print("\n【优化后】:")
    print("✅ 优先检查 cf-turnstile 存在性")
    print("✅ 针对性处理策略")
    print("✅ 更高的处理效率")
    print("✅ 更好的成功率")
    print("✅ 完善的调试信息")
    print("✅ 智能重试机制")
    
    print("\n🎯 核心改进:")
    print("• 先检查 → 再处理 → 最后验证")
    print("• 专注处理已确认存在的元素")
    print("• 减少无效尝试，提高效率")
    print("• 更好的错误处理和用户反馈")

if __name__ == "__main__":
    print("🚀 Turnstile验证优化演示程序")
    print("=" * 60)
    
    # 显示优化好处
    show_optimization_benefits()
    
    # 询问是否运行演示
    print("\n" + "=" * 60)
    user_input = input("是否运行实际验证演示? (y/N): ").strip().lower()
    
    if user_input in ['y', 'yes', '是']:
        print("\n🎬 开始实际演示...")
        success = demo_turnstile_optimization()
        
        if success:
            print("\n🏆 演示完成: 优化方案工作良好!")
        else:
            print("\n📝 演示完成: 可根据日志信息进一步优化")
    else:
        print("\n👋 演示结束，感谢使用!")
    
    print("\n📚 如需了解更多信息，请查看 TURNSTILE_OPTIMIZATION.md") 