'''
Author: sineom sineom@126.com
Date: 2025-05-29 14:00:07
LastEditors: sineom sineom@126.com
LastEditTime: 2025-05-29 14:13:01
FilePath: /cursorX项目/注册机/注册机/get_email.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
                
import base64
import imaplib
import poplib
import requests

def get_access_token(client_id, refresh_token):
    data = {
        'client_id': client_id,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    ret = requests.post('https://login.live.com/oauth20_token.srf', data=data)

    # 打印响应内容和访问令牌
    print(ret.text)
    print(ret.json()['access_token'])
    return ret.json()['access_token']

# 使用访问令牌生成OAuth2认证字符串
def generate_auth_string(user, token):
    auth_string = f"user={user}\1auth=Bearer {token}\1\1"
    return auth_string

pop3_server = 'outlook.office365.com'
pop3_port = 995  # 使用SSL的POP3

def connect_pop3(email, access_token):
    server = poplib.POP3_SSL(pop3_server, pop3_port)
    # 使用OAuth2进行认证
    auth_string = generate_auth_string(email, access_token)
    encoded_auth_string = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
    server._shortcmd(f'AUTH XOAUTH2')
    server._shortcmd(f'{encoded_auth_string}')

    # 获取邮件列表
    num_messages = len(server.list()[1])
    print(f"邮箱中有 {num_messages} 封邮件。")

    # 获取邮件内容
    for i in range(num_messages):
        response, lines, octets = server.retr(i + 1)
        msg_content = b"\n".join(lines).decode("utf-8")
        print(f"邮件 {i + 1}:")
        print(msg_content)
        print("=" * 50)

def connect_imap(email, access_token):
    mail = imaplib.IMAP4_SSL('outlook.office365.com')
    # 打印生成的认证字符串
    print(generate_auth_string(email, access_token))
    mail.authenticate('XOAUTH2', lambda x: generate_auth_string(email, access_token))
    mail.select("INBOX")
    status, messages = mail.search(None, 'ALL')
    print("邮件ID:", messages)
    mail.logout()

# 设置电子邮件地址和刷新令牌  
#### laurencampbelljqb3106@outlook.com----x----M.C558_SN1.0.U.-CpzrirbvNqGOvFvurLV!vmyKCxQUwv1qGsIoPt93Lv582HXsY3NOuKSoLaO2*1zY68No8Zp88xSv9c98ATxqwD4tjmLUNRpHx4sgMYZxe*r43FBNGyvH*Nomgc7WXguejfFpFHAnqGHvzodI!yG3lTu*zxOxaQpW16*U1fyzaZVpNN3d3!fxTN1Rjt6fhYYqX!Q1DGrTA49NE0B7*g8Loxm9qoZRlrLRmmStNecZ2xd6nT2hfJDLw*NbXSu450!TBkeQ0oEelWDYspe2NqHmg78mgUo7HjR!XYsqwMUZ7a2B8JEjogKKncQjSqxiNFWbMDiVl*ULfciJf*52AxZOn174J4fNk5YzxAMr4rJnAofdIP2M4*ZuU3EAaCkMJiqtFHGLcd6E9k51ZT4FbCl4pw!OmBC8HFAb9!a6Sxd1dYe9----9e5f94bc-e8a4-4e73-b8be-63364c29d753
client_id = '9e5f94bc-e8a4-4e73-b8be-63364c29d753'
email = "laurencampbelljqb3106@outlook.com"
t = "M.C558_SN1.0.U.-CpzrirbvNqGOvFvurLV!vmyKCxQUwv1qGsIoPt93Lv582HXsY3NOuKSoLaO2*1zY68No8Zp88xSv9c98ATxqwD4tjmLUNRpHx4sgMYZxe*r43FBNGyvH*Nomgc7WXguejfFpFHAnqGHvzodI!yG3lTu*zxOxaQpW16*U1fyzaZVpNN3d3!fxTN1Rjt6fhYYqX!Q1DGrTA49NE0B7*g8Loxm9qoZRlrLRmmStNecZ2xd6nT2hfJDLw*NbXSu450!TBkeQ0oEelWDYspe2NqHmg78mgUo7HjR!XYsqwMUZ7a2B8JEjogKKncQjSqxiNFWbMDiVl*ULfciJf*52AxZOn174J4fNk5YzxAMr4rJnAofdIP2M4*ZuU3EAaCkMJiqtFHGLcd6E9k51ZT4FbCl4pw!OmBC8HFAb9!a6Sxd1dYe9"

# 使用刷新令牌获取访问令牌
acc_token = get_access_token(client_id, t)

# 连接到IMAP服务器并访问电子邮件
connect_pop3(email, acc_token)