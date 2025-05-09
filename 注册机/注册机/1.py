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
                code = None
                # 尝试从垃圾邮件和收件箱获取验证码，设置最大重试次数和等待时间
                max_attempts = 5  # 最大尝试次数
                base_wait_time = 3  # 基础等待时间（秒）
                
                for attempt in range(1, max_attempts + 1):
                    # 先检查垃圾邮件
                    try:
                        print(f"第 {attempt} 次尝试获取验证码 (垃圾邮件)...")
                        code = get_Junk_code(live_email, live_token, live_client_id)
                        if code:
                            print(f"在垃圾邮件中找到验证码: {code}")
                            break
                    except Exception as e:
                        print(f"从垃圾邮件获取验证码出错: {e}")
                    
                    # 再检查收件箱
                    try:
                        print(f"第 {attempt} 次尝试获取验证码 (收件箱)...")
                        code = get_INBOX_code(live_email, live_token, live_client_id)
                        if code:
                            print(f"在收件箱中找到验证码: {code}")
                            break
                    except Exception as e:
                        print(f"从收件箱获取验证码出错: {e}")
                    
                    if attempt < max_attempts:
                        # 使用递增的等待时间
                        wait_time = base_wait_time * attempt
                        print(f"未找到验证码，{wait_time} 秒后重试...")
                        time.sleep(wait_time)
                    else:
                        print(f"已尝试 {max_attempts} 次，仍未找到验证码")
                
                if code:
                    print("最终获取验证码成功：", code)
                    browser.activate_tab(tab)
                    
                    i = 0
                    for digit in code:
                        tab.ele(f'@data-index={i}').input(digit)
                        time.sleep(random.uniform(0.1,0.3))
                        i += 1
                else:
                    print("自动获取验证码失败，请手动输入验证码")
                    # 保持浏览器窗口活跃，等待手动输入
                    browser.activate_tab(tab)
                    # 等待用户手动处理
                    print("请在浏览器中手动输入验证码，完成后按 Enter 键继续...")
                    input("按 Enter 键继续...")
                    # 给页面一些时间可能的跳转
                    time.sleep(2)
                    
                    # 检查是否已成功验证
                    max_check_attempts = 3
                    for check_attempt in range(max_check_attempts):
                        if tab.ele('Account Settings', timeout=2):
                            print("检测到已成功手动验证")
                            break
                        elif check_attempt < max_check_attempts - 1:
                            print(f"未检测到验证成功，继续等待... ({check_attempt + 1}/{max_check_attempts})")
                            time.sleep(2)
                    
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
    browser = None
    
    try:
        with open('email.txt', 'r') as f:
            line = f.readline().strip()
            if not line:
                print("email.txt 文件为空")
                return False
            # 解析邮箱、密码和token
            parts = line.split('----')
            if len(parts) < 4:
                print("email.txt 文件格式错误，需要邮箱----密码----token----client_id格式")
                return False
                
            live_email = parts[0]
            live_password = parts[1]
            live_token = parts[2]
            live_client_id = parts[3]
            
            # 删除已使用的账号
            with open('email.txt', 'r') as f:
                lines = f.readlines()
            with open('email.txt', 'w') as f:
                f.writelines(lines[1:])
            print(f"正在注册邮箱: {live_email}")
            print(f"密码: {live_password}")
            
    except FileNotFoundError:
        print("找不到 email.txt 文件")
        return False
    except Exception as e:
        print(f"读取文件时发生错误: {str(e)}")
        if browser:
            browser.quit()
        return False
    
    try:
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
                result = True
            else:
                print("获取token失败")
                with open('email.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{live_email}----{live_password}----{live_token}----{live_client_id}\n")
                result = False
        else:
            print("账号注册失败")
            with open('email.txt', 'a', encoding='utf-8') as f:
                f.write(f"{live_email}----{live_password}----{live_token}----{live_client_id}\n")
            result = False
    except Exception as e:
        print(f"注册过程中发生错误: {str(e)}")
        with open('email.txt', 'a', encoding='utf-8') as f:
            f.write(f"{live_email}----{live_password}----{live_token}----{live_client_id}\n")
        result = False
    finally:
        if browser:
            try:
                browser.quit()
            except:
                pass
    
    return result


if __name__ == "__main__":
    repeat_times = 2  # 注册次数
    success_count = 0
    
    for i in range(repeat_times):
        try:
            print(f"\n开始第 {i+1}/{repeat_times} 次注册")
            if main():
                success_count += 1
                print(f"成功注册: {success_count}/{i+1} 次尝试")
            else:
                print(f"注册失败，继续下一次尝试")
            
            # 在注册之间添加随机等待时间，避免被检测为机器人
            if i < repeat_times - 1:
                wait_time = random.uniform(2, 5)
                print(f"等待 {wait_time:.1f} 秒后开始下一次注册...")
                time.sleep(wait_time)
                
        except Exception as e:
            print(f"发生错误: {str(e)}")
            continue
    
    print(f"\n注册完成，共完成 {success_count}/{repeat_times} 次注册")