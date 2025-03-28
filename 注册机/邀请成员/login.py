# Cursor一键登录

import requests

def main(challenge, uuid, session_token):
    # 调用接口实现登录
    url = "https://www.cursor.com/api/auth/loginDeepCallbackControl"
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "origin":"https://www.cursor.com",
        "priority":"u=1, i",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "referer": f"https://www.cursor.com/cn/loginDeepControl?challenge={challenge}&uuid={uuid}&mode=login",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "cookie":f"WorkosCursorSessionToken={session_token}"
    }
    data = {
        "uuid": uuid,
        "challenge": challenge
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        print("登录成功")
    else:
        print("登录失败")

if __name__ == "__main__":
    # 从token.txt中获取session_token并删除第一行
    try:
        with open("token.txt", "r") as f:
            lines = f.readlines()
            if lines:
                session_token = lines[0].strip()
                # 删除第一行
                with open("token.txt", "w") as fw:
                    fw.writelines(lines[1:])
            else:
                print("token.txt文件为空，请先添加token")
                exit(1)
    except FileNotFoundError:
        print("未找到token.txt文件，请先创建并添加token")
        exit(1)
 
    url = input("请输入要登录的网址：")
    if not url:  # 检查URL是否为空
        print("URL不能为空")
        exit(1)
    print(f"登录网址: {url}")
    
    # 从URL提取challenge参数
    try:
        if "challenge=" in url:
            challenge = url.split("challenge=")[1].split("&")[0]
            print(f"challenge: {challenge}")
        else:
            print("URL中未找到challenge参数")
            exit(1)
            
        # 从URL提取uuid参数
        if "uuid=" in url:
            uuid = url.split("uuid=")[1].split("&")[0] if "&" in url.split("uuid=")[1] else url.split("uuid=")[1]
            print(f"uuid: {uuid}")
        else:
            print("URL中未找到uuid参数")
            exit(1)
            
        main(challenge, uuid, session_token)
    except Exception as e:
        print(f"处理URL时出错: {e}")
        print("请确保URL格式正确，例如: https://cursor.com/loginDeepControl?challenge=xxx&uuid=yyy")
        exit(1)