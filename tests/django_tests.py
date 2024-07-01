from django.test import SimpleTestCase
from django.urls import reverse
import django
import os
from django.conf import settings
class UpViewTests(SimpleTestCase):
    django.setup()
    def setUp(self):
        django.setup()
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    def test_up_home_view(self):
        response = self.client.get(reverse('up'))  # Assuming 'home' is a view in up.urls
        self.assertEqual(response.status_code, 200)  # Check for a successful response
        self.assertContains(response, "okay")  # Check for expected content