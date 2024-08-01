#2024-08-01 16:30:41
import requests
import time
import os
import uuid
import random
code="樱桃生活"
ver="2.0"
envname="yuanshen_ytsh"
split_chars=['@','&','\n']
debug=False
debugcookie=""
def env(*args,**kwargs):
 def split_cookies(cookie,split_chars):
  for sep in split_chars:
   if sep in cookie:
    return cookie.split(sep)
  return[cookie]
 def scmain(cookies):
  for i,cookie in enumerate(cookies,1):
   print(f"--------开始第{i}个账号--------")
   main=yuanshen(cookie)
   main.main()
   print(f"--------第{i}个账号执行完毕--------")
 if not os.getenv(envname)and not debug:
  print(f"请先设置环境变量[{envname}]")
  exit()
 cookie=os.getenv(envname,"")
 if debug:
  cookie=debugcookie
 try:
  print(requests.get("https://gitee.com/HuaJiB/yuanshen34/raw/master/pubilc.txt").text,"\n\n\n")
 except:
  print("网络异常,链接公告服务器失败(gitee)，请检查网络")
  exit()
 cookies=split_cookies(cookie,split_chars)
 account_count=len(cookies)
 print(f"一共获取到{account_count}个账号")
 print(f"=========🔔开始执行[{code}][{ver}]=========\n")
 start_time=time.time()
 if debug:
  scmain(cookies)
 else:
  try:
   scmain(cookies,*args,**kwargs)
  except Exception as e:
   print(f"脚本执行出错: {e}")
 end_time=time.time()
 execution_time=end_time-start_time
 print(f"\n============🔔脚本[{code}]执行结束============")
 print(f"本次脚本总运行时间: [{execution_time:.2f}] 秒")
class yuanshen:
 def __init__(self,cookie)->None:
  self.headers={"token":cookie,"user-agent":"Mozilla/5.0 (Linux; Android 14; 23113RKC6C Build/UKQ1.230804.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/118.0.0.0 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/34.285713)","Content-Type":"application/json","Content-Length":"2","Host":"ap.svms.cn","Connection":"Keep-Alive","Accept-Encoding":"gzip"}
 def sign(self):
  url='http://ap.svms.cn/api/user/sign'
  r=requests.post(url,headers=self.headers,json={}).json()
  if r['code']==1:
   print(f"签到成功[{r['msg']}]")
  else:
   print(f"签到失败[{r['msg']}]")
 def addwater(self):
  try:
   i=0
   for _ in range(3):
    i+=1
    url="http://ap.svms.cn/api/circle/send_ad"
    uuidstr=str(uuid.uuid4()).replace("-","")
    data={'type':'video_sign','uuid':uuidstr}
    r=requests.post(url,headers=self.headers,json=data).json()
    if r['isValid']:
     print(f"第[{i}]次视频广告领水滴成功！")
    else:
     print(f"第[{i}]次视频广告领水滴失败！")
     break
    time.sleep(random.randint(30,40))
  except:
   print("实名了吗你就跑。。。nm")
 def use_water(self):
  self.userinfo()
  url='http://ap.svms.cn/api/user/use_fl'
  r=requests.post(url,headers=self.headers,json={}).json()
  if r['code']==1:
   print(f"使用肥料成功[{r['msg']}]")
  else:
   print(f"使用肥料失败[{r['msg']}]")
  time.sleep(3)
  url="http://ap.svms.cn/api/user/getFruit"
  r=requests.post(url,headers=self.headers,json={}).json()
  if r['code']==1:print(f"收获樱桃成功颗")
  else:print(f"收获樱桃失败[{r['msg']}]")
 def userinfo(self,showinfo=False):
  url='http://ap.svms.cn/api/user/info'
  r=requests.post(url,headers=self.headers,json={}).json()
  if r['code']==1:
   fruit=r["data"]["fruit"]
   gold=r["data"]["water"]
   treenum=r["data"]["feed"]
   if showinfo:print(f"账号[{r['data']['nickname']}]  剩余樱桃[{fruit}] 剩余樱桃树[{treenum}] 剩余金币[{gold}]")
   buynum=int((float(gold))/3)
   if buynum>0:
    url='http://ap.svms.cn/api/user/trans_feed'
    data={"num":f"{buynum}","type":1}
    r=requests.post(url,headers=self.headers,json=data).json()
    if r['code']==1:
     print(f"兑换[{buynum}]个樱桃树成功！")
    else:
     print(f"兑换[{buynum}]个樱桃树失败！[{r['msg']}]")
  else:
   print(f"获取账号信息失败[{r['msg']}]")
 def main(self):
  self.sign()
  self.addwater()
  print("="*40)
  self.use_water()
  print("="*40)
  self.userinfo(showinfo=True)
if __name__=='__main__':
 env()
