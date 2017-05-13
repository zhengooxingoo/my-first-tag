# coding:utf-8
'''
    爬取搜狗微信中的100篇文章。每个网页有十篇文章的网址，翻页十页
'''
import urllib
import requests
import urllib2
from bs4 import BeautifulSoup
import os
import time
import json
import random


# parse every page
def parsePage(pa):
    articles = []
    for i in pa:  # 爬取每页中的十篇文章，一篇一篇爬取
        h3 = i.find('h3')
        if h3 != None:	
            hyperlink = h3.a['href']
            articles.append(parseArticle(hyperlink))  # 进入一篇微信相关文章
            #time.sleep(2)
    print (len(articles))
    return articles


# parse every article
def parseArticle(hyperlink):
    article = []
    content = urllib2.urlopen(hyperlink).read()
    soup = BeautifulSoup(content, 'html.parser')
    a = soup.find('div', {'class', 'rich_media_content'})
    if a != None:
        parag = a.find_all('p')
        for p in parag:
            article.append(p.text.strip().replace('\n', ''))
        return article
    else:
        return "ERROR"

#parse all pages
def crawler(urls,filepath):

    articles =[]
    #file_path = os.path.abspath(".")+'/tags/temp/tmp.txt'
    #file_path = '/home/zxingoo/supertags/tags/temp/tmp.txt'
    for url in urls:
        content = requests.get(url).content
        soup = BeautifulSoup(content, 'html.parser')       
        pa = soup.find_all('div', {'class', 'txt-box'})
        #time.sleep(2)
        articles.append(parsePage(pa))


    with open(filepath,'w') as p:
        for page_articles in articles:
            for article in page_articles:
                for word in article:
                    p.write(word.encode('utf-8'))
                p.write('\n')
    
    return u''.join(str(c) for v in articles for b in v for c in b)

if __name__ == "__main__":
    urls =[]
    keyword = u'人民的名义'
    params = {}
    params['type']= 2
    params['query'] = keyword.encode("UTF-8")
    pages = range(1, 11)
    for page in pages:
        params['page'] = page
        urls.append( 'http://weixin.sogou.com//weixin?' + urllib.urlencode(params) )
    print urls
    crawler(urls)    

