'''
邮件服务模块 - 处理邮件获取和解析
'''
import base64
import imaplib
import poplib
import requests
import email
from email.header import decode_header
import re
from datetime import datetime
import json
import os

class EmailService:
    def __init__(self, client_id=None, email_address=None, refresh_token=None):
        self.client_id = client_id
        self.email_address = email_address
        self.refresh_token = refresh_token
        self.access_token = None
        
    @staticmethod
    def load_email_accounts():
        """从email.txt文件加载所有邮箱账户"""
        accounts = []
        email_file_path = os.path.join(os.path.dirname(__file__), 'email.txt')
        
        try:
            with open(email_file_path, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:
                        continue
                        
                    # 解析格式: email----x----refresh_token----client_id
                    parts = line.split('----')
                    if len(parts) >= 4:
                        email_addr = parts[0]
                        refresh_token = parts[2]
                        client_id = parts[3]
                        
                        accounts.append({
                            'id': line_num,
                            'email': email_addr,
                            'refresh_token': refresh_token,
                            'client_id': client_id
                        })
                    else:
                        print(f"跳过格式错误的行 {line_num}: {line}")
                        
        except FileNotFoundError:
            print("email.txt 文件未找到")
        except Exception as e:
            print(f"读取邮箱账户失败: {e}")
            
        return accounts
    
    @classmethod
    def create_for_account(cls, account_info):
        """为特定邮箱账户创建EmailService实例"""
        return cls(
            client_id=account_info['client_id'],
            email_address=account_info['email'],
            refresh_token=account_info['refresh_token']
        )
        
    def get_access_token(self):
        """获取访问令牌"""
        data = {
            'client_id': self.client_id,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }
        try:
            ret = requests.post('https://login.live.com/oauth20_token.srf', data=data)
            ret.raise_for_status()
            self.access_token = ret.json()['access_token']
            return self.access_token
        except Exception as e:
            print(f"获取访问令牌失败: {e}")
            return None

    def generate_auth_string(self, user, token):
        """生成OAuth2认证字符串"""
        auth_string = f"user={user}\1auth=Bearer {token}\1\1"
        return auth_string

    def decode_mime_words(self, s):
        """解码MIME编码的文本"""
        if not s:
            return ""
        decoded_words = decode_header(s)
        result = ""
        for word, encoding in decoded_words:
            if isinstance(word, bytes):
                if encoding:
                    try:
                        result += word.decode(encoding)
                    except:
                        result += word.decode('utf-8', errors='ignore')
                else:
                    result += word.decode('utf-8', errors='ignore')
            else:
                result += word
        return result

    def extract_email_content(self, msg):
        """提取邮件内容"""
        content = {
            'text': '',
            'html': ''
        }
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    try:
                        content['text'] = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        content['text'] = str(part.get_payload())
                elif content_type == 'text/html':
                    try:
                        content['html'] = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        content['html'] = str(part.get_payload())
        else:
            content_type = msg.get_content_type()
            try:
                payload = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            except:
                payload = str(msg.get_payload())
                
            if content_type == 'text/plain':
                content['text'] = payload
            elif content_type == 'text/html':
                content['html'] = payload
            else:
                content['text'] = payload
                
        return content

    def get_emails_imap(self, limit=50):
        """使用IMAP获取邮件列表"""
        if not self.access_token:
            if not self.get_access_token():
                return []
                
        try:
            mail = imaplib.IMAP4_SSL('outlook.office365.com')
            auth_string = self.generate_auth_string(self.email_address, self.access_token)
            mail.authenticate('XOAUTH2', lambda x: auth_string)
            mail.select("INBOX")
            
            # 搜索所有邮件
            status, messages = mail.search(None, 'ALL')
            if status != 'OK':
                return []
                
            message_ids = messages[0].split()
            emails = []
            
            # 限制邮件数量并倒序（最新的在前）
            message_ids = message_ids[-limit:][::-1]
            
            for i, msg_id in enumerate(message_ids):
                try:
                    # 获取邮件头信息
                    status, msg_data = mail.fetch(msg_id, '(RFC822)')
                    if status != 'OK':
                        continue
                        
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    # 提取邮件信息
                    subject = self.decode_mime_words(msg.get('Subject', ''))
                    sender = self.decode_mime_words(msg.get('From', ''))
                    date_str = msg.get('Date', '')
                    
                    # 解析日期
                    try:
                        date_obj = email.utils.parsedate_tz(date_str)
                        if date_obj:
                            timestamp = email.utils.mktime_tz(date_obj)
                            date_formatted = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            date_formatted = date_str
                    except:
                        date_formatted = date_str
                    
                    # 提取邮件内容
                    content = self.extract_email_content(msg)
                    
                    # 生成预览文本
                    preview = content['text'][:200] if content['text'] else content['html'][:200]
                    preview = re.sub(r'<[^>]+>', '', preview)  # 移除HTML标签
                    preview = re.sub(r'\s+', ' ', preview).strip()  # 清理空白字符
                    
                    email_data = {
                        'id': i + 1,
                        'message_id': msg_id.decode(),
                        'subject': subject,
                        'sender': sender,
                        'date': date_formatted,
                        'preview': preview,
                        'content': content,
                        'read': False  # 可以后续实现已读状态
                    }
                    
                    emails.append(email_data)
                    
                except Exception as e:
                    print(f"处理邮件 {msg_id} 时出错: {e}")
                    continue
            
            mail.logout()
            return emails
            
        except Exception as e:
            print(f"IMAP连接失败: {e}")
            return []

    def get_email_by_id(self, email_id):
        """根据ID获取特定邮件的详细内容"""
        emails = self.get_emails_imap(limit=100)  # 获取更多邮件以确保能找到
        for email_data in emails:
            if email_data['id'] == int(email_id):
                return email_data
        return None 