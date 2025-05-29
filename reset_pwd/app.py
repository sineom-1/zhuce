'''
Author: sineom sineom@126.com
Date: 2025-05-29 21:17:37
LastEditors: sineom sineom@126.com
LastEditTime: 2025-05-29 21:35:06
FilePath: /zhuce/注册机/注册机/app.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
'''
Flask Web邮件客户端
'''
from flask import Flask, render_template, jsonify, request, redirect, url_for
from email_service import EmailService
import os

app = Flask(__name__)

@app.route('/')
def index():
    """主页 - 邮箱列表页面"""
    return render_template('mailbox_list.html')

@app.route('/api/mailboxes')
def get_mailboxes():
    """获取邮箱列表API"""
    try:
        accounts = EmailService.load_email_accounts()
        return jsonify({
            'success': True,
            'mailboxes': accounts,
            'total': len(accounts)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/mailbox/<int:mailbox_id>')
def mailbox_detail(mailbox_id):
    """邮箱邮件列表页面"""
    return render_template('email_list.html', mailbox_id=mailbox_id)

@app.route('/api/mailbox/<int:mailbox_id>/emails')
def get_emails_by_mailbox(mailbox_id):
    """获取指定邮箱的邮件列表API"""
    try:
        # 获取所有邮箱账户
        accounts = EmailService.load_email_accounts()
        
        # 查找指定的邮箱
        target_account = None
        for account in accounts:
            if account['id'] == mailbox_id:
                target_account = account
                break
                
        if not target_account:
            return jsonify({
                'success': False,
                'error': '邮箱未找到'
            }), 404
            
        # 创建邮件服务实例
        email_service = EmailService.create_for_account(target_account)
        
        # 获取邮件
        limit = request.args.get('limit', 50, type=int)
        emails = email_service.get_emails_imap(limit=limit)
        
        return jsonify({
            'success': True,
            'emails': emails,
            'total': len(emails),
            'mailbox': target_account
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/mailbox/<int:mailbox_id>/emails/<int:email_id>')
def get_email_detail_by_mailbox(mailbox_id, email_id):
    """获取指定邮箱中特定邮件的详情API"""
    try:
        # 获取所有邮箱账户
        accounts = EmailService.load_email_accounts()
        
        # 查找指定的邮箱
        target_account = None
        for account in accounts:
            if account['id'] == mailbox_id:
                target_account = account
                break
                
        if not target_account:
            return jsonify({
                'success': False,
                'error': '邮箱未找到'
            }), 404
            
        # 创建邮件服务实例
        email_service = EmailService.create_for_account(target_account)
        
        # 获取邮件详情
        email_data = email_service.get_email_by_id(email_id)
        if email_data:
            return jsonify({
                'success': True,
                'email': email_data,
                'mailbox': target_account
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

@app.route('/mailbox/<int:mailbox_id>/email/<int:email_id>')
def email_detail_page(mailbox_id, email_id):
    """邮件详情页面"""
    return render_template('email_detail.html', mailbox_id=mailbox_id, email_id=email_id)

# 保留原有的API路由作为兼容（已废弃）
@app.route('/api/emails')
def get_emails():
    """获取邮件列表API（已废弃，请使用/api/mailbox/<id>/emails）"""
    return jsonify({
        'success': False,
        'error': '此API已废弃，请先选择邮箱'
    }), 410

@app.route('/api/emails/<int:email_id>')
def get_email_detail(email_id):
    """获取邮件详情API（已废弃，请使用/api/mailbox/<id>/emails/<email_id>）"""
    return jsonify({
        'success': False,
        'error': '此API已废弃，请先选择邮箱'
    }), 410

@app.route('/email/<int:email_id>')
def old_email_detail_page(email_id):
    """邮件详情页面（已废弃，重定向到主页）"""
    return redirect(url_for('index'))

if __name__ == '__main__':
    # 创建templates目录
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(debug=True, host='0.0.0.0', port=5001) 