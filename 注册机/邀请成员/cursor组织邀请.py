'''
Author: sineom sineom@126.com
Date: 2025-03-27 02:06:20
LastEditors: sineom sineom@126.com
LastEditTime: 2025-05-28 12:46:26
FilePath: /邀请成员/cursor组织邀请.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import random
import aiohttp
import asyncio
import json
from tqdm import tqdm
import requests
import concurrent.futures

# 设置邀请代码
invite_code = "0ebde47581589246135fe2a3f340b0235078a6c75d39cee9"

# 读取cookies.txt文件
with open('cookies.txt', 'r') as file:
    cookies = file.readlines()

# Modify the send_request function to be compatible with multithreading
def send_request(cookie):
    from datetime import datetime
    start_time = datetime.now()
    print(f"线程开始执行时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')} | cookie: {cookie.strip()}")
    cookie = cookie.strip()  # Remove newline and spaces
    # Set request headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/json',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'origin': 'https://www.cursor.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://www.cursor.com/team/accept-invite?code={invite_code}',
        'accept-language': 'de_AT,AT;q=0.9,en;q=0.8,de_AT;q=0.7,cs;q=0.6,fr;q=0.5,no;q=0.4,it;q=0.3',
        'priority': 'u=1, i',
        'Cookie': f'WorkosCursorSessionToken={cookie}'
    }
    # Set request data
    data = {
        'inviteCode': invite_code
    }
    # Send POST request
    response = requests.post('https://www.cursor.com/api/accept-invite', headers=headers, json=data)
    if response.status_code == 200:
        # Parse JSON response
        response_data = response.json()
        team_id = response_data.get("teamId")
        if team_id:
            end_time = datetime.now()
            print(f"线程结束执行时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')} | cookie: {cookie}")
            return cookie  # Return successful cookie
    end_time = datetime.now()
    print(f"线程结束执行时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')} | cookie: {cookie}")
    return None  # Return None if request failed

# Define the main function for multithreading
def main(concurrency):
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        # Submit tasks to the thread pool
        futures = {executor.submit(send_request, cookie): cookie for cookie in cookies}
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    # Write successful tokens
    with open('success.txt', 'w') as success_file:
        for result in tqdm(results, total=len(results)):
            success_file.write(f"{result}\n")  # Write successful token
    print("全部异步任务已完成")

# Run the main function
if __name__ == "__main__":
    try:
        concurrency = 60  # Set default concurrency level
        main(concurrency)
    except Exception as e:
        print(f"发生错误: {e}")