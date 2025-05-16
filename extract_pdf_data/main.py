import argparse
import logging
from src.metadata_extractor import extract_metadata_from_grobid_output
from src.grobid_client import process_papers

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    parser = argparse.ArgumentParser(
        description='Process PDF papers and generate visualizations.\n' +
        'This script processes PDF papers in the data/ folder, extracts information, and generates visualizations in the output/ folder.'
    )
    parser.parse_args()

    
    logging.info("Initializing analysis...")

    # Paso 1: Process PDFs
    papers = process_papers("data/") 

    # Paso 2: Extract keywords and generate keyword cloud
    extract_metadata_from_grobid_output(papers, "output")

    logging.info("Analysis complete. Results saved in the output/ folder.")

if __name__ == "__main__":
    main()

