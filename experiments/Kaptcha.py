import kaptcha
x, image = kaptcha.Captcha(width=1200,  # 验证码的宽度 px
                 height=300,  # 验证码的高度 px
                 chips=1,  # 干扰点 强度(1-20)
                 mode="L",  # 色彩模式 RGB\L
                 imageObj=True,  # 返回 PIL.Image 格式
                 gif=False,  # gif 格式验证码(不可与imageObj同为真)
                 bg="white",  # 背景颜色 颜色代码或 16 进制
                 contour=False,  # 以下四个滤镜只可开启一个
                 enhance=False,
                 edge=False,
                 emboss=False
                 ).letter_digit(length=4)

image.show()