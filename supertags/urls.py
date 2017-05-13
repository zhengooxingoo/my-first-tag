#coding:utf-8
"""supertags URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from tags import views as tags_views
urlpatterns = [
    # 主页面
    url(r'^$',tags_views.index, name='index'),
    # 创建词云
    url(r'^wordcloud/create/$', tags_views.wordcloud_create, name='wordcloud.create'),
    url(r'^shape/img/(.+)/$', tags_views.shape_img, name='shape.img'),
    #url(r'^admin/', admin.site.urls),
]
