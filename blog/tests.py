from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from .views import post_list, post_detail, cv_show

class HomePageTest(TestCase):

    def test_root_url_resolves_to_post_list_view(self):
        found = resolve('/')  
        self.assertEqual(found.func, post_list) 

    def test_cv_page_has_correct_title(self):
        request = HttpRequest()
        response = cv_show(request)  
        html = response.content.decode('utf8')  
        self.assertIn('<title>My CV</title>', html)

    def test_can_save_a_POST_request(self):
        response = self.client.post('/cv/new/', data={'title': 'A new list item', 'text': 'Bah.'})
        self.assertIn('A new list item', response.content.decode())

    
   