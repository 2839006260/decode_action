'''
添加自动孵蛋、合成
入口：http://saves.dwc.tuesjf.cn/?type=1&share_code=CRUHET
抓dwccc.tuesjf.cn接口的token ,变量名dwc_token   多个账号#隔开
token有的在url链接上，有的在请求体里，自己找
一天看8个广告得24个宠物蛋，宠物蛋拿去孵化，孵化完拿去派遣或合成或出售
里面的货币是金币，可直接兑换红包提现，也可以直接咸鱼出售
'''
import bz2
import base64
exec(bz2.decompress(base64.b64decode('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')).decode('utf-8'))