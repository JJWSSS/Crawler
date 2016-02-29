__author__ = 'JJW'
# -*- coding:utf-8 -*-

import urllib
from bs4 import BeautifulSoup
import re

class Tool(object):
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()

class tieba_spider(object):

    def __init__(self):
        self.file = None
        self.base_url = 'http://tieba.baidu.com/p/3877775766'
        print('贴吧爬虫开始工作....')

    def get_page(self, pagenum):
        url = self.base_url + '?pn=' + str(pagenum)
        try:
            response = urllib.request.urlopen(url)
            return response.read()
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                print('Reason: %s' % e.reason)
                return None

    def all_page_number(self):
        page = self.get_page(1)
        # print(page)
        soup = BeautifulSoup(page, 'html5lib')
        li = soup.find_all('li', class_='l_reply_num')[0]
        span = li.contents[2]
        return span.string

    def get_title(self):
        page = self.get_page(1)
        soup = BeautifulSoup(page, 'html5lib')
        # print(soup.find('h3', class_='core_title_txt pull-left text-overflow  ').string)
        return soup.find('h3', class_='core_title_txt pull-left text-overflow  ').string

    def set_file(self, filename):
        if filename is not None:
            self.file = open(filename + '.txt', 'w+', encoding='utf-8')
        else:
            self.file = open('tiebaspider.txt', 'w+', encoding='utf-8')

    def get_information(self, num):
        self.file.write('第%d页-----------------------------------------------------------------------\n' % num)
        page = self.get_page(num)
        soup = BeautifulSoup(page, 'html5lib')
        divs = soup.find_all('div', class_='l_post l_post_bright j_l_post clearfix')
        for div in divs:
            # print(div.contents, len(div.contents))
            author = div.contents[1]
            # print(author.find_all('a', class_='p_author_name j_user_card'))
            # print(author.find_all('li', class_='d_name')[0].contents)
            author_name = author.find_all('li', class_='d_name')[0].contents[1].string
            # print(author_name)
            # author_name = author_name[0].string
            cont_tag = div.contents[2]
            # print(cont_tag.find('div', class_='d_post_content j_d_post_content '))
            cont = cont_tag.find('div', class_='d_post_content j_d_post_content ').string
            if not cont:
                cont = cont_tag.find('div', class_='d_post_content j_d_post_content ').text.encode('utf-8').decode()
            # print(cont)
            tool = Tool()
            cont = tool.replace(cont)
            floor = cont_tag.find_all('span', class_='tail-info')
            if len(floor) == 3:
                floor_num = floor[1].string
            else:
                floor_num = floor[0].string
            self.file.write(u'----------------------------------------------------------\n')
            self.file.write(str(author_name) + '    ' + str(floor_num) + '\n')
            self.file.write(cont + '\n')
            # self.file.write(u'----------------------------------------------------------\n')

    def start_spider(self):
        title = self.get_title()
        self.set_file(title)
        self.file.write(title + '\n')
        all_num = self.all_page_number()
        max_page = int(all_num)
        for i in range(1, max_page+1):
            print('正在读取第%d页的内容\n' % i)
            self.get_information(i)
            print('第%d页读取完成\n' % i)
        self.file.close()

if __name__ == '__main__':
    tb = tieba_spider()
    tb.start_spider()


