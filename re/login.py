import time
import pytesseract
from PIL import Image, ImageEnhance
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import win32api
import win32con
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

# 1.打开浏览器，最大化浏览器
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('http://trace.yufengtek.com/#/login')
driver.implicitly_wait(10)


#判断元素是否存在
def isElement(identifyBy,c):
    # Determine whether elements exist
    # Usage:
    # isElement(By.XPATH,"//a")
    time.sleep(1)
    flag=None
    try:
        if identifyBy == "id":
            #self.driver.implicitly_wait(60)
            driver.find_element_by_id(c)
        elif identifyBy == "xpath":
            #self.driver.implicitly_wait(60)
            time.sleep(2)
            driver.find_element_by_xpath(c)
        flag = True
    except :
        flag = False
    finally:
        return flag

'''
----
登录
----
'''
# 用户名元素
nameElement = driver.find_element(By.NAME, 'login-name')
# 密码元素
passElement = driver.find_element(By.NAME, 'login-password')
# 验证码输入框元素
codeElement = driver.find_element(By.NAME, 'login-authcode')
# 验证图片元素
imageElement = driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div[1]/div[3]/img')

# 打印当前页面url
nowurl = driver.current_url
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
    driver.get_screenshot_as_file(screenImg)
    # 定位验证码位置,大小
    location = driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div[3]/img').location
    size = driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div[3]/img').size
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
    driver.find_element_by_class_name('login-button').click()

    time.sleep(5)
    # 打印点击登录后的url
    clickurl = driver.current_url
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
        print("进入首页")
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

# 点击退出登录
# time.sleep(5)
# driver.find_element_by_css_selector("#app > div.app-top-wrap > div.nav-buttom-right > svg.logout > g:nth-child(3) > circle").click()

time.sleep(3)
'''
--------
智慧源地
--------
'''
driver.find_element_by_xpath("//li[contains(text(),'智慧源地')]").click()
print("进入智慧源地")
time.sleep(3)
# driver.find_element_by_xpath("//input[contains(@placeholder,'请输入地名(乡镇村)')]").send_keys("竹子坝村")
# driver.find_element_by_xpath("//button[contains(@class,'iconfont')]").click()
driver.find_element_by_xpath("//li[contains(@label,'迳口村')]").click()
# 鼠标滚轮滑动
time.sleep(3)
win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, 1000)
time.sleep(2)
win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -1000)
time.sleep(2)

driver.find_element_by_xpath("//div[contains(text(),'果园导航')]").click()
time.sleep(3)
driver.find_element_by_xpath("//input[@placeholder='请输入果园名称']").send_keys("鹰嘴桃果业基地")
time.sleep(1)
driver.find_element_by_xpath("//button[@class='iconfont']").click()
time.sleep(1)
driver.find_element_by_xpath("//li[contains(text(),'鹰嘴桃果业基地')]").click()
time.sleep(5)
# 关闭果园生长模型
#driver.find_element_by_xpath("//div[contains(@class,'iconfont grow-tree-closebtn')]").click()

# driver.find_element_by_xpath("//li[contains(text(),'赣州市茅店九橙生态农业')]").click()
# time.sleep(5)
driver.find_element_by_xpath("//input[@placeholder='请输入果园名称']").clear()
print("清除成功")
time.sleep(1)
driver.find_element_by_xpath("//input[@placeholder='请输入果园名称']").send_keys("赣州市会昌县珠兰乡果园")
time.sleep(1)
driver.find_element_by_xpath("//button[@class='iconfont']").click()
time.sleep(1)
driver.find_element_by_xpath("//li[contains(text(),'赣州市会昌县珠兰乡果园')]").click()
time.sleep(5)
# 关闭果园生长模型
#driver.find_element_by_xpath("//div[contains(@class,'iconfont grow-tree-closebtn')]").click()

try:
    # 识别要悬停的元素
    ele = driver.find_element_by_xpath("//div[contains(@class,'leaflet-marker-icon google-map-cluster leaflet-zoom-animated leaflet-interactive')]")
    # 鼠标悬停至元素
    ActionChains(driver).move_to_element(ele).perform()
except NoSuchElementException:
    print("元素不存在，跳过")

time.sleep(3)
# win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, 300)
# time.sleep(2)
# win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, 300)

eleIcon = isElement("xpath", "//div[contains(@class,'leaflet-marker-icon google-map-cluster leaflet-zoom-animated leaflet-interactive')]")
if eleIcon is True:
    ele.click()
