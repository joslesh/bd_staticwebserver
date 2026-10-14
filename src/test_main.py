import unittest
from main import extract_title 

class TestMain(unittest.TestCase):
    
    def test_extract_titles(self):
        markdown_file = "test/test_file.md"
        extracted_title = extract_title(markdown_file)
        self.assertEqual(
                "Test Title",
                extracted_title,
                )

if __name__ == "__main__":
    unittest.main()
