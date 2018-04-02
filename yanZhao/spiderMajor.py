import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from config import *
from bs4 import BeautifulSoup
from selectQuery import *

class SpiderMajor:
    MONGO_COLLECTION = "majors"
    browser = webdriver.Chrome()

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # browser = webdriver.Chrome(chrome_options=chrome_options)

    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]


    def index_page(self,schoolName,url):
        """
        抓取索引页
        """
        cookies = ''
        try:
            SpiderMajor.browser.get(url)
            cookies = SpiderMajor.browser.get_cookies()
            if cookies == '' or cookies == None:
                SpiderMajor.browser.add_cookie(cookies)
            html = SpiderMajor.browser.page_source
            doc = pq(html)

            soup = BeautifulSoup(str(doc), 'html.parser')
            tbodyRaw = soup.find('tbody')
            trs = BeautifulSoup(str(tbodyRaw), 'html.parser').find_all('tr')

            for item in trs:
                # print('item\n', item)

                major = {
                    'school':schoolName,
                    'department':item.find_all('td')[0].get_text(),
                    'marjor': item.find_all('td')[1].get_text(),
                    'direction': item.find_all('td')[2].get_text(),
                    'details_link': 'http://yz.chsi.com.cn/'+ item.find_all('td')[6].find('a').get('href')
                }
                print(major)
                self.save_to_mongo(major)

        except TimeoutException:
            print("爬取院校失败")

    def save_to_mongo(self,result):
            """
            保存至MongoDB
            :param result: 结果
            """
            try:
                if SpiderMajor.db[SpiderMajor.MONGO_COLLECTION].insert(result):
                    print('存储到MongoDB成功')
            except Exception:
                print('存储到MongoDB失败')


    def main(self,schoolName,url):
        self.index_page(schoolName,url)


if __name__ == '__main__':
    spiderMajor = SpiderMajor()

    query = Query()
    major_links = query.query_majors()
    for major_link in list(major_links):
        print(major_link)
        url = major_link['link']
        id = major_link['id']
        schoolName = major_link['school']
        spiderMajor.main(schoolName,url)

