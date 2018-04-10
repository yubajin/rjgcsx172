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

    def index_page(self,url,school,_985,_211,department,marjor,direction,detail_collection_save):
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

            zhaosheng_number = 0
            tuimian_number = 0
            if (len(number.split(',')) > 1):
                zhaosheng_number = number.split(',')[0].split('：')[1]
                tuimian_number = number.split(',')[1].split('：')[1]

            example_scope =  ''
            zsml_result = soup.select('.zsml-result')
            zsml_result_items = BeautifulSoup(str(zsml_result), 'html.parser').select('.zsml-res-items')
            for zsml_result_item in zsml_result_items:
                zsml_result_item_tds = BeautifulSoup(str(zsml_result_item), 'html.parser').find_all('td')

                for zsml_result_item_td in zsml_result_item_tds:
                    example_scope += zsml_result_item_td.get_text() + ','

                example_scope = example_scope.replace('\n','').replace(' ','').replace('见招生简章','')
                example_scope += ';'
            details = {
                'school':school,
                '_985':_985,
                '_211':_211,
                'department':department,
                'marjor': marjor,
                'direction': direction,
                'zhaosheng_number': zhaosheng_number,
                'tuimian_number': tuimian_number,
                'example_scope':example_scope
            }
            print(details)

            self.save_to_mongo(details,detail_collection_save)

        except TimeoutException:
            print("爬取院校失败")

    def save_to_mongo(self,result,detail_collection):
            """
            保存至MongoDB
            :param result: 结果
            """
            try:
                if SpiderDetails.db[detail_collection].insert(result):
                    print('存储到MongoDB成功')
            except Exception:
                print('存储到MongoDB失败')


    def main(self,query_db_num,detail_collection_save):
        query = Query()
        majors_collection_db = ''
        if query_db_num == 0:
            majors_collection_db = MAJORS_COLLECTION
        if query_db_num != 0:
            majors_collection_db = MAJORS_COLLECTION_P
        details_link = query.query_details(majors_collection_db)
        for detail_link in list(details_link):
            url = detail_link['url']
            _985 = detail_link['_985']
            _211 = detail_link['_211']
            school = detail_link['school']
            department = detail_link['department']
            marjor = detail_link['marjor']
            direction = detail_link['direction']
            spider.index_page(url,school,_985,_211,department,marjor,direction,detail_collection_save)


if __name__ == '__main__':
    spider = SpiderDetails()

    #爬取学硕
    # detail_collection_save = DETAILS_COLLECTION
    # spider.main(0,detail_collection_save)

    #爬取专硕
    detail_collection_save_p = DETAILS_COLLECTION_P
    spider.main(1, detail_collection_save_p)

    # number = '专业：12,其中推免：4'
    # zhaosheng_number = number.split(',')[0].split('：')[1]
    # tuimian_number = number.split(',')[1].split('：')[1]
    # print(zhaosheng_number)
    # print(tuimian_number)
