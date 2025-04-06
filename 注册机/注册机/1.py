from DrissionPage import ChromiumOptions, Chromium
from DrissionPage.common import Keys
import time
import random
from mail_api import get_INBOX_code, get_Junk_code

import os

def handle_turnstile(tab):
    """处理 Turnstile 验证"""
    print("准备处理验证")
    try:  
        while True:
            try:
                challengeCheck = (tab.ele('@id=cf-turnstile', timeout=2)
                                    .child()
                                    .shadow_root
                                    .ele("tag:iframe")
                                    .ele("tag:body")
                                    .sr("tag:input"))
                                    
                if challengeCheck:
                    print("验证框加载完成")
                    time.sleep(random.uniform(1, 3))
                    challengeCheck.click()
                    print("验证按钮已点击，等待验证完成...")
                    time.sleep(2)
                    return True
            except:
                pass

            if tab.ele('@name=password', timeout=2):
                print("无需验证")   
                break            
            if tab.ele('@data-index=0', timeout=2):
                print("无需验证")   
                break
            if tab.ele('Account Settings', timeout=2):
                print("无需验证")   
                break       

            time.sleep(random.uniform(1,2))       
    except Exception as e:
        print(e)
        print('跳过验证')
        return False

def get_cursor_session_token(tab):
    """获取cursor session token"""
    cookies = tab.cookies()
    cursor_session_token = None
    for cookie in cookies:
        if cookie['name'] == 'WorkosCursorSessionToken':
            cursor_session_token = cookie['value']
            break
    return cursor_session_token

def sign_up_account(browser, tab, live_email, live_password, live_token, live_client_id, sign_up_url):
    """注册账户流程"""
    print("\n开始注册新账户...")
    tab.get(sign_up_url)

    try:
        if tab.ele('@name=email'):
            print("已打开注册页面")
            tab.actions.click('@name=email').input(live_email)
            print("输入邮箱" )
            time.sleep(random.uniform(1,2))
            tab.actions.click('@type=submit')
            print("点击注册按钮")
    except Exception as e:
        print("打开注册页面失败")
        return False

    handle_turnstile(tab)            

    try:
        if tab.ele('@class=rt-reset rt-BaseButton rt-r-size-3 rt-variant-surface rt-high-contrast rt-Button'):
            tab.ele('@class=rt-reset rt-BaseButton rt-r-size-3 rt-variant-surface rt-high-contrast rt-Button').click()
            print("点击获取验证码按钮")
    except Exception as e:
        print("点击获取验证码按钮失败")
        return False

    time.sleep(random.uniform(1,2))
    if tab.ele('This email is not available.'):
        print('This email is not available.')
        return False

    handle_turnstile(tab)
    time.sleep(random.uniform(1,2))
    while True:
        try:
            if tab.ele('Account Settings'):
                break
            if tab.ele('@data-index=0'):
                print("准备获取验证码")
                try:
                    code = get_Junk_code(live_email, live_token,live_client_id)
                    print("code:",code)
                except Exception as e:
                    print("报错：",e)
                if code == None:
                    try:
                        code = get_INBOX_code(live_email, live_token,live_client_id)
                        print("code:",code)
                    except Exception as e:
                        print("报错：",e)
                if code:
                    print("获取验证码成功：", code)
                    browser.activate_tab(tab)
                else:
                    print("获取验证码失败，程序退出")
                    return False

                i = 0
                for digit in code:
                    tab.ele(f'@data-index={i}').input(digit)
                    time.sleep(random.uniform(0.1,0.3))
                    i += 1
                break
        except Exception as e:
            print(e)

    handle_turnstile(tab)
    
    time.sleep(random.uniform(1,2))
    print("注册完成")
    print("Cursor 账号： " + live_email)
    print("       密码： " + live_password)
    return True

def main():
    # 配置信息
    sign_up_url = 'https://authenticator.cursor.sh'
    
    try:
        with open('email.txt', 'r') as f:
            line = f.readline().strip()
            if not line:
                print("email.txt 文件为空")
            # 解析邮箱、密码和token
            live_email = line.split('----')[0]
            live_password = line.split('----')[1]
            live_token = line.split('----')[2]
            live_client_id = line.split('----')[3]
            # 删除已使用的账号
            with open('email.txt', 'r') as f:
                lines = f.readlines()
            with open('email.txt', 'w') as f:
                f.writelines(lines[1:])
            print(f"正在注册邮箱: {live_email}")
            print(f"密码: {live_password}")
            
    except FileNotFoundError:
        print("找不到 email.txt 文件")
        return
    except Exception as e:
        print(f"读取文件时发生错误: {str(e)}")
        browser.quit()
        return
    
    # 浏览器配置
    co = ChromiumOptions()
    co.add_extension("turnstilePatch")
    co.set_pref('credentials_enable_service', False)
    co.set_argument('--hide-crash-restore-bubble') 
    co.incognito(True)
    co.auto_port(True)
    co.use_system_user_path()
    # 设置代理
    #co.set_proxy(http='http://111.180.198.68:1900')

    browser = Chromium(co)
    tab = browser.latest_tab
    tab.run_js("try { turnstile.reset() } catch(e) { }")

    if sign_up_account(browser, tab, live_email, live_password, live_token, live_client_id, sign_up_url):
        time.sleep(1)
        token = get_cursor_session_token(tab)
        if token!=None:
            os.makedirs('output', exist_ok=True)
            with open('output/cursor_accounts.txt', 'a', encoding='utf-8') as f:
                f.write(f"{live_email}----{live_password}----{token}\n")
            print("账户注册成功")
        else:
            print("账号注册失败")
            with open('email.txt', 'a', encoding='utf-8') as f:
                f.write(f"{live_email}----{live_password}----{live_client_id}----{live_token}\n")
    else:
        print("账号注册失败")
        with open('email.txt', 'a', encoding='utf-8') as f:
            f.write(f"{live_email}----{live_password}----{live_client_id}----{live_token}\n")
        browser.quit()
    browser.quit()    


if __name__ == "__main__":
    repeat_times = 5  # 注册次数
    for i in range(repeat_times):
        try:
            print(f"\n开始第 {i+1}/{repeat_times} 次注册")
            main()
        except Exception as e:
            print(f"发生错误: {e}")
            continue