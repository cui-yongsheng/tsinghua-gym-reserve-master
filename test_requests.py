from function.function import test_refresh_field, login, confirm, get_free_field, chose_filed_book, screen_shot_text, exception_hand, remind, send_text, change_captcha
from selenium import webdriver
from experiments.Model import Model
import time
import sys
import torch
import string
import logging
import requests

# 参数设置
url_login = 'https://50.tsinghua.edu.cn/j_spring_security_check?'
url_table = 'https://50.tsinghua.edu.cn/gymsite/cacheAction.do?ms=viewBook'
header = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
}
user_nm = '2023310690'
user_pw = 'CYScys20010522'
param = {'un': user_nm, 'pw': user_pw}
session = requests.session()
response = session.get(url=url_login, headers=header, params=param, allow_redirects=False)

gyms = ['3998000']
sports = ['4045681']
datas = ['2024-03-23']
reserve_time = [-2, -1]              #目前定位最后两行

for data in datas:
    for index in range(len(gyms)):
        gym = gyms[index]
        sport = sports[index]
        param = {'gymnasium_id':gym,'item_id':sport,'time_date':data,'userType':1}
        response = session.get(url=url_table, params=param)
        print(response.url)
# # 参数设置
# characters = string.digits + string.ascii_lowercase + string.ascii_uppercase
# wait_time = 0.2                                                     # 设置操作间隔时间
# data = '2024-03-23'
# path = 'yzm.png'
# index = 0
# gym = gyms[index]
# sport = sports[index]
#
#
# #实例化
# driver = webdriver.Edge()                                       # 使用Edge浏览器，需要下载Edge驱动
# model = Model(62, input_shape=(3, 64, 192))
# model=torch.load('./model/ctc_kaptcha.pth',map_location=torch.device('cpu'))
# model.eval()
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# fh = logging.FileHandler('test.log')
# fh.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# logger.addHandler(fh)
# logger.info("######################")
#
# # 实例浏览器类别
# driver.get(url)                                                 # 访问登录界面
# driver.implicitly_wait(wait_time*20)                            # 等待浏览器响应，弹性等待时间
# driver.maximize_window()                                        # 最大化浏览器
# time.sleep(wait_time)
# #登录
# login(driver, user_nm, user_pw)
# time.sleep(wait_time)
# confirm(driver)
# time.sleep(wait_time)
#
# #检查表格是否刷新
# while 1:
#     is_refresh = test_refresh_field(driver,gym,sport,data,reserve_time)
#     if is_refresh:
#         break
#     else:
#         time.sleep(0.1)
# logger.info('!!!!开始抢!!!!')
# re = 1
# while index < 3:
#     logger.info('当前体育馆'+str(index))
#     while re != 0:
#         gym = gyms[index]
#         sport = sports[index]
#         lst = get_free_field(driver, gym, sport, data, reserve_time)
#         logger.info('当前体育馆' + str(index)+'空闲:'+str(len(lst)))
#         if len(lst) == 0:
#             index += 1
#             break
#         # 选择场地+预约
#         chose_filed_book(driver, gym, sport, data, lst)
#         logger.info('选择场地成功')
#         time.sleep(wait_time)
#         bbox = screen_shot_text(driver,path,model,characters)
#         while len(bbox)!=4:
#             #切换验证码
#             change_captcha(driver)
#             bbox = screen_shot_text(driver,path,model,characters)
#         send_text(driver, bbox)
#         logger.info('已输入验证码')
#         time.sleep(wait_time)
#         re = exception_hand(driver)
#         if re == 2:
#             index = 3
#             break
#     if re == 0:
#         break
#
# if index == 3:
#     logger.info("无空闲场地")
#     driver.quit()
#     sys.exit(0)
#
#
# #不需要发票
# button = driver.find_element_by_css_selector("#xm4")
# button.click()
# time.sleep(wait_time)
# #稍后支付
# button = driver.find_element_by_css_selector("#payLater")
# button.click()
# #微信提醒
# remind()

