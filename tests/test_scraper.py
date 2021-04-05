import unittest
import sys
sys.path.insert(1, r'C:\Users\movil\Documents\Project\Mangaudible\modules')
from MangaScraper import scraper, create_folders

class TestScraper(unittest.TestCase):
  
  # Simple test if the function can scrape manga from a website 
    def test_scraper(self):
      manga_test = ["late-bloomer"]
      titles_test = ["Late bloomer"]
      filepath = "C:/Users/manga/"
      self.assertEqual(scraper(manga_test, titles_test, 3)["Late bloomer"][0], "https://image.rawdevart.com/comic/late-bloomer/chapters/1/001.jpg")
      self.assertEqual(create_folders(filepath, titles_test), "C:/Users/manga/Late bloomer/chapter1")
     




if __name__ == '__main__':
    unittest.main()
