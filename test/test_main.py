import unittest
import os
import random
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.grobid_client import process_papers
from src.link_extractor import extract_links
from src.visualization import figures_per_article

class TestMain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup code to run once before all tests
        cls.pdf_folder = "data/"
        
        if not os.path.exists(cls.pdf_folder):
            raise unittest.SkipTest(f"The folder {cls.pdf_folder} does not exist.")
        
        pdf_files = [f for f in os.listdir(cls.pdf_folder) if f.endswith('.pdf')]
        if not pdf_files:
            raise unittest.SkipTest("No hay archivos PDF en la carpeta data/")
        
        cls.papers = process_papers(cls.pdf_folder)
        
        if cls.papers:
            cls.paper = random.choice(list(cls.papers.keys()))
        else:
            cls.paper = None
            print("There are no papers to test.")

    def test_valid_urls(self):
        """Test if the URLs of papers are valid."""
        if not self.paper:
            self.skipTest("There are no papers to test.")
        
        links = extract_links(self.papers)
        for paper, link_list in links.items():
            for link in link_list:
                self.assertTrue(link.startswith("http://") or link.startswith("https://"), f"Invalid URL: {link}")

    def test_is_pdf(self):
        """Test if the file is a PDF."""
        if not self.paper:
            self.skipTest("There are no papers to test.")
        
        for filename in os.listdir(self.pdf_folder):
            if filename.endswith(".pdf"):
                self.assertTrue(filename.endswith(".pdf"), f"File is not a PDF: {filename}")

    def test_number_of_figures(self):
        """Test if the number of figures for a specific paper is correct."""
        if not self.paper:
            self.skipTest("There are no papers to test.")
        paper = "2305.04532v2.pdf"
        expected_figures = 6
        figure_counts = figures_per_article(self.papers)
        self.assertEqual(figure_counts.get(paper, 0), expected_figures, f"Number of figures for {paper} is not {expected_figures}")

if __name__ == '__main__':
    unittest.main()