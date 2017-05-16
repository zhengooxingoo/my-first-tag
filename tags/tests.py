#coding:utf-8
from django.test import TestCase

# Create your tests here.
from django.core.urlresolvers import resolve
from tags.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
import re
from tags.models import Fonts

class HomePageTest(TestCase):
    def remove_csrf(self,html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def assertEqualExceptCSRF(self, html_code1, html_code2):
        return self.assertEqual(
            self.remove_csrf(html_code1),
            self.remove_csrf(html_code2)
        )
        


        
        


