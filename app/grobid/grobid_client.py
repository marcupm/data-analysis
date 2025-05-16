import requests
import os
import logging

GROBID_URL_DOCKER = "http://grobid:8070/api/"
GROBID_URL_LOCALHOST = "http://localhost:8070/api/"

def check_grobid_availability():
    """Check if GROBID is available at the provided URL."""
    urls = [GROBID_URL_DOCKER, GROBID_URL_LOCALHOST]
    
    for url in urls:
        url_is_alive = url + 'isalive'
        try:
            response = requests.get(url_is_alive)
            if response.status_code == 200:
                logging.info(f"GROBID available at {url}")
                return url  # Return the URL if it's available
            else:
                logging.error(f"GROBID not available at {url}, Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error connecting to GROBID at {url}: {e}")
    
    return None  # Return None if no URL is available

def process_papers(pdf_folder):
    """Send PDFs to GROBID for processing and return the extracted text."""
    processed_papers = {}
    grobid_url = check_grobid_availability() + "processFulltextDocument"

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(pdf_folder, filename)
            logging.info(f"Processing: {filename}")

            with open(filepath, "rb") as pdf:
                response = requests.post(
                    grobid_url, 
                    files={"input": pdf}, 
                    data={"consolidateHeader": 1}
                )
                
                if response.status_code == 200:
                    processed_papers[filename] = response.text
                else:
                    logging.error(f"Processing error: {filename}")

    return processed_papers
