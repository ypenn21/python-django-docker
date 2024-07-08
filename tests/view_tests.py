from django.test import SimpleTestCase
from django.urls import reverse
import django
import os
import unittest
class ViewTests(SimpleTestCase):
    def setUp(self):
        django.setup()
    def test_up_up_view(self):
        response = self.client.get(reverse('up'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "okay")

    def test_up_status_view(self):
        response = self.client.get(reverse('status'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "okay:")

    def test_up_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<title>Shell Script to Terraform</title>\n")

    def test_up_view_with_error_handling(self):
        # Test error handling
        bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
        response = self.client.get(f"${bind}/missing")
        self.assertEqual(response.status_code, 404)
# Answer as a Software Engineer with expertise in python. Create a test for the api.views for a method api which responds at the HTTP endpoint /api and response should be ‘okay’ in view_tests.py .

if __name__ == '__main__':
	unittest.main(warnings = 'ignore')