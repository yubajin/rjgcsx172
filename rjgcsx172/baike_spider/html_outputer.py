'''
Created on 2017年8月8日

@author: Administrator
'''


class HtmlOutput(object):
    def __init__(self):
        self.datas = []
    
    def collect_data(self,data):
        if data is None:
            return
        self.datas.append(data)

    
    def output_html(self):
        #python文件读写open()
        fout = open('output.html','w')
        
        fout.write('<html>')
        fout.write('<head>')
        fout.write('<meta charset="UTF-8">')
        fout.write('</head>')
        fout.write('<body>')
        fout.write('<table>')
        
        for data in self.datas:
            fout.write('<tr>')
            fout.write('<td>%s</td>' % data['url'])
            fout.write('<td>%s</td>' % data['title'].encode('UTF-8'))
            fout.write('<td>%s</td>' % data['summary'].encode('UTF-8'))
        
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
    
    
    
    



