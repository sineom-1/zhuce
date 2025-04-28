'''
Author: sineom sineom@126.com
Date: 2025-03-27 02:06:20
LastEditors: sineom sineom@126.com
LastEditTime: 2025-04-28 16:20:11
FilePath: /邀请成员/cursor组织邀请.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import random
import aiohttp
import asyncio
import json
from tqdm import tqdm

# 设置邀请代码
invite_code = "a1f6906579fe7651b6bc18b933e71dd500c3214bb316053b"

# 读取cookies.txt文件
with open('cookies.txt', 'r') as file:
    cookies = file.readlines()

# 定义异步请求函数
async def send_request(session, semaphore, cookie):
    async with semaphore:  # 限制并发请求
        cookie = cookie.strip()  # 去除换行符和空格
        # 设置请求头
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

        # 设置请求数据
        data = {
            'inviteCode': invite_code
        }

        # 发送POST请求
        async with session.post('https://www.cursor.com/api/accept-invite', headers=headers, json=data) as response:
            print(response.status)
            if response.status == 200:
                # 解析JSON响应
                response_data = await response.json()
                team_id = response_data.get("teamId")
                if team_id:
                    return cookie  # 返回成功的cookie
    return None  # 返回None表示请求失败

# 定义主异步函数
async def main():
    semaphore = asyncio.Semaphore(30)  # 限制并发请求为30
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, semaphore, cookie) for cookie in cookies]
        results = await asyncio.gather(*tasks)

        # 写入成功的token
        with open('success.txt', 'w') as success_file:
            for result in tqdm(results, total=len(cookies)):
                if result:
                    success_file.write(f"{result}\n")  # 写入成功的token

# 运行主函数
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"发生错误: {e}")