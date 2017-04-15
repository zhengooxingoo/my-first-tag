#coding:utf-8
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def home_page(request):
    return HttpResponse('<html><title>中文标签云</title></html>')
