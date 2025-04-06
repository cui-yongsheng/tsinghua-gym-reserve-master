import logging
from function.function import test_refresh_field, login, confirm, get_free_field, chose_filed_book, screen_shot_text, exception_hand, remind, send_text, change_captcha
from selenium.webdriver.common.by import By
from selenium import webdriver
from experiments.Model import Model
import time
import sys
import torch
import string
from function.log import Logger
import traceback

# 参数设置
characters = string.digits + string.ascii_lowercase + string.ascii_uppercase
url = "https://50.tsinghua.edu.cn/j_spring_security_check?"         # 体育管理系统预约界面
wait_time = 0.5                                                     # 设置操作间隔时间
user_nm = '2023310690'                                              # 用户名
user_pw = 'CYScys20010522'                                          # 密码
data = '2024-12-08'
path = 'yzm.png'

'''
气膜馆 3998000      羽毛球场 4045681
综合体育馆 4797914   羽毛球场 4797899
西体育馆 4836273     羽毛球场 4836196 台球 14567218
体育馆 5843934      紫荆网球场 5845263 东网球场 20974500
北体育馆 20034171    乒乓球场 20035114 网球场 20035938
'''

index = 0
gyms = ['3998000', '4797914', '4836273']
sports = ['4045681', '4797899', '4836196']
# gyms = ['4836273']
# sports = ['14567218']
gym = gyms[index]
sport = sports[index]
reserve_time = [-1, -2, -3, -4]              #目前定位最后三行

#实例化
driver = webdriver.Edge()          # 使用Edge浏览器，需要下载Edge驱动
model = Model(62, input_shape=(3, 64, 192))
model=torch.load('./model/ctc_kaptcha.pth',map_location=torch.device('cpu'))
model.eval()

logger = Logger("test.log", logging.INFO, __name__).getlog()
def exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("未处理的异常: %s", str(exc_value), exc_info=(exc_type, exc_value, exc_traceback))
# 设置自定义的异常处理器
sys.excepthook = exception_handler
logger.info("######################")


# 实例浏览器类别
driver.get(url)                                                 # 访问登录界面
driver.implicitly_wait(wait_time*20)                            # 等待浏览器响应，弹性等待时间
driver.maximize_window()                                        # 最大化浏览器
time.sleep(wait_time)
#登录
login(driver, user_nm, user_pw)
time.sleep(wait_time)
confirm(driver)
time.sleep(wait_time)

#检查表格是否刷新
while 1:
    is_refresh = test_refresh_field(driver,gym,sport,data,reserve_time)
    if is_refresh:
        break
    else:
        time.sleep(0.2)
logger.info('!!!!开始抢!!!!')
re = 1
while index < 3:
    logger.info('当前体育馆'+str(index))
    while re != 0:
        gym = gyms[index]
        sport = sports[index]
        lst = get_free_field(driver, gym, sport, data, reserve_time)
        logger.info('当前体育馆' + str(index)+'空闲:'+str(len(lst)))
        if len(lst) == 0:
            index += 1
            break
        # 选择场地+预约
        chose_filed_book(driver, gym, sport, data, lst)
        logger.info('选择场地成功')
        time.sleep(wait_time)
        if index < 2:
            button = driver.find_element(By.CSS_SELECTOR,"#selectPayWay0")
            button.click()
        bbox = screen_shot_text(driver, path, model, characters)
        while len(bbox) != 4:
            #切换验证码
            change_captcha(driver)
            logger.info('切换验证码')
            bbox = screen_shot_text(driver, path, model, characters)
        send_text(driver, bbox)
        logger.info('已输入验证码')
        time.sleep(wait_time)
        re = exception_hand(driver)

        if re == 2:
            index = 3
            break
    if re == 0:
        logger.info('验证码正确')
        break

if index == 3:
    logger.info("无空闲场地")
    driver.quit()
    sys.exit(0)

if index == 2:
    #不需要发票
    button = driver.find_element(By.CSS_SELECTOR,"#xm4")
    button.click()
    time.sleep(wait_time)
    #稍后支付
    button = driver.find_element(By.CSS_SELECTOR,"#payLater")
    button.click()
#微信提醒
# remind()

