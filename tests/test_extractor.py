import unittest
import sys
sys.path.insert(1, r'C:\Users\movil\Documents\Project\Mangaudible\modules')
from PanelExtractor import url_to_image, sort_panels, panelExtraction

class TestExtractor(unittest.TestCase):

    # Simple unit test to check if unsorted panels are sorted and if url conversion to image works
    def test_panelextraction(self):
        url = "https://storage.googleapis.com/mangaudible/manga/Grand%20Blue/chapter1/10.jpg"
        unsorted_frame = [[16, 1889, 380, 287], [9, 18, 873, 338], [567, 365, 319, 330]]
        output = [[9, 18, 873, 338], [16, 1889, 380, 287], [567, 365, 319, 330]]
        panels = [231, 843, 345, 181], [70, 718, 590, 306], [339, 544, 83, 134], [69, 60, 195, 372], [267, 56, 393, 375], [395, 0, 265, 172]
        img = url_to_image(url)
        self.assertSequenceEqual(url_to_image(url).tolist(), img.tolist())
        self.assertSequenceEqual(sort_panels(unsorted_frame), output)
        self.assertSequenceEqual(panelExtraction(url_to_image(url)), panels)





if __name__ == '__main__':
    unittest.main()