from django.test import SimpleTestCase
from django.urls import reverse
import django
import os
import unittest
from unittest.mock import patch
from src.api.llm_service import LLMService
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

    def test_up_api_view(self):
        response = self.client.get(reverse('api'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "okay")

    # def test_get_llm(self):
    #     response = self.client.get(reverse("getLLM", args=["my-llm"]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), {"llm": "my-llm"})

if __name__ == '__main__':
	unittest.main(warnings = 'ignore')