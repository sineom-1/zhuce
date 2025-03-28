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
    email = "akioocoyuu739@hotmail.com"
    access_token = "M.C545_BAY.0.U.-Cp*X2wf9YxEf3Sb00R4DuTICLGxcn!83zRirznpQHaf!k!pNyTqFpyD9eC0vbijwLU0QKfFsDzweiq!sOGIF7GTbgnWnlUcWx23ZC*ilX1On*e8fieLVuJZDdbRZdC7MsIU9B*q2qsKGmXlTBq3LakS445N8UtmseSPUXNWsz4gYTiKNR3xkOM6iLadGYKsLRCy5BlgZuLXRks8nh3DNaWb0JNTM3kD6edQN8lBbx2hMrmXJ!l7w4a1V9xwFJQZCrXbp4qCU5aYgll5JS3kJfMNXmLi2dj18ZNxxFaWyKoxhWQM*K9tbEMb!dXUsFevD8u2OmIfczkxwmivbXVdmUnK!*Bcj2im6hhCmLEE!bJLt*IoRsprj1eV4r7FQz1ZedVs9tHlsa*lvzjfwUSXY1kuETghgQZ1WPwdVf6cgU9L*"
    client_id = "8b4ba9dd-3ea5-4e5f-86f1-ddba2230dcf2"
    print(get_Junk_code(email, access_token,client_id))
    print(get_INBOX_code(email, access_token,client_id))