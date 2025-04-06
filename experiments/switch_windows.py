# coding=utf-8
from selenium import webdriver
import time

# 参数设置
url = "https://50.tsinghua.edu.cn/j_spring_security_check?"     # 体育管理系统预约界面
wait_time = 1                                                   # 设置操作间隔时间
user_nm = '2023310690'                                          # 用户名
user_pw = 'CYScys20010522'                                      # 密码
# 待处理：预约时间，预约时间段，预约场地

# 实例浏览器类别
browser = webdriver.Edge()                                       # 使用Edge浏览器，需要下载Edge驱动
browser.get('https://www.baidu.com')  # 在当前浏览器中访问百度
browser.get('https://www.sogou.com')  # 在当前浏览器中访问百度

import time

time.sleep(10)
browser.quit()