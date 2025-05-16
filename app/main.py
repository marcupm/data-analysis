import argparse
import logging
from grobid.metadata_extractor import extract_metadata_from_grobid_output
from grobid.grobid_client import process_papers
from enrich.openalex_query import add_topics
from enrich.json_to_rdf import json_to_rdf
from enrich.wikidata_enrich import enrich_rdf_with_wikidata
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():

    parser = argparse.ArgumentParser(
        description='Process PDF papers and generate visualizations.\n' +
        'This script processes PDF papers in the data/ folder, extracts information, and generates visualizations in the output/ folder.'
    )
    parser.parse_args()

    
    logging.info("Initializing analysis...")


    # Step 1: Process PDFs
 #   papers = process_papers("../data") 

    # Step 2: Extract metadata and generate json
 #   extract_metadata_from_grobid_output(papers, "output", "papers_metadata.json")

    logging.info("Metadata extracted with Grobid. Output saved in /output/grobid_output.json")

    # Step 3: Add topics to json with openalex
    add_topics("output\\papers_metadata.json", "output\\papers_with_openalex.json")

    # Step 4: Convert json to rdf file
    json_to_rdf("output\\papers_with_openalex.json", "output\\papers_with_topics.ttl")

    # Step 5: Enrich rdf file with wikidata
    enrich_rdf_with_wikidata("output\\papers_with_topics.ttl", "output\\papers_wikidata_enriched.ttl")

if __name__ == "__main__":
    main()

