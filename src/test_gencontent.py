import unittest
from gencontent import extract_title

class TestGenContent(unittest.TestCase):

    def test_extract_title(self):
        text = "# Hello"
        result = extract_title(text)
        self.assertEqual("Hello", result)

    def test_extract_title_invalid(self):
        text = "## Hello"
        with self.assertRaises(ValueError):
            extract_title(text)

    def test_extract_title_multi_line(self):
        text = "### Hello\n## Hi\n# How are you"
        result = extract_title(text)
        self.assertEqual("How are you", result)