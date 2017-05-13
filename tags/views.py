#coding:utf-8
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from tags.components.crawler import crawler
import sys
import urllib
import os
import numpy as np
from tags.components.freq import Keywords


from PIL import Image
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc("savefig", dpi=400)
from tags.components.color import *

import random

# 跳转到主页
def index(request):
    return render(request, 'index.html')
    

# 预览形状的图片
@csrf_exempt
def shape_img(request,imgName):
    imgPath = os.path.abspath(".")+"/tags/material/shapes/"+ imgName # 形状所在路径
    image_data = open(imgPath, "rb").read()
    return HttpResponse(image_data, content_type="image/png")
    
    
# 创建词云
@csrf_exempt
def wordcloud_create(request):
    currentpath = os.path.abspath(".")
    keyword = request.POST['keywords'].encode('utf-8') # 关键词
    bgcolor = request.POST['bgcolor'].encode('utf-8') # 背景色
    maxwords = request.POST['maxwords'].encode('utf-8') # 最大词数
    fontColor = request.POST['fontColor'].encode('utf-8') # 字体颜色
    fontStyle = request.POST['fontStyle'].encode('utf-8') # 字体
    shapes = request.POST['shapes'].encode('utf-8') # 形状

    params = {
        'type': 2,
        'query': keyword
    }
    urls = []
    for page in range(1, 11):
        params['page'] = page
        urls.append('http://weixin.sogou.com/weixin?' + urllib.urlencode(params))
    print urls
    
    # 爬去文章
    txt = getWebArticle(keyword)
    # 检索需要的关键词
    txt_freq = Keywords(txt).tf_idf()
    # ---

    font_path = currentpath + '/tags/material/fonts/'+ fontStyle #选择字体，fontStyle值为当前文件夹下字体文件的名字
    image_path = currentpath + "/tags/material/shapes/"+ shapes #选择形状，shapes值为当前文件夹下图片的名字
    mask = np.array(Image.open(image_path))

    # WordCloud参数：(参考https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html#wordcloud.WordCloud)
    #   font_path : string 字体路径
    #   width : int (default=400) 画布的宽度
    #   height : int (default=200) 画布的高度
    #   prefer_horizontal : float (default=0.90)
    #   mask : nd-array or None (default=None)
    #   scale : float (default=1)
    #   min_font_size : int (default=4) 最小的字体尺寸
    #   font_step : int (default=1) 字体的步长
    #   max_words : number (default=200) 最大词数
    #   stopwords : set of strings or None
    #   background_color : color value (default=”black”) 词云图像背景颜色
    #   max_font_size : int or None (default=None) 最大的字体尺寸
    #   mode : string (default=”RGB”)
    #   relative_scaling : float (default=.5)
    #   color_func : callable, default=None
    #   regexp : string or None (optional)
    #   collocations : bool, default=True
    #   colormap : string or matplotlib colormap, default=”viridis”
    #   normalize_plurals : bool, default=True
    wc = WordCloud(font_path,
                   background_color=bgcolor, # 背景颜色
                   max_words=int(maxwords), # 词云显示的最大词数
                   mask=mask)
                   
    wc.generate_from_frequencies(txt_freq) 
    
    if fontColor == '0':
        plt.imshow(wc, interpolation="bilinear")    
    elif fontColor =='1':
        plt.imshow(wc.recolor(color_func=image_colors_func(image_path)), interpolation="bilinear")
    else:
        plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),
           interpolation="bilinear")
           
    plt.axis("off")
    plt.savefig(currentpath + '/tags/static/temp.png',bbox_inches="tight", transparent=False)       
    # random.randint(0,1000)加在图片url后面，只要随机数发生改变，浏览器就会重新请求图片
    result = '<img src="/static/temp.png?a='+str(random.randint(0,1000))+'" width="600px" height="600px"/>'

    return HttpResponse(result, content_type="text")

# 爬去文章
def getWebArticle( keyword ):
    # 检索本地文章
    txt = getLocalArticle( keyword )
    if txt!=False:
        return txt;

    params = {
        'type': 2,
        'query': keyword
    }
    urls = []
    for page in range(1, 11):
        params['page'] = page
        urls.append('http://weixin.sogou.com/weixin?' + urllib.urlencode(params))
    print urls
    
    folderPath = os.path.abspath(".")+"/tags/static/article" # 文章所在文件夹
    filePath = folderPath+"/"+keyword.decode('utf-8')+".txt" # 文章的保存路径
    
    if os.path.exists(folderPath)==False and os.path.isfile(folderPath)==False: # 路径不存在,就创建路径
        os.makedirs(folderPath)
    
    if os.path.exists(filePath)==False or os.path.isfile(filePath)==False: # 文章不存在，就创建文章    
        txt = crawler(urls,filePath)
        return txt
    # 将本章保存到本地
    #keepArticle( keyword,txt )
    #return txt;
    
# 检索本地文章
def getLocalArticle( keyword ):
    folderPath = os.path.abspath(".")+"/tags/static/article" # 文章所在文件夹
    filePath = folderPath+"/"+keyword.decode('utf-8')+".txt" # 文章的保存路径

    if os.path.exists(folderPath)==False and os.path.isfile(folderPath)==False: # 路径不存在
        os.makedirs(folderPath)
        return False;
    elif os.path.exists(filePath)==False or os.path.isfile(filePath)==False: # 文章不存在
        return False;
    else: # 文章存在,读取内容并返回
        fileObj = open(filePath, 'r')
        try:
            article = fileObj.read( )
        finally:
            fileObj.close( )
        return article;

# 将本章保存到本地
def keepArticle( keyword,article ):
    folderPath = os.path.abspath(".")+"/tags/static/article" # 文章所在文件夹
    filePath = folderPath+"/"+keyword.decode('utf-8')+".txt" # 文章的保存路径

    if os.path.exists(folderPath)==False and os.path.isfile(folderPath)==False: # 路径不存在,就创建路径
        os.makedirs(folderPath)
    
    if os.path.exists(filePath)==False or os.path.isfile(filePath)==False: # 文章不存在，就创建文章
        fileObj = open(filePath, 'w')
        fileObj.write(article)
        fileObj.close()

    return;        
