import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from config import *
from bs4 import BeautifulSoup
from selectQuery import *

class SpiderDetails:
    DETAILS_COLLECTION = "details"
    browser = webdriver.Chrome()
    # browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # browser = webdriver.Chrome(chrome_options=chrome_options)

    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]

    def __init__(self):
        self.url = set()
        self.majorId = set()

    def index_page(self,url,school,department,marjor,direction):
        """
        抓取索引页
        """
        try:
            SpiderDetails.browser.get(url)
            html = SpiderDetails.browser.page_source
            doc = pq(html)
            soup = BeautifulSoup(str(doc), 'html.parser')

            zsml_condition = soup.select('.zsml-condition')
            zsml_summmary = BeautifulSoup(str(zsml_condition), 'html.parser').find_all('tr')[4]
            number = BeautifulSoup(str(zsml_summmary), 'html.parser').find_all('td')[1].get_text()

            zhaosheng_number = number.split(',')[0].split('：')[1]
            tuimian_number = number.split(',')[1].split('：')[1]

            zsml_result = soup.select('.zsml-result')
            zsml_result_item = BeautifulSoup(str(zsml_result), 'html.parser').find('tbody')
            zsml_result_item_tds = BeautifulSoup(str(zsml_result_item), 'html.parser').find_all('td')

            example_scope =  ''
            for zsml_result_item_td in zsml_result_item_tds:
                example_scope += zsml_result_item_td.get_text() + ','

            details = {
                'school':school,
                'department':department,
                'marjor': marjor,
                'direction': direction,
                'number':number,
                'zhaosheng_number': zhaosheng_number,
                'tuimian_number': tuimian_number,
                'example_scope':example_scope
            }
            print(details)

            self.save_to_mongo(details)

        except TimeoutException:
            print("爬取院校失败")

    def save_to_mongo(self,result):
            """
            保存至MongoDB
            :param result: 结果
            """
            try:
                if SpiderDetails.db[SpiderDetails.DETAILS_COLLECTION].insert(result):
                    print('存储到MongoDB成功')
            except Exception:
                print('存储到MongoDB失败')


    # def main(self,url,majorId):
    #     self.index_page(majorId,url)


if __name__ == '__main__':
    spider = SpiderDetails()

    query = Query()
    details_link = query.query_details()
    for detail_link in list(details_link):
        url = detail_link['url']
        school = detail_link['school']
        department = detail_link['department']
        major = detail_link['marjor']
        direction = detail_link['direction']
        spider.index_page(url,school,department,major,direction)

    # number = '专业：12,其中推免：4'
    # zhaosheng_number = number.split(',')[0].split('：')[1]
    # tuimian_number = number.split(',')[1].split('：')[1]
    # print(zhaosheng_number)
    # print(tuimian_number)
