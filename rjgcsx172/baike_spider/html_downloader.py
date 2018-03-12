'''
Created on 2017年8月8日

@author: Administrator
'''
import urllib.request

class HtmlDownloader():
    
    
    def download(self,url):
        if url is None:
            return None
        
        response = urllib.request.urlopen(url)
        
        if response.getcode() != 200:#########getCode()
            return None
        
        return response.read()
    
    



