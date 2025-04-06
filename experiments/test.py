from selenium import webdriver
import time
import sys
import cv2
import easyocr

def yzm_process(path,reader,path_process):
    '''验证码处理，包含图片的裁剪和识图，输出识别文本和置信率'''
    #裁剪图片
    img = cv2.imread(path)
    cropped = img[0:30, 30:100]  # 裁剪坐标为[y0:y1, x0:x1]
    cv2.imwrite(path_process, cropped)
    #识图
    result = reader.readtext(path_process)
    try:
        text, bbox, confidence = result[0]
    except:
        return 0, 0              # 返回confidence=0
    return bbox, confidence

def test_refresh_field(driver,gym,sport,data,reserve_time):
    '''测试表格是否刷新'''
    driver.get("https://50.tsinghua.edu.cn/gymsite/cacheAction.do?ms=viewBook&gymnasium_id=%s&item_id=%s&time_date=%s&userType=1" % (gym, sport, data))  # 访问指定时间、场地和运动
    t_body = driver.find_element_by_tag_name('tbody')  # 定位表格主体
    tr_list = t_body.find_elements_by_tag_name('tr')  # 定位表格每一行
    td_list = tr_list[reserve_time].find_elements_by_tag_name('td')  # 定位表格每个单元格
    td = td_list[0]
    if td.get_attribute('time_date') != data:
        return False
    return True

def get_free_field(driver,gym,sport,data,reserve_time):
    '''测试表格是否刷新'''
    driver.get("https://50.tsinghua.edu.cn/gymsite/cacheAction.do?ms=viewBook&gymnasium_id=%s&item_id=%s&time_date=%s&userType=1" % (gym, sport, data))  # 访问指定时间、场地和运动
    t_body = driver.find_element_by_tag_name('tbody')  # 定位表格主体
    tr_list = t_body.find_elements_by_tag_name('tr')  # 定位表格每一行
    td_list = tr_list[reserve_time].find_elements_by_tag_name('td')  # 定位表格每个单元格
    lst = []
    for td in td_list:
        if td.get_attribute('style') == '':  # 查找未被预定场地
            lst.append('#' + td.get_attribute('id'))
    return lst

def operate_1(driver,gym, sport, data, wait_time,lst):
    '''选择场地+预约'''
    driver.get("https://50.tsinghua.edu.cn/gymbook/gymBookAction.do?ms=viewGymBook&gymnasium_id=%s&item_id=%s&time_date=%s&userType=" % (gym, sport, data))  # 访问指定时间、场地和运动
    driver.switch_to.frame("overlayView")
    box = driver.find_element_by_css_selector(lst[0])
    box.click()
    driver.switch_to.parent_frame()
    button = driver.find_element_by_css_selector("#box-0 > div > div > div.pull-right > span > a > span")
    button.click()
    time.sleep(wait_time)

def operate_2(driver,reader,path,path_process,wait_time):
    '''截图+识别验证码'''
    img = driver.find_element_by_css_selector("#selectPayWay > div.modal-body > div > label > img")
    img.screenshot(path)
    time.sleep(wait_time / 2)
    bbox, confidence = yzm_process(path, reader, path_process)
    print(bbox)
    return bbox, confidence

def operate_3(driver,bbox,wait_time):
    '''填写验证码+确定'''
    text= driver.find_element_by_css_selector("#selectPayWay > div.modal-body > div > label > input")
    text.send_keys(bbox)
    button = driver.find_element_by_css_selector("#selectPayWay > div.modal-footer > a:nth-child(1)")
    button.click()
    time.sleep(wait_time)

def operate_4(driver,wait_time,reader, path, path_process):
    '''循环识别验证码，直到置信率大于0.8'''
    confidence = 0
    while confidence < 0.7:
        #更换验证码
        button = driver.find_element_by_css_selector("#selectPayWay > div.modal-body > div > label > img")
        button.click()
        time.sleep(wait_time/2)
        #截图
        bbox, confidence = operate_2(driver, reader, path, path_process, wait_time)
        if bbox==0 or len(bbox)!=4:
            confidence=0
    return bbox
