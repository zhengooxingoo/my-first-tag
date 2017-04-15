#coding:utf-8
from django.test import TestCase

# Create your tests here.
from django.core.urlresolvers import resolve
from tags.views import home_page
from django.http import HttpRequest
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func , home_page)
        
        
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        title_b='<title>中文标签云</title>'.encode('utf-8')
        self.assertIn(title_b,response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
