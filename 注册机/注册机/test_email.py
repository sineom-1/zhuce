#!/usr/bin/env python3
"""
邮件服务测试脚本
"""

from reset_pwd.email_service import EmailService

def test_email_service():
    """测试邮件服务功能"""
    print("🧪 开始测试邮件服务...")
    print("=" * 50)
    
    # 使用配置信息
    EMAIL_CONFIG = {
        'client_id': '9e5f94bc-e8a4-4e73-b8be-63364c29d753',
        'email': 'laurencampbelljqb3106@outlook.com',
        'refresh_token': 'M.C558_SN1.0.U.-CpzrirbvNqGOvFvurLV!vmyKCxQUwv1qGsIoPt93Lv582HXsY3NOuKSoLaO2*1zY68No8Zp88xSv9c98ATxqwD4tjmLUNRpHx4sgMYZxe*r43FBNGyvH*Nomgc7WXguejfFpFHAnqGHvzodI!yG3lTu*zxOxaQpW16*U1fyzaZVpNN3d3!fxTN1Rjt6fhYYqX!Q1DGrTA49NE0B7*g8Loxm9qoZRlrLRmmStNecZ2xd6nT2hfJDLw*NbXSu450!TBkeQ0oEelWDYspe2NqHmg78mgUo7HjR!XYsqwMUZ7a2B8JEjogKKncQjSqxiNFWbMDiVl*ULfciJf*52AxZOn174J4fNk5YzxAMr4rJnAofdIP2M4*ZuU3EAaCkMJiqtFHGLcd6E9k51ZT4FbCl4pw!OmBC8HFAb9!a6Sxd1dYe9'
    }
    
    # 初始化邮件服务
    email_service = EmailService(
        EMAIL_CONFIG['client_id'],
        EMAIL_CONFIG['email'],
        EMAIL_CONFIG['refresh_token']
    )
    
    # 测试获取访问令牌
    print("🔑 测试获取访问令牌...")
    token = email_service.get_access_token()
    if token:
        print("✅ 访问令牌获取成功")
        print(f"令牌前缀: {token[:50]}...")
    else:
        print("❌ 访问令牌获取失败")
        return False
    
    # 测试获取邮件列表
    print("\n📧 测试获取邮件列表...")
    emails = email_service.get_emails_imap(limit=5)
    
    if emails:
        print(f"✅ 成功获取 {len(emails)} 封邮件")
        print("\n📋 邮件列表预览:")
        print("-" * 50)
        
        for i, email in enumerate(emails[:3], 1):  # 只显示前3封
            print(f"{i}. 发件人: {email['sender'][:50]}...")
            print(f"   主题: {email['subject'][:50]}...")
            print(f"   日期: {email['date']}")
            print(f"   预览: {email['preview'][:100]}...")
            print("-" * 50)
        
        # 测试获取特定邮件详情
        if emails:
            print(f"\n📖 测试获取邮件详情 (ID: {emails[0]['id']})...")
            email_detail = email_service.get_email_by_id(emails[0]['id'])
            if email_detail:
                print("✅ 邮件详情获取成功")
                print(f"内容长度: 文本={len(email_detail['content']['text'])} 字符, HTML={len(email_detail['content']['html'])} 字符")
            else:
                print("❌ 邮件详情获取失败")
        
        return True
    else:
        print("❌ 邮件列表获取失败")
        return False

def main():
    """主函数"""
    try:
        success = test_email_service()
        print("\n" + "=" * 50)
        if success:
            print("🎉 所有测试通过！Web邮件客户端已准备就绪")
            print("💡 运行 'python app.py' 启动Web服务器")
            print("🌐 然后访问 http://localhost:5000")
        else:
            print("❌ 测试失败，请检查配置")
    except Exception as e:
        print(f"💥 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 