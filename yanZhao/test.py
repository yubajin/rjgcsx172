import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from config import *
from bs4 import BeautifulSoup

browser = webdriver.Chrome()
# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(chrome_options=chrome_options)

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def index_page():
    """
    抓取索引页
    """
    try:
        url = 'http://www.jxufe.cn/'
        browser.get(url)
        get_products()
    except TimeoutException:
        print("爬取院校失败")


def get_products():
    """
    提取商品数据
    """
    html = browser.page_source
    doc = pq(html)
    print('doc:',doc)
    items = doc('.centerInner ul li').items()

    for item in items:
        print("##############################################################################################################")
        print(item)
        print("##############################################################################################################")
        #
        # print('item',item.find('a:first'))


if __name__ == '__main__':
    # index_page()
    #
    # zsml_result_item = BeautifulSoup(str(zsml_result), 'html.parser').find('tbody')
    # zsml_result_item_tds = BeautifulSoup(str(zsml_result_item), 'html.parser').find_all('td')
    #
    # example_scope = ''
    # for zsml_result_item_td in zsml_result_item_tds:
    #     example_scope += zsml_result_item_td.get_text() + ','

    td_item = '<td>(101)思想政治理论<span class="sub-msg">见招生简章</span></td>'
    td = BeautifulSoup(td_item,'html.parser').find('td')
    td_later = td.get_text()
    print(td)
    print(td_later.replace('\n','').replace(' ','').replace('见招生简章',''))
    pass


