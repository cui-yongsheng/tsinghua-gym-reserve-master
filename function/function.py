from PIL import Image
from torchvision.transforms.functional import to_tensor
from selenium.webdriver.common.by import By
from experiments.Model import decode
import requests
import time
import logging
from function.log import Logger
import random

logger = Logger("test.log", logging.INFO, __name__).getlog()

def yzm_process(path,characters,model):
    '''验证码处理，包含图片的裁剪和识图，输出识别文本和置信率'''
    #识图
    image = Image.open(path)
    image = image.resize((192, 64), Image.LANCZOS)
    image = to_tensor(image.convert("RGB"))
    output = model(image.unsqueeze(0))
    output_argmax = output.detach().permute(1, 0, 2).argmax(dim=-1)
    result = decode(output_argmax[0],characters)
    logger.info('验证码处理成功：返回结果'+str(result))
    return result

def test_refresh_field(driver,gym,sport,data,reserve_time):
    '''测试表格是否刷新'''
    driver.get("https://50.tsinghua.edu.cn/gymsite/cacheAction.do?ms=viewBook&gymnasium_id=%s&item_id=%s&time_date=%s&userType=1" % (gym, sport, data))  # 访问指定时间、场地和运动
    t_body = driver.find_element(By.TAG_NAME,'tbody')  # 定位表格主体
    tr_list = t_body.find_elements(By.TAG_NAME,'tr')  # 定位表格每一行
    td_list = tr_list[reserve_time[0]].find_elements(By.TAG_NAME,'td')  # 定位表格每个单元格
    td = td_list[0]
    if td.get_attribute('time_date') != data:
        return False
    return True

def get_free_field(driver,gym,sport,data,reserve_time):
    '''获取剩余表格'''
    driver.get("https://50.tsinghua.edu.cn/gymsite/cacheAction.do?ms=viewBook&gymnasium_id=%s&item_id=%s&time_date=%s&userType=1" % (gym, sport, data))  # 访问指定时间、场地和运动
    t_body = driver.find_element(By.TAG_NAME,'tbody')  # 定位表格主体
    tr_list = t_body.find_elements(By.TAG_NAME,'tr')  # 定位表格每一行
    lst = []
    for i in range(len(reserve_time)):
        td_list = tr_list[reserve_time[i]].find_elements(By.TAG_NAME,'td')  # 定位表格每个单元格
        for td in td_list:
            if td.get_attribute('style') == '':  # 查找未被预定场地
                lst.append('#' + td.get_attribute('id'))
    logger.info('获取空闲表格成功')
    return lst

def chose_filed_book(driver,gym, sport, data ,lst):
    '''选择场地+预约'''
    driver.get("https://50.tsinghua.edu.cn/gymbook/gymBookAction.do?ms=viewGymBook&gymnasium_id=%s&item_id=%s&time_date=%s&userType=" % (gym, sport, data))  # 访问指定时间、场地和运动
    driver.switch_to.frame("overlayView")
    box = driver.find_element(By.CSS_SELECTOR,lst[0])
    box.click()
    driver.switch_to.parent_frame()
    button = driver.find_element(By.CSS_SELECTOR,"#box-0 > div > div > div.pull-right > span > a > span")
    button.click()


def screen_shot_text(driver,path,model,characters):
    '''截图+识别验证码'''
    img = driver.find_element(By.CSS_SELECTOR,"#selectPayWay > div.modal-body > div > label > img")
    img.screenshot(path)
    bbox = yzm_process(path,characters,model)
    return bbox

def send_text(driver,bbox):
    '''填写验证码+确定'''
    text= driver.find_element(By.CSS_SELECTOR,"#selectPayWay > div.modal-body > div > label > input")
    text.send_keys(bbox)
    button = driver.find_element(By.CSS_SELECTOR,"#selectPayWay > div.modal-footer > a:nth-child(1)")
    button.click()

def change_captcha(driver):
        '''更换验证码'''
        button = driver.find_element(By.CSS_SELECTOR,"#selectPayWay > div.modal-body > div > label > img")
        button.click()
def login(driver,user_nm,user_pw):
    '''登录界面操作'''
    text_nm = driver.find_element(By.CSS_SELECTOR,"#login_username")  # 查找用户名输入框
    text_pw = driver.find_element(By.CSS_SELECTOR,"#login_password")  # 查找密码输入框
    text_nm.send_keys(user_nm)  # 输入用户名
    text_pw.send_keys(user_pw)  # 查找密码
    button_login = driver.find_element(By.CSS_SELECTOR,"#panelLogin > div.submit.clearfix > input[type=image]")  # 登录
    button_login.click()

def confirm(driver):
    button = driver.find_element(By.CSS_SELECTOR,"#nav-main > ul > li:nth-child(3) > a")        #“场地预约”
    button.click()
    button = driver.find_element(By.CSS_SELECTOR,"#bookInfo > div > div.yuyueButton > a")       #“预约场地”
    button.click()
    time.sleep(0.5)
    button = driver.find_element(By.CSS_SELECTOR,"#attentionModal > div.modal-footer > button") #“提醒事项，同意”
    button.click()

def exception_hand(driver):
    ''' 异常处理'''
    try:
        alert = driver.switch_to.alert  # 处理alert弹出框(alert)
        if alert.text == "预定失败：预约验证码错误":
            logger.info('预约验证码错误')
            alert.accept()
            return 1
        elif alert.text == "预定失败：未到预约开放时间":
            logger.info('未到预约开放时间')
            alert.accept()
            return 2
        elif alert.text == "没有选中的预约信息":
            logger.info('没有选中的预约信息')
            alert.accept()
            return 3
        else:
            logger.info('其他错误')
            alert.accept()
            return 4
    except:
        logger.info('预定成功')
        return 0


def remind():
    '''微信提醒预约成功'''
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
    requests.post(api,data = data)