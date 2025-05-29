'''
Author: sineom sineom@126.com
Date: 2025-03-28 23:26:40
LastEditors: sineom sineom@126.com
LastEditTime: 2025-05-29 21:42:08
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
    ### laurencampbelljqb3106@outlook.com----x----M.C558_SN1.0.U.-CpzrirbvNqGOvFvurLV!vmyKCxQUwv1qGsIoPt93Lv582HXsY3NOuKSoLaO2*1zY68No8Zp88xSv9c98ATxqwD4tjmLUNRpHx4sgMYZxe*r43FBNGyvH*Nomgc7WXguejfFpFHAnqGHvzodI!yG3lTu*zxOxaQpW16*U1fyzaZVpNN3d3!fxTN1Rjt6fhYYqX!Q1DGrTA49NE0B7*g8Loxm9qoZRlrLRmmStNecZ2xd6nT2hfJDLw*NbXSu450!TBkeQ0oEelWDYspe2NqHmg78mgUo7HjR!XYsqwMUZ7a2B8JEjogKKncQjSqxiNFWbMDiVl*ULfciJf*52AxZOn174J4fNk5YzxAMr4rJnAofdIP2M4*ZuU3EAaCkMJiqtFHGLcd6E9k51ZT4FbCl4pw!OmBC8HFAb9!a6Sxd1dYe9----9e5f94bc-e8a4-4e73-b8be-63364c29d753
    email = "laurencampbelljqb3106@outlook.com"
    access_token = "M.C558_SN1.0.U.-CpzrirbvNqGOvFvurLV!vmyKCxQUwv1qGsIoPt93Lv582HXsY3NOuKSoLaO2*1zY68No8Zp88xSv9c98ATxqwD4tjmLUNRpHx4sgMYZxe*r43FBNGyvH*Nomgc7WXguejfFpFHAnqGHvzodI!yG3lTu*zxOxaQpW16*U1fyzaZVpNN3d3!fxTN1Rjt6fhYYqX!Q1DGrTA49NE0B7*g8Loxm9qoZRlrLRmmStNecZ2xd6nT2hfJDLw*NbXSu450!TBkeQ0oEelWDYspe2NqHmg78mgUo7HjR!XYsqwMUZ7a2B8JEjogKKncQjSqxiNFWbMDiVl*ULfciJf*52AxZOn174J4fNk5YzxAMr4rJnAofdIP2M4*ZuU3EAaCkMJiqtFHGLcd6E9k51ZT4FbCl4pw!OmBC8HFAb9!a6Sxd1dYe9"
    client_id = "9e5f94bc-e8a4-4e73-b8be-63364c29d753" 
    print(get_Junk_code(email, access_token,client_id))
    print(get_INBOX_code(email, access_token,client_id))