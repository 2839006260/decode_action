#2024-07-07 05:42:57

import requests
import time
import random
import os
version = "version1.2"
url0 = "https://raw.gitcode.com/wzfqingyi01/script_info/raw/main/dwc_version"
resp = requests.get(url0)
print(resp.text)
if version not in resp.text:
    exit()
start_time = int(time.time())
class dwc():
    def __init__(self,start_time,token) -> None:
        self.start_time = start_time
        self.token = token
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Linux; Android 11; Redmi K30i 5G Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/34.545456)",
            "Host": "dwccc.tuesjf.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        self.state = 0

    def look_ad(self):
        url = "http://dwccc.tuesjf.cn/apis/v1/is_vip"
        params = {
            "token": self.token
        }
        try:
            response = requests.get(url, headers=self.headers, params=params)
            print(f"判断会员：{response.json().get('msg')}")
        except Exception as e:
            print(f'判断会员异常{e}')
        time.sleep(random.randint(15,25))
        data = {
            "token": self.token
        }
        url2 = "http://dwccc.tuesjf.cn/apis/v1/lookVideo"
        try:
            response = requests.post(url2, headers=self.headers, data=data)
            msg = response.json().get('msg')
            print(f"领取蛋蛋：{msg}")
            if "次数上限" in msg:
                self.state = 1
        except Exception as e:
            print(f'领取蛋蛋异常{e}')

    def exchangedig(self):
        url = "http://dwccc.tuesjf.cn/apis/v1/exchangeDig"
        data = {
            "box_id": self.dig_id,
            "token": self.token
        }
        try:
            response = requests.post(url, headers=self.headers, data=data)
            print(f"放蛋蛋：{response.json().get('msg')}")
            self.frequency_num -= 1
        except Exception as e:
            print(f'放蛋蛋异常{e}')
    
    def get_dig(self):
        url = "http://dwccc.tuesjf.cn/apis/v1/startDig"
        data = {
            "carve_id": self.dig_id,
            "token": self.token
        }
        try:
            response = requests.post(url, headers=self.headers, data=data)
            print(f"收取蛋蛋：{response.json().get('msg')}")
        except Exception as e:
            print(f'收取蛋蛋异常{e}')
    
    def diglist(self):
        url = "http://dwccc.tuesjf.cn/apis/v1/digList"
        params = {
            "token": self.token
        }
        try:
            response = requests.get(url, headers=self.headers, params=params)
            time.sleep(5)
            for digs in response.json().get('data'):
                self.dig_id = digs.get('id')
                state = digs.get('state')
                if state != 0:
                    if "1970-01-01" in digs.get('end_time_text'):
                        print(f'蛋槽{self.dig_id}可放蛋')
                        if self.frequency_num > 0:
                            self.exchangedig()
                            time.sleep(5)
                        else:
                            print('没蛋可放')
                    else:
                        if int(time.time()) > digs.get('end_time'):
                            print(f'蛋槽{self.dig_id}已孵化完')
                            time.sleep(3)
                            self.get_dig()
                            time.sleep(5)
                            
                        else:
                            print(f'蛋槽{self.dig_id}正在孵化')
                            self.last = digs.get('end_time') - int(time.time())
        except Exception as e:
            print(f'查询蛋坑异常{e}')

    def user_info(self):
        url = "http://dwccc.tuesjf.cn/apis/v1/user_info"
        params = {
            "token": self.token
        }
        try:
            response = requests.get(url, headers=self.headers, params=params)
            self.frequency_num = response.json().get('data').get('info').get('frequency_num')
            print(f'还有[{self.frequency_num}]个蛋待孵化')
        except Exception as e:
            print(f'获取用户信息异常{e}')
    
    def sign_num(self):
        url = "http://dwccc.tuesjf.cn/apis/v1/signNunShow"
        params = {
            "token": self.token
        }
        try:
            response = requests.get(url, headers=self.headers, params=params)
            self.in_num = response.json().get('data').get('info').get('in_num')
            
        except Exception as e:
            print(f'获取用户信息异常{e}')
    
    def cws(self,ty,product_id=1):
        self.cw_list = []
        for i2 in range(5):
            url = "http://dwccc.tuesjf.cn/apis/v1/productOder"
            params = {
                "token": self.token,
                "product_id": product_id,
                "page": i2,
                "type": ty
            }
            try:
                response = requests.get(url, headers=self.headers, params=params)
                if response.json().get('data').get('list') == []:
                    break
                for i in response.json().get('data').get('list'):
                    self.cw_list.append(i)
                
            except Exception as e:
                print(f'获取派遣列表异常{e}')
    
    def hecheng(self):
        url = "http://dwccc.tuesjf.cn/apis/v1/startCompound"
        data = {
            "left_id": self.one_id,
            "right_id": self.tow_id,
            "token": self.token
        }
        try:
            response = requests.post(url, headers=self.headers, data=data)
            self.cw_list.append(response.json().get('data'))
            self.cw_list = sorted(self.cw_list, key=lambda x: x['score'])
            _type = response.json().get('data').get('type')
            if _type == 0:
                print("合成成功：获得普通宠物")
            elif _type == 1:
                print("合成成功：获得珍稀宠物")
            else:
                print(f"合成失败：{response.json().get('msg')}")
        except Exception as e:
            print(f'派遣宠物异常{e}')
    
    def main(self):
        print(f"=========开始任务：处理蛋坑=========")
        self.user_info()
        time.sleep(1)
        self.diglist()
        print(f"=========开始任务：看广告=========")
        self.sign_num()
        if self.in_num < 8:
            while True:
                self.look_ad()
                if self.state == 1:
                    break
                time.sleep(random.randint(61,66))
        else:
            print('今天的广告看完了')
        print(f"=========开始任务：继续处理蛋坑=========")
        time.sleep(3)
        self.user_info()
        time.sleep(3)
        while True:
            if self.frequency_num > 0:
                self.diglist()
                try:
                    print(f'等{self.last+2}秒')
                    time.sleep(self.last+2)
                    del self.last
                except:
                    time.sleep(2)
            else:
                break
        print(f"=========开始任务：合成宠物=========")
        time.sleep(3)
        while True:
            self.one_id = self.tow_id = 0
            self.cws(0)
            time.sleep(3)
            if len(self.cw_list) >= 2:
                self.cw_list = sorted(self.cw_list, key=lambda x: x['score'])
                for ids in self.cw_list:
                    if self.one_id == 0:
                        self.one_id = ids.get('id')
                    else:
                        self.tow_id = ids.get('id')
                        self.hecheng()
                        time.sleep(5)
                        self.one_id = self.tow_id = 0
            else:
                print('宠物数量不够合成')
                break

if __name__=='__main__':
    token=os.getenv("dwc_token")
    if not token:
        print("请检查环境变量是否存在")
        exit()
    tokens = token.split('#')
    print(f'共有{len(tokens)}个账号')
    for i,token in enumerate(tokens):
        print(f"--------开始第{i+1}个账号--------")
        main=dwc(start_time,token)
        main.main()
        print(f"--------第{i+1}个账号执行完毕--------")
        time.sleep(15)
