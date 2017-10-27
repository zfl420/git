import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq  # 导入 PyQuery 并重命名为 pq
from config import *   # 引入 config.py 里面的所有变量
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]   #链接到 MONGODB


browser = webdriver.PhantomJS()    # 调用 PhantomjS 浏览器, 调试阶段用chrome。调试好了就用PhantomjS 无界面浏览器
wait = WebDriverWait(browser, 10)  # 浏览器等待传入 wait

browser.set_window_size(1400, 900)   #设置浏览器窗口大小，有些流量器窗口太小会显示不全

def search():  #定义搜索函数
    print('正在搜索')  #由于没有界面，所以用这个看看状态
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )   # 拿到淘宝搜索框
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        # 拿到搜索按钮
        input.send_keys(KEYWORD)   # 在这里搜索（KEYWORD）,keyword 在config.py里面，在搜索框输入"美食"
        submit.click()   # 点击搜索按钮
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        # 等待元素（下面的页码显示区块）加载完成
        get_products() #页面完全加载好了后再调用 这个函数。此函数在下面。
        return total.text #获取加载完成的页码区块的字符串
    except TimeoutException:    # 假如上面的操作失败
        return search()   # 重新再执行一次 def search() 这个函数

def next_page(page_number):   # 定义翻页函数（传入页码）
    print('正在翻页', page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        ) # 拿到页码输入框
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        # 拿到页码后面的 确定 按钮
        input.clear() # 清除页码输入框的内容
        input.send_keys(page_number)  #输入页码
        submit.click()  # 点击确定按钮,执行翻页操作
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        # 判断上面的翻页操作是否成功，用到函数 —— 在元素中有这样的文字（text_to_be_present_in_element），当翻页成功后，判断当前的高亮页码的文字, str(page_number) 为当前要传入判定的text，用这个页码和 CSS 选择器里面你的 text 比较
        get_products() # 翻页成功后再调用一下。
    except TimeoutException:
        next_page(page_number) # 如果出错就从新执行这个请求

def get_products():  # 这个函数需要在 search() 加载完是用一次，每次 next_page(page_number) 加载完一个新的页面调用一次。
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    # 判断加载成功，id 为mainsrp-itemlist 里面的 class items 里面的 item。 如果通过了就表示所有的宝贝信息都已经加载成功了
    html = browser.page_source  # 拿到正在网页的源代码
    doc = pq(html)   # 把网页的源代码传入 doc
    items = doc('#mainsrp-itemlist .items .item').items()  # 后面调用 .items() 可以选着 doc 里面的所有 .item ，每个item是一个宝贝信息
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'), #从上面的代码获取图片(获取 class .pic 里面的.img 的属性（attr） src
            'price': item.find('.price').text(), # 从 class .price 里面获取 text
            'deal': item.find('.deal-cnt').text()[:-3], # 从class deal-cnt 里面获取 text(去掉后面3个字符）
            'title': item.find('.title').text(),  # 从名称为 title 的class 里面获取 text
            'shop': item.find('.shop').text(), #从 名称为 shop 的class里面获取 text
            'localtion': item.find('.location').text() #从名称为 localtion 的 class 里面获取 text
        }
        print(product)   # 打印单个商品信息
        save_to_mongo(product)  #保存单个商品信息到 MONGODB


def save_to_mongo(result):  # 定义保存到 MONGODB 的函数，传入 result
    try:  # 错误判断
        if db[MONGO_TABLE].insert(result):
            print('保存到 MONGO_DB成功', result)
    except Exception:  #如果出错就答应下面的文字+ result(result 是 product)
        print('存储到mongodb 错误', result)


def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))
        for i in range(2, total + 1): # 页码从第2页开始，然后是3、4、5。因为一打开就是第1页
            next_page(i)
    except Exception:   #如果出错就给错误信息
        print('错误啦')
    finally: # 不论是否出现异常，最后都要执行下面的操作
        browser.close()


if __name__ == '__main__':
    main()