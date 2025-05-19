import argparse
import logging
from grobid.metadata_extractor import extract_metadata_from_grobid_output
from grobid.grobid_client import process_papers
from enrich.openalex_query import add_topics
from enrich.json_to_rdf import json_to_rdf
from enrich.wikidata_enrich import enrich_rdf_with_wikidata
from similarity.paper_similarity import similarity_score
from ner.extract_acknowledgements import named_entity_recognition
from provenance.create_prov import create_provenance_document
from ro_create.create_ro_crate import create_ro_crate_metadata
from topic_modeling.abstract_topics import create_topic_modeling
import os
import subprocess
import sys
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_api_services():
    """Run both API and SPARQL endpoint services as subprocesses."""
    api_path = os.path.join("..", "api", "api.py")
    sparql_path = os.path.join("..", "api", "sparql_endpoint.py")
    
    logging.info("Starting API and SPARQL endpoint services...")
    
    api_process = subprocess.Popen([sys.executable, api_path])
    sparql_process = subprocess.Popen([sys.executable, sparql_path])
    
    logging.info("API running on http://localhost:5001")
    logging.info("SPARQL endpoint running on http://localhost:5000")
    
    try:
        # Keep the main thread alive
        print("Services are running. Press Ctrl+C to stop...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        logging.info("Shutting down services...")
        api_process.terminate()
        sparql_process.terminate()
        api_process.wait(timeout=5)
        sparql_process.wait(timeout=5)

def run_analysis_pipeline():
    """Run the complete data analysis pipeline."""
    output_folder = "output"

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
    if add_topics(os.path.join(output_folder,"papers_metadata.json"),
                  os.path.join(output_folder,"papers_with_openalex.json")) == 1:
        print("Error adding topics: Aborting")
        return

    # Step 4: Convert json to rdf file
    if json_to_rdf(os.path.join(output_folder,"papers_with_openalex.json"),
                   os.path.join(output_folder,"papers_with_topics.ttl")) == 1:
        print("Error transforming to RDF: Aborting")
        return

    # Step 5: Enrich rdf file with wikidata
    if enrich_rdf_with_wikidata(os.path.join(output_folder,"papers_with_topics.ttl"),
                               os.path.join(output_folder,"papers_wikidata_enriched.ttl")) == 1:
        print("Error perfoming enrichment with wikidata: Aborting")
        return 

    # Step 6: Run Topic Modeling on Abstracts
    create_topic_modeling()

    # Step 6: Generate similarity score between papers based on topics
    if similarity_score(os.path.join(output_folder,"papers_with_openalex.json"),
                       os.path.join(output_folder,"paper_similarities.json")) == 1:
        print("Error analalysing similarities")

    # Step 7: Extracting named entities from acknowledgements
    named_entity_recognition()

    # Step 8: Generate provenance
    create_provenance_document()

    # Step 9: Package as Research Object
    create_ro_crate_metadata()

def main():
   # run_analysis_pipeline()
    
    # Run API services
    run_api_services()

if __name__ == "__main__":
    main()