'''
Flask Web邮件客户端
'''
from flask import Flask, render_template, jsonify, request
from email_service import EmailService
import os

app = Flask(__name__)

# 邮件配置 - 从原get_email.py文件中获取
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

@app.route('/')
def index():
    """主页 - 邮件列表页面"""
    return render_template('index.html')

@app.route('/api/emails')
def get_emails():
    """获取邮件列表API"""
    try:
        limit = request.args.get('limit', 50, type=int)
        emails = email_service.get_emails_imap(limit=limit)
        return jsonify({
            'success': True,
            'emails': emails,
            'total': len(emails)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/emails/<int:email_id>')
def get_email_detail(email_id):
    """获取邮件详情API"""
    try:
        email_data = email_service.get_email_by_id(email_id)
        if email_data:
            return jsonify({
                'success': True,
                'email': email_data
            })
        else:
            return jsonify({
                'success': False,
                'error': '邮件未找到'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/email/<int:email_id>')
def email_detail_page(email_id):
    """邮件详情页面"""
    return render_template('email_detail.html', email_id=email_id)

if __name__ == '__main__':
    # 创建templates目录
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(debug=True, host='0.0.0.0', port=5001) 