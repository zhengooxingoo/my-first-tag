#coding:utf-8
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
     
    def tearDown(self):
        self.browser.quit()
        
    def test_can_crawler_and_display_the_tags(self):
        #zxing听说有一个在线中文标签云系统
        #输入最近热点话题的关键字，就可以自动搜索100篇相关话题的微信文章
        #并将这些文章中的高频词语以及词频提取出来，生成标签云
        #她很感兴趣，就试着进入这个网站
        self.browser.get(self.live_server_url)

        #她发现网页标题和头部都包含‘中文标签云’这几个字
        self.assertIn(u'中文标签云',self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn(u'中文标签云',header_text)
        
        #应用邀请她输入关注的热点的关键词
        inputbox =self.browser.find_element_by_id('id_keywords')
     
        #她在文本框中输入了‘人民的名义’
        #最近朋友圈里这个剧很火啊，但她并没有时间来刷剧
        #让‘不明事理’的她也来看看大概讲了点啥，刷刷存在感吧
        inputbox.send_keys('人民的名义')

        #她按了回车键后，页面更新了       
        inputbox.send_keys(Keys.ENTER) 
        
        #从表格中看到微信相关文章的URL
        #看到了相关话题的高频词汇。原来，这里面有个达康阿～～
        #还看到了一幅标签云的个性的图案。她点击了图片下载
        table = self.browser.find_element_by_id('id_words_table')
        cols = table.find_elements_by_tag_name('td')
        time.sleep(40)
        self.assertIn(u'反腐',[col.text for col in cols])
        

        #她想了一下，最近白百合这事也挺火的。微信文章都会说点啥呢
        #她刷新了网页，在文本框中输入了‘’

        #页面再次更新，得到了她很满意的答案，就去睡觉了
        self.fail('Finish the test!!')
        





