import time
import pytesseract
from PIL import Image, ImageEnhance
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re,unittest

class traceTestDemo(unittest.TestCase):

    def setUp(self):
        '''
        前置条件准备，准备浏览器
        :return:
        '''
        # 1.打开浏览器，最大化浏览器
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get('http://trace.yufengtek.com/#/login')
        self.driver.implicitly_wait(10)

    # def tearDown(self):
    #     '''
    #     测试结束，关闭浏览器
    #     :return:
    #     '''
    #     # print('结束')
    #     # time.sleep(3)
    #     # self.driver.quit()

    '''
    登录
    '''
    def test_login(self):
        # 用户名元素
        nameElement = self.driver.find_element(By.NAME, 'login-name')
        # 密码元素
        passElement = self.driver.find_element(By.NAME, 'login-password')
        # 验证码输入框元素
        codeElement = self.driver.find_element(By.NAME, 'login-authcode')
        # 验证图片元素
        imageElement = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div[1]/div[3]/img')

        # 打印当前页面url
        nowurl = self.driver.current_url
        print("nowurl："+nowurl)

        '''
        beforehttp = driver.current_url
        print("beforehttp:"+beforehttp)
        '''

        nameElement.send_keys('admin')
        passElement.send_keys('admin')

        while True:
            # 截图保存到本地
            screenImg = "D:/imagesDemo/screenImg.png"
            # 浏览器截屏
            self.driver.get_screenshot_as_file(screenImg)
            # 定位验证码位置,大小
            location = self.driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div[3]/img').location
            size = self.driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div[3]/img').size
            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']
            # 从文件读取截图，截取验证码位置再次保存
            img = Image.open(screenImg).crop((left, top, right, bottom))
            # 图片处理
            img = img.convert('RGBA')  # 转换模式：L | RGB
            img = img.convert('L')  # 转换模式：L | RGB
            img = ImageEnhance.Contrast(img)  # 增强对比度
            img = img.enhance(2.0)  # 增加饱和度
            img.save(screenImg)
            # 再次读取识别验证码
            img = Image.open(screenImg)
            code = pytesseract.image_to_string(img)
            # 打印识别的验证码
            print(code.strip())
            # 识别验证码去特殊符号-加工-正则表达式
            b = ''
            for i in code.strip():
                pattern = re.compile(r'[a-zA-Z0-9]')
                m = pattern.search(i)
                if m != None:
                    b += i
                # 输出去特殊符号以后的验证码
                print(b)
                time.sleep(1)

            '''
            # 2、截取屏幕内容，保存到本地
            driver.get_screenshot_as_file(u"D:\\imagesDemo\\01.png")
         
            # 3、打开截图，获取验证码位置，截取保存验证码
            ran = Image.open("D:\\imagesDemo\\01.png")
            box = (483, 494, 595, 544)  # 获取验证码位置,自动定位不是很明白，就使用了手动定位，代表（左，上，右，下）
            ran.crop(box).save("D:\\imagesDemo\\02.png")
        
            # 4、获取验证码图片，读取验证码
            imageCode = Image.open("D:\\imagesDemo\\02.png") # 图像增强，二值化
            # imageCode.load()
            sharp_img = ImageEnhance.Contrast(imageCode).enhance(2.0)
            sharp_img.save("D:\\imagesDemo\\03.png")
            sharp_img.load()  # 对比度增强
            code = pytesseract.image_to_string(sharp_img).strip()
            newcode = code.replace(" ", "")
            '''

            # 收到验证码，进行输入验证并点击登录
            print(b)
            time.sleep(2)
            codeElement.send_keys(b)
            time.sleep(1)
            self.driver.find_element_by_class_name('login-button').click()

            time.sleep(3)
            # 打印点击登录后的url
            clickurl = self.driver.current_url
            print("clickurl："+clickurl)

            '''
            rearhttp = driver.current_url
            print("rearhttp："+rearhttp)
            '''

            # 判断
            if nowurl==clickurl:
                print("验证码错误")
                time.sleep(1)
                codeElement.send_keys(Keys.CONTROL, "a")
                codeElement.send_keys(Keys.DELETE)
            else:
                print("登录成功")
                break

            '''
            if beforehttp == rearhttp:
                print("登录失败")
                # 清空验证码
                time.sleep(1)
                driver.find_element_by_name('login-authcode').send_keys(Keys.CONTROL, "a")
                driver.find_element_by_name('login-authcode').send_keys(Keys.DELETE)
            else:
                print("登录成功")
                break
        
            flag = isElement("xpath", "//*[@id='app']/div[3]/div[1]/div[3]/img")
            print(flag)
            if flag is True:
                print("验证码错误")
                print(flag)
                time.sleep(1)
                codeElement.send_keys(Keys.CONTROL, "a")
                codeElement.send_keys(Keys.DELETE)
            else:
                print("进入首页")
                print(flag)
                break
            '''


if __name__=='__main__':
    unittest.main()