else:
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -300)

time.sleep(2)
# 点击果园生长模型
driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div[2]/div[1]/div[1]").click()
time.sleep(5)

try:
    model = driver.find_element_by_xpath("//div[contains(text(),'土壤水分')]")
    ActionChains(driver).move_to_element(model).perform()
    time.sleep(3)
except NoSuchElementException:
    print("土壤水分不存在")

try:
    model = driver.find_element_by_xpath("//div[contains(text(),'日照时长')]")
    ActionChains(driver).move_to_element(model).perform()
    time.sleep(3)
except NoSuchElementException:
    print("日照时长不存在")

try:
    model = driver.find_element_by_xpath("//div[contains(text(),'环境温度')]")
    ActionChains(driver).move_to_element(model).perform()
    time.sleep(3)
except NoSuchElementException:
    print("环境温度不存在")

# 关闭果园生长模型
driver.find_element_by_xpath("//div[contains(@class,'iconfont grow-tree-closebtn')]").click()
time.sleep(3)


'''
--------
种植分布
--------
'''
driver.find_element_by_xpath("//li[contains(text(),'种植分布')]").click()
print("进入种植分布")
time.sleep(3)

# 识别要悬停的元素
ele = driver.find_element_by_xpath("//img[contains(@class,'leaflet-marker-icon leaflet-zoom-animated leaflet-interactive')]")
# 鼠标悬停至元素并点击
ActionChains(driver).move_to_element(ele).perform()
time.sleep(3)
# win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, 300)
# time.sleep(2)
# win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, 300)
ele.click()
time.sleep(3)

'''
--------
农事活动
--------
'''
driver.find_element_by_xpath("//li[contains(text(),'农事活动')]").click()
print("进入农事活动")
time.sleep(2)

driver.find_element_by_xpath("//*[@id='app']/div[3]/section[2]/div/div[2]/div/div/div[1]/div/div[3]/div[1]").click()

# 识别要悬停的元素
ele = driver.find_element_by_xpath("//*[@id='app']/div[1]/div[1]/div[4]/img[3]")
# 鼠标悬停至元素并点击
ActionChains(driver).move_to_element(ele).perform()
time.sleep(3)
ele.click()
time.sleep(3)


'''
--------
产品行情
--------
'''
driver.find_element_by_xpath("//li[contains(text(),'产品行情')]").click()
print("进入产品行情")
time.sleep(2)

# 识别要悬停的元素
ele = driver.find_element_by_xpath("//*[@id='app']/div[1]/div[1]/div[4]/img[3]")
# 鼠标悬停至元素并点击
ActionChains(driver).move_to_element(ele).perform()
time.sleep(3)
ele.click()
time.sleep(3)

# driver.switch_to.frame()

'''
--------
区块链溯源
--------
'''
driver.find_element_by_xpath("//li[contains(text(),'区块链溯源')]").click()
print("进入区块链溯源")
time.sleep(3)
# 点击‘全国溯源分布’
driver.find_element_by_xpath("//*[@id='app']/div[3]/section[3]/div/span[1]").click()
time.sleep(3)
# 点击图标选择日期
driver.find_element_by_xpath("//*[@id='app']/div[3]/section[2]/div/div[2]/div/div[1]/div[1]/input").click()
time.sleep(1)
driver.find_element_by_xpath("//span[contains(text(),'4 月') and @class='el-date-picker__header-label']").click()
time.sleep(1)
driver.find_element_by_xpath("//a[contains(text(),'三月')]").click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[2]/table[1]/tbody/tr[6]/td[3]/div/span").click()
time.sleep(3)

try:
    driver.find_element_by_xpath("//div[contains(text(),'2020-03-24')]").click()
except (NoSuchElementException, ElementNotInteractableException):
    print("2020-03-24不存在")
time.sleep(1)
try:
    driver.find_element_by_xpath("//div[contains(text(),'2020-03-23')]").click()
except (NoSuchElementException, ElementNotInteractableException):
    print("2020-03-23不存在")
time.sleep(1)
try:
    driver.find_element_by_xpath("//div[contains(text(),'2020-03-22')]").click()
except (NoSuchElementException, ElementNotInteractableException):
    print("2020-03-22不存在")
time.sleep(1)
try:
    driver.find_element_by_xpath("//div[contains(text(),'2020-03-21')]").click()
except (NoSuchElementException, ElementNotInteractableException):
    print("2020-03-21不存在")
time.sleep(1)
print('结束')
driver.quit()



