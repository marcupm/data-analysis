import argparse
import logging
from grobid.metadata_extractor import extract_metadata_from_grobid_output
from grobid.grobid_client import process_papers
from enrich.openalex_query import add_topics
from enrich.json_to_rdf import json_to_rdf
from enrich.wikidata_enrich import enrich_rdf_with_wikidata
from similarity.paper_similarity import similarity_score
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():

    parser = argparse.ArgumentParser(
        description='Process PDF papers and generate visualizations.\n' +
        'This script processes PDF papers in the data/ folder, extracts information, and generates visualizations in the output/ folder.'
    )
    parser.parse_args()

    output_folder = "output"

    output_file = os.path.join(output_folder, "papers_metadata.json")

    logging.info("Initializing analysis...")

    # Step 1: Process PDFs
    papers = process_papers("../data") 
    
    if papers == 1:
        print("Error processing the papers: Aborting")
        return

    # Step 2: Extract metadata and generate json
    if extract_metadata_from_grobid_output(papers, "output", "papers_metadata.json") == 1:
        print("Error getting metadata of papers: Aborting")
        return

    logging.info("Metadata extracted with Grobid. Output saved in /output/grobid_output.json")

    # Step 3: Add topics to json with openalex
    if add_topics( os.path.join(output_folder,"papers_metadata.json"),
                    os.path.join(output_folder,"papers_with_openalex.json")) == 1:
        print("Error adding topics: Aborting")
        return

    # Step 4: Convert json to rdf file
    if json_to_rdf( os.path.join(output_folder,"papers_with_openalex.json"),
                     os.path.join(output_folder,"papers_with_topics.ttl")) == 1:
        print("Error transforming to RDF: Aborting")
        return

    # Step 5: Enrich rdf file with wikidata
    if enrich_rdf_with_wikidata(os.path.join(output_folder,"papers_with_topics.ttl"),
                                 os.path.join(output_folder,"paper_similarities.json")) == 1:
        print("Error perfoming enrichment with wikidata: Aborting")
        return 


    # Step 6: Generate similarity score between papers based on topics
    if similarity_score(os.path.join(output_folder,"papers_with_openalex.json"),
                         os.path.join(output_folder,"paper_similarities.json")) == 1:
        print("Error analalysing similarities")

if __name__ == "__main__":
    main()