# 参数设置
url = "https://50.tsinghua.edu.cn/j_spring_security_check?"     # 体育管理系统预约界面
wait_time = 0.4                                                # 设置操作间隔时间
user_nm = '2023310690'                                          # 用户名
user_pw = 'CYScys20010522'                                      # 密码
data = '2024-03-15'
path = 'yzm.png'
path_process = 'yzm_process.png'
'''
气膜馆 3998000      羽毛球场 4045681
综合体育馆 4797914   羽毛球场 4797899
西体育馆 4836273     羽毛球场 4836196 台球 14567218
体育馆 5843934      紫荆网球场 5845263 东网球场 20974500
北体育馆 20034171    乒乓球场 20035114 网球场 20035938
'''
index = 0
gyms = ['3998000','4797914','4836273']
sports = ['4045681','4797899','4836196']
gym = gyms[index]
sport = sports[index]
reserve_time = -1          #目前只定位最后一行

#实例化
reader = easyocr.Reader(['en'], gpu=False)                                 # OCR工具
driver = webdriver.Edge()                                       # 使用Edge浏览器，需要下载Edge驱动

# 实例浏览器类别
driver.get(url)                                                 # 访问登录界面
driver.implicitly_wait(wait_time*10)                            # 等待浏览器响应，弹性等待时间
driver.maximize_window()                                        # 最大化浏览器
time.sleep(wait_time)

# 登录界面操作
text_nm = driver.find_element_by_css_selector("#login_username")    #查找用户名输入框
text_pw = driver.find_element_by_css_selector("#login_password")    #查找密码输入框
text_nm.send_keys(user_nm)                                          #输入用户名
text_pw.send_keys(user_pw)                                          #查找密码
button_login = driver.find_element_by_css_selector("#panelLogin > div.submit.clearfix > input[type=image]")     #登录
button_login.click()
time.sleep(wait_time)

#弹出页面确认
button = driver.find_element_by_css_selector("#nav-main > ul > li:nth-child(3) > a")        #“场地预约”
button.click()
time.sleep(wait_time)
button = driver.find_element_by_css_selector("#bookInfo > div > div.yuyueButton > a")       #“预约场地”
button.click()
time.sleep(wait_time)
button = driver.find_element_by_css_selector("#attentionModal > div.modal-footer > button") #“提醒事项，同意”
button.click()
time.sleep(wait_time)

#检查表格是否刷新
while 1:
    is_refresh = test_refresh_field(driver,gym,sport,data,reserve_time)
    if is_refresh:
        break
    else:
        time.sleep(2)
flag = 1
while 1:
    while flag:
        lst = get_free_field(driver, gym, sport, data, reserve_time)
        if len(lst) == 0:
            index += 1
            if len(gyms) <= index:
                print("无空闲场地")
                sys.exit(0)
            else:
                gym = gyms[index]
                sport = sports[index]
        else:
            flag = 0
            break
    confidence = 0
    # 选择场地+预约
    operate_1(driver, gym, sport, data, wait_time,lst)
    # 循环识别验证码，直到置信率大于0.8
    bbox = operate_4(driver, wait_time, reader, path, path_process)
    #填写验证码
    operate_3(driver, bbox, wait_time)
    try:
        alert = driver.switch_to.alert  # 处理alert弹出框(alert)
        if alert.text == "预定失败：预约验证码错误":
            alert.accept()
        elif alert.text == "预定失败：未到预约开放时间":
            alert.accept()
            print("未到预约开放时间")
            sys.exit(0)
        else:
            alert.accept()
            lst = get_free_field(driver, gym, sport, data, reserve_time)
            if len(lst) == 0:
                index += 1
                if len(gyms)<=index:
                    sys.exit(0)
                else:
                    gym = gyms[index]
                    sport = sports[index]
    except:
        break


#不需要发票
button = driver.find_element_by_css_selector("#xm4")
button.click()
time.sleep(wait_time)
#稍后支付
button = driver.find_element_by_css_selector("#payLater")
button.click()
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

