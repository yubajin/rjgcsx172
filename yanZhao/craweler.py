import requests
from pyquery import PyQuery as pq

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
response = requests.get('http://yz.chsi.com.cn/zsml/queryAction.do',stream = False)
response.encoding = 'utf-8'

cookies = response.cookies
print('cookies:',cookies)

datas = {
    'ssdm': '36',
    'dwmc':'' ,
    'mldm': '',
    'mlmc': '',
    'yjxkdm': '0835',
    'zymc': '',
    'xxfs':''
}
loginresp = requests.post('http://yz.chsi.com.cn/zsml/queryAction.do',data=datas,headers = headers,cookies=cookies,stream = False)


filename = 'content'
with open(filename, 'wb') as fd:
    for chunk in loginresp.iter_content(chunk_size=32):
        fd.write(chunk)

print(loginresp)

doc = pq(loginresp)
print('doc:',loginresp)
items = loginresp('.centerInner ul li').items()

for item in items:
    print("##############################################################################################################")
    print(item)
    print("##############################################################################################################")
    #
    # print('item',item.find('a:first'))
