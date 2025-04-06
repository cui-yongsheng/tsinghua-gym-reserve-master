#微信提醒预约成功
import requests
api = "https://sc.ftqq.com/SCT206826TP6Y3Ya9rGWmEBmDpazSEXZjU.send"
title = u"紧急通知"
content = """
#预约成功！
##请尽快支付
"""
data = {
   "text":title,
   "desp":content
}
req = requests.post(api,data = data)