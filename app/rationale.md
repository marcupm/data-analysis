# Rationale

## Project Overview

This project aims to analyze a group of articles using Grobid and enriched its information using OpenAlex, Wikidata and other text analysis tools. The program generates the following outputs:
- papers_wikidata_enrinches.ttl: File with turtle format with the final enriched knowledge graph
- data provenance: available in .xml, .provn and .json 
- ro-crate-metadata.json: Reasearch Object information
- png files: Graphs generated from the information gathered during the analysis
- Intermediate files to see the steps taken by the program

## Project Structure

The project is organized into the following files:
- `app/`: Performs the main functionality of the program. Contains the main.py script and the rest of funcions used by it grouped in files
- `app/main.py`: The main script that orchestrates the entire analysis process.
- `api/`: Contains the files used to run the sparql endpoint and the API
- `demo/`: A demostration of an analysis done in ten papers and a script to create your own demostration
  
## Steps and Validation

EXPLAINED in the [README](../README.md) file.

## Conclusion

The project successfully performs the required analysis on the open-access articles. Each step has been validated to ensure correctness and reliability. The results are saved in the `output` folder.

By following best practices and validating each step, I ensure that the analysis is accurate and the results are meaningful.
