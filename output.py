#2024-09-13 13:29:04

import base64
import json
import requests
import random
import time
import hashlib
import string
import threading
import os

class qqmc():
    def __init__(self,token) -> None:
        self.device = token.split('#')[0]
        self.token = token.split('#')[1]
        self.headers_g = {
            "Authorization": self.token,
            "X-Version-Code": "105",
            "X-Platform": "android",
            "X-System": "11",
            "X-Brand": "Redmi",
            "X-Device-ID": self.device,
            "X-Client-Id": "com.yourong.app.qqmc",
            "distributor-key": "qqmc",
            "Host": "qqmc.huitui.pro",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.9.3"
        }
        self.headers_p = {
            "Authorization": self.token,
            "X-Version-Code": "105",
            "X-Platform": "android",
            "X-System": "11",
            "X-Brand": "Redmi",
            "X-Device-ID": self.device,
            "X-Client-Id": "com.yourong.app.qqmc",
            "distributor-key": "qqmc",
            "Content-Type": "application/json; charset=UTF-8",
            "Host": "qqmc.huitui.pro",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.9.3"
        }

    def get_nonce(self):
        characters = string.ascii_lowercase + string.digits
        self.nonce = ''
        for _ in range(32):
            self.nonce += random.choice(characters)
    def get_md5(self,message):
        md5 = hashlib.md5()
        md5.update(message.encode('utf-8'))
        return md5.hexdigest()

    def tasks(self):
        url = "http://qqmc.huitui.pro/tasks"
        response = requests.get(url, headers=self.headers_g)
        if response.json().get('code') == 200001:
            print('获取任务列表成功')
            self.task_list = {}
            for tasks in response.json().get('data').get('tasks'):
                if tasks.get('finished'):
                    continue
                if tasks.get('id') == 1 or tasks.get('id') == 2:
                    self.task_list[tasks.get('name')] = tasks.get('id')
        else:
            print(f"获取任务失败：{response.json().get('message')}")
    
    def daily(self,k):
        t = str(int(time.time()*1000))
        self.get_nonce()
        if self.task_list[k] == 1:
            if len(self.device) <= 16:
                message = f"{self.device}&{self.task_list[k]}&{t}&{self.nonce}&T50uedlIX0fsgr5i0cGQdriBjmSAiLqC&com.yourong.app.qqmc"
            else:
                message = f"{self.task_list[k]}&{t}&{self.nonce}&{self.device}&T50uedlIX0fsgr5i0cGQdriBjmSAiLqC&com.yourong.app.qqmc"
        elif self.task_list[k] == 2:
            if len(self.device) <= 16:
                message = f"{self.device}&{t}&{self.task_list[k]}&{self.nonce}&T50uedlIX0fsgr5i0cGQdriBjmSAiLqC&com.yourong.app.qqmc"
            else:
                message = f"{t}&{self.task_list[k]}&{self.nonce}&{self.device}&T50uedlIX0fsgr5i0cGQdriBjmSAiLqC&com.yourong.app.qqmc"
        # print(message)
        md5 = self.get_md5(message)
        url = "http://qqmc.huitui.pro/tasks/complete"
        data = {
            "sign": md5,
            "id": self.task_list[k],
            "nonce": self.nonce,
            "timestamp": t
        }
        response = requests.post(url, headers=self.headers_p, json=data)
        # print(response.json())
        if response.json().get('code') == 200001:
            print(f"[{k}]任务成功，获得金币：{response.json().get('data').get('reward')}")
            time.sleep(random.randint(30,40))
            self.daily(k)
        else:
            print(f"[{k}]任务失败：{response.json().get('message')}")
            if "验签异常" in response.json().get('message'):
                time.sleep(random.randint(30,40))
                self.daily(k)
    
    def collect(self):
        t = str(int(time.time()*1000-1))
        self.get_nonce()
        message = f"1&{t}&{self.nonce}&{self.device}&T50uedlIX0fsgr5i0cGQdriBjmSAiLqC&com.yourong.app.qqmc"
        md5 = self.get_md5(message)
        url = "http://qqmc.huitui.pro/lucky_cats/fast_collect"
        data = {
            "sign": md5,
            "mode": 1,
            "nonce": self.nonce,
            "timestamp": t
        }
        response = requests.post(url, headers=self.headers_p, json=data)
        if response.json().get('code') == 200001:
            print("一键收取元宝成功")
        else:
            print(f"一键收取元宝失败：{response.json().get('message')}")
            if "验签异常" in response.json().get('message'):
                time.sleep(5)
                self.collect()
    
    def bay_cat(self):
        headers = {
            "Authorization": self.token,
            "X-Version-Code": "105",
            "X-Platform": "android",
            "X-System": "11",
            "X-Brand": "Redmi",
            "X-Device-ID": self.device,
            "X-Client-Id": "com.yourong.app.qqmc",
            "distributor-key": "qqmc",
            "Content-Length": "0",
            "Host": "qqmc.huitui.pro",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.9.3"
        }
        url = "http://qqmc.huitui.pro/lucky_cats/purchase"
        response = requests.post(url, headers=headers)
        if response.json().get('code') == 200001:
            print("购买喵喵成功")
        else:
            print(f"购买喵喵失败：{response.json().get('message')}")

    
    def cat_info(self):
        url = "http://qqmc.huitui.pro/lucky_cats/info"
        response = requests.get(url, headers=self.headers_g)
        if response.json().get('code') == 200001:
            self.jinbi = float(response.json().get('data').get('walletGold').get('balance'))
            self.yuanbao = response.json().get('data').get('walletIngot').get('balance')
        else:
            print(f"获取信息失败：{response.json().get('message')}")
            
    def main(self):
        self.tasks()
        if self.task_list != {}:
            print('==============开始任务：日常任务==============')
            for k in self.task_list:
                self.daily(k)
        print('==============开始任务：收取元宝==============')
        self.collect()
        self.cat_info()
        if self.jinbi > 3000:
            print('==============开始任务：购买喵喵==============')
            for i in range(int(self.jinbi/3000)):
                self.bay_cat()
                time.sleep(2)


if __name__ in "__main__":
    token = os.getenv('token_qqmc')
    if not token:
        print('请检查环境变量token_qqmc')
        exit()
    tokens = token.split('@')
    print(f'共有{len(tokens)}个账号')
    if thread_TF:
        print('多线程已开启')
        threads = []
        for i,token in enumerate(tokens):
            print(f'----------开始第{i+1}个账号----------')
            main = qqmc(token)
            thread = threading.Thread(target=main.main)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
    else:
        for i,token in enumerate(tokens):
            print('多线程已关闭')
            print(f'----------开始第{i+1}个账号----------')
            try:
                main = qqmc(token)
                main.main()
            except:
                pass
            print(f'----------结束第{i+1}个账号----------')
            time.sleep(random.randint(10,20))

