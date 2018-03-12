'''
Created on 2017年8月8日

@author: Administrator
'''

from bs4 import BeautifulSoup
import re
import urllib.parse

class HtmlParser(object):
    

    def _get_new_urls(self, page_url, soup, connection):
        new_urls = set()
        #https://baike.baidu.com/item/Python/407313?fr=aladdin
        links = soup.find_all('a', href=re.compile(r'/item/'))
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(page_url, new_url)

            print(link.get_text(),'---->',new_full_url,'已加入要爬取队列')

            try:
                # 获取会话指针
                with connection.cursor() as cursor:
                    sql = "insert into newurls(title, url) values('%s','%s')"
                    data = (link.get_text(), new_full_url)
                    cursor.execute(sql % data)
                    connection.commit()
            except:
                print('insert newurl errors')

            new_urls.add(new_full_url)
        return new_urls
    
    
    def _get_new_data(self, page_url, soup, connection):
        res_data = {}
        
        res_data['url'] = page_url
        
        title_node = soup.find('dd',class_='lemmaWgt-lemmaTitle-title').find('h1')
        res_data['title'] = title_node.get_text()
        
        summary_node = soup.find('div',class_='lemma-summary')
        res_data['summary'] = summary_node.get_text()

        try:
            # 获取会话指针
            with connection.cursor() as cursor:
                sql = "insert into info(url, title, summary) values('%s', '%s','%s')"
                data = (res_data['url'], res_data['title'], res_data['summary'])
                cursor.execute(sql % data)
                connection.commit()
        except:
            print('insert into info errors')

        return res_data
    
    def parse(self, page_url, html_cont, connection):
        if page_url is None or html_cont is None:
            return
        
        soup = BeautifulSoup(html_cont,'html.parser')#############html_parser

        new_urls = self._get_new_urls(page_url, soup, connection)
        new_data = self._get_new_data(page_url, soup, connection)
        
        return new_urls, new_data
    



