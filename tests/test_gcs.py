import sys
import unittest
from google.cloud import exceptions
# from modules.gcs import retrieve_url
sys.path.insert(1, r'C:\Users\movil\Documents\Project\Mangaudible\modules')
import gcs

class TestGcs(unittest.TestCase):
    
    # Test all the retrieval of a manga page url and the number of pages in the manga
    def test_retrieve_url(self):
        self.assertEqual(gcs.retrieve_url("mangaudible", "Grand Blue", 1, 2), "https://storage.cloud.google.com/mangaudible/manga/Grand Blue/1/2.jpg")
        self.assertEqual(gcs.retrieve_url("mangaudible", "Dan Blue", 1, 2), "Invalid manga name")
        self.assertEqual(gcs.page_count("mangaudible", "Grand Blue", "chapter1"), 50)
        self.assertEqual(gcs.page_count("mangaudible", "Grand Blue", "chapter3"), 0)
        



if __name__ == '__main__':
    unittest.main()

