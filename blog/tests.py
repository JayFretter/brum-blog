from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from .models import CVSection

from .views import cv_show

class CVTest(TestCase):

    def test_cv_url_resolves_to_cv_show_view(self):
        found = resolve('/cv/')  
        self.assertEqual(found.func, cv_show) 

    def test_cv_page_has_correct_title(self):
        request = HttpRequest()
        response = cv_show(request)  
        html = response.content.decode('utf8')  
        self.assertIn('<title>My CV</title>', html)

    def test_can_save_and_retrieve_cv_section(self):
        # Make sure the database is empty in the beginning
        self.assertEqual(CVSection.objects.all().count(), 0)

        # Create new CV section
        new_section = CVSection()
        new_section.title = "Education"
        new_section.text = "School 0: 2005-2010"

        # Save the section
        new_section.save()

        # Retrieve all CV sections, ensuring there is only one, and that the data is intact
        saved_sections = CVSection.objects.all()
        self.assertEqual(saved_sections.count(), 1)
        self.assertEqual(saved_sections[0].title, "Education")
        self.assertEqual(saved_sections[0].text, "School 0: 2005-2010")

    def test_can_delete_saved_cv_section(self):
        # Make sure the database is empty in the beginning
        self.assertEqual(CVSection.objects.all().count(), 0)

        # Create new CV section
        new_section = CVSection()
        new_section.title = "Employment"
        new_section.text = "2012-Present: Workplace"
        new_section.save()

        # Ensure it made its way to the database
        saved_sections = CVSection.objects.all()
        self.assertEqual(saved_sections.count(), 1)

        # Delete the CV section
        retrieved_section = saved_sections[0]
        retrieved_section.delete()

        # Check that there are now zero CV sections in the database
        self.assertEqual(CVSection.objects.all().count(), 0)

    def test_can_save_a_POST_request(self):
        # Make sure the database is empty in the beginning
        self.assertEqual(CVSection.objects.all().count(), 0)

        # Send a POST request creating a new CV section item
        self.client.post('/cv/new/', data={'title': 'Summary', 'text': 'I am a team player',})

        # Retrieve all CV sections, ensuring there is only one, and that the data is intact
        saved_sections = CVSection.objects.all()
        self.assertEqual(saved_sections.count(), 1)
        self.assertEqual(saved_sections[0].title, "Summary")
        self.assertEqual(saved_sections[0].text, "I am a team player")

    
   