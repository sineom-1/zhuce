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
client_id = '9e5f94bc-e8a4-4e73-b8be-63364c29d753'
email = "TracyMoore1973718@outlook.com"
t = "M.C556_BAY.0.U.-CjFBNOZUrWO0zoB31lSy15Dk6lfwJH123oPhdSqiyrDGpA5!1!1ihMLkRTUvky*Z2sIHKlcr!2FvN!USfEHaKt9pymyn2bjvUvmylX7S8wPvmmiwaHGfg*!3kygSQnFU*Ebwqa6O1VDFpZjtoKVooHh4PsaF6kovLBxB2dnnreUBfVkCiL!92CtYmjTtXaLMp07u4gU9ZFJzy5z*6z9KZ0NCWyyVJpgwiBzHctLDRUYuRI9nNrC5wj4XlSJCzHV*CMkHYfR22IzSlYvXnD1SwVlpfWC!1uqpexVIcTSDsvQ1VeTMlFpxyYTkp2sf7bY2lrwum1GoAO39xphdCnBQyJYiBNCtL7xcRL1FkUEWEr4re6e!DdjPv*6DzMAkaWNC0o7fCMD9Kpb9R7PNCfSk4uY83uwZa2UvvKSH9rsqTWOm"

# 使用刷新令牌获取访问令牌
acc_token = get_access_token(client_id, t)

# 连接到IMAP服务器并访问电子邮件
connect_imap(email, acc_token)


# 运行主函数
if __name__ == "__main__":
    try:
        connect_pop3(email=email,access_token="EwA4BOl3BAAUcDnR9grBJokeAHaUV8R3+rVHX+IAAbZ5YjbRIbfjyUsM9HcxZEXEYm6eJOts9xBuhsbC4Sh3ClY7E1sN3IiEt9NtJwHhteFB2yNX5owLfn3P2W/i15TN5fVszoq56kOxA8+WGGujkEndLopUzPQD7XCtPRl4b4Vz5d/DKrbTOjMZ2OBwVw+CV+lPGIGlHa9bNThoCoxAThGtS8WdrPP8FJBAUJt8jOcLwzYSKt2G+3n1SyIZh3p4xNFnPr8H7ay4qGBt13HjHrzOq6P0dVlO1vS86ctFsUeCbvPWlFnU95XSR8f0PTP9XuBko9NutbRKIQfS+I0JCzvn7sBOA1W9zzes/sbdkknZpHJkf6EsjsZH57sExX0QZgAAENIwbAyPrjLJNm4c5NYGSDEAA1Wb5RPlW74YCqu2+72L8XWuveKRA6iFiyFed5wFht7+n8yoqH/mAEjVy4z56VtUtH8zjvpLTETGZeltMNYLw6Wb/4s9hbw863Ldd1yOk+v4B/3Qx1iNFvC61RoLaJThMzCCzl7eTmIuX9Twm70+YNP7m/zQnbetmmxcMF/u/8TFX3UMUdF9n0/SXUumEq6Ai66bZXbz/jngnpXWhjX//CRnWhMKZPpSyIdtdldTq7oyVYV//B+yY4lPuUjrP4LozzYnkmduD+bfQs/bvlkhKe3iM4BbaflzV4+QPLiPWoFIrWClX55lWALIkHhW2SBawZL4iqiE4H6bMgAw1i770Kd1GzricLKnBAUReVxnNVSKVu5NPr0P5AbzEv5OeC76pS21tfy/IvFL7+VbVTOulhZTR6pXITfK+4e2at3ST0JaaclwYKeEk38BoEn+utPoMkJs27iwpIuWLmIq+YO3cqnaWByiwUlSVG6UYh8bf/RvkjapyiWpdPoFEuJlO8k1Nt3fmvEgcEkyqrcsMMFXodRnX/Ca6rLJSoFqE1+48Kq9lesEA//11sER5o3rejKKzCeV48OnTWRaPVM+ThtO7ZDqhyyj2qPJvIsAAj1FcOphMLfUZC0y5Qk4wFOF5hYSiCbtR3Zqkp3unl/lPprHFToepUsGLWzoPio0LrROJGVIQqF61dMhxYRLzrs61KGoqtjTy+DhzSGzdQRHArpdi8fIzJ5UJjRuDNHkTVw0+Q7j+EfDqGBBdh6NthC3r+nN2iBONtdnZWpuUQ0yLtaQrRk6CkuopO7l/bh50zDpOQZg07uXfyOH848BJrbR/IP3/0U2qHLAn8dADYirmuP6vpCq5Jy7Vd8nsoTRSCyne8S7W5r32x+bTInrN92dFtFp1dlU5YW/wFwbkKdKWxWBI9jzZUDsENwjCqeeWckHuHBMaJpa1eTDsQPgmvCPNdhvaOGCxzpPxiaTg1Ee0gT/nQO3MC+crxcB7MvV9ppHgYS/G5DIRR2AOiQxG/yUCysKUDUD")
    except Exception as e:
        print(f"发生错误: {e}")

