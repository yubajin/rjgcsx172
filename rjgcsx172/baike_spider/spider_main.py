import url_manager
import html_downloader
import html_parser
import html_outputer
import pymysql.cursors

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutput()

    
    def craw(self, root_url):

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='123456',
                                     db='wikiurl',
                                     charset='utf8')

        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                
                html_cont = self.downloader.download(new_url)
                #返回urls_node
                new_urls, new_data = self.parser.parse(new_url,html_cont, connection)

                self.urls.add_new_urls(new_urls)

                print('以上爬的是----->%d title: %s,url:%s页面' %(count, new_data['title'], new_url,))

                try:
                    # 获取会话指针
                    with connection.cursor() as cursor:
                        sql = "insert into urls(id, urlname, urlhref) values(%.2f, '%s','%s')"
                        data = (count, new_data['title'], new_url)
                        cursor.execute(sql % data)
                        connection.commit()
                except:
                    print('insert urls errors')

                
                self.outputer.collect_data(new_data)

                if count == 100:
                    connection.close()
                    break
                count = count + 1
            except:
                print('craw failed')
        
        self.outputer.output_html()
    
    
if __name__=='__main__':
    root_url = 'https://baike.baidu.com/item/Python/407313?fr=aladdin'
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)