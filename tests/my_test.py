import unittest
from src.up.utils import generate_random_number


class UtilsTest(unittest.TestCase):


    # def setUp(self):
    #     self.browser = webdriver.Firefox()

    # def tearDown(self):
    #     self.browser.quit()

    # def test_can_start_list_and_retrive_later(self):
    #     self.browser.get('http://localhost:8000')
    #     self.assertIn('To-Do', self.browser.title)

    def test_increment(self):
        self.assertEqual(1,1)

    def test_generate_random_number(self):
        """Tests that generate_random_number returns a random integer within the specified range."""
        min_value = 10
        max_value = 20
        random_number = generate_random_number(min_value, max_value)
        self.assertTrue(min_value <= random_number <= max_value)
if __name__ == '__main__':
	unittest.main(warnings = 'ignore')