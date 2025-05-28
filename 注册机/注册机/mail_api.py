'''
Author: sineom sineom@126.com
Date: 2025-03-28 23:26:40
LastEditors: sineom sineom@126.com
LastEditTime: 2025-05-28 23:09:59
FilePath: /zhuce/注册机/注册机/mail_api.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import requests
import re

def get_INBOX_code(email, access_token,client_id):
    try:
        url = f"https://email.aliyy.cc/api/mail-new/?refresh_token={access_token}&client_id={client_id}&email={email}&mailbox=INBOX"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()["text"]
            print(data)
            verify_code_pattern = r'Your one-time code is:\s*\n\s*(\d\s+\d\s+\d\s+\d\s+\d\s+\d)'
            match = re.search(verify_code_pattern, data)
            if match:
                verify_code = match.group(1).replace(' ', '')
                print(f"找到验证码:", verify_code)
                return verify_code
            else:
                return None
        else:
            print(f"获取验证码失败")
            return None
    except Exception as e:
        print(f"获取验证码失败: {e}")
        return None

def get_Junk_code(email, access_token,client_id):
    try:
        url = f"https://email.aliyy.cc/api/mail-new/?refresh_token={access_token}&client_id={client_id}&email={email}&mailbox=Junk"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()["text"]
            print(data)
            verify_code_pattern = r'Your one-time code is:\s*\n\s*(\d\s+\d\s+\d\s+\d\s+\d\s+\d)'
            match = re.search(verify_code_pattern, data)
            if match:
                verify_code = match.group(1).replace(' ', '')
                print(f"找到验证码:", verify_code)
                return verify_code
            else:
                return None
        else:
            print(f"获取验证码失败")
            return None
    except Exception as e:
        print(f"获取验证码失败: {e}")
        return None
    

if __name__ == "__main__":
    email = "jamesreeseyxek@outlook.com"
    access_token = "M.C543_SN1.0.U.-Ckt65NDWel!bZDKnWl8FDDeOerrnis21hXeiMbgWFzYUo*Vys!Fv1LfyeSgtyLay9EMQCs3G*1!yBh0TyIgyuUJ1Vln8x*W2OqrL9YVQ4rY6GB6yD0SKR!6H1ZuAJuib8oGtXbJTzejCWnGBhn5i3jR0xCoNq!CoTnBBoEHzhs2*!VcHriuLWAQ8DoxUJYBMOFGMgzpl1kUJkwBRjdUcmF7wNjGd!Gl!wqG!IYEiF8b5SFb02x57ikLF!zEau!cQ3C4XTbcjblaX!twlIBFWwOBRPW5RPmYwEMH5X0Vn9cTRwGlo*sSMJDVJTGH3LIQ9kGCmAsusmEOGANM69akbilDP6HPTnNzXOI*KyBFwNuVbHUAiT40ggqtGBaYYL!Gpdyh*75uEIBvsMTbeBjj4kmd9*Vui*vyM5LDwPPwzn*ne!jHJnKwWC31ZdrG9rxgS1g$$"
    client_id = "9e5f94bc-e8a4-4e73-b8be-63364c29d753"
    print(get_Junk_code(email, access_token,client_id))
    print(get_INBOX_code(email, access_token,client_id))