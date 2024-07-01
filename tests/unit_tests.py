import unittest
# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from up.utils import generate_random_number

class UtilsTest(unittest.TestCase):
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