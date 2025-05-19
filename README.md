# Data Analysis
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14957145.svg)](https://doi.org/10.5281/zenodo.14957145)

## Overview

This project analyzes a corpus of research papers to extract topics, compute similarities, link them in a knowledge graph, and identify funding information. It leverages HuggingFace models and follows best practices for research data management.

## Table of Contents

- Prerequisites
- Installation
- Pipeline Steps
- Component Details
- Query the Knowledge Graph
- Research Object & Provenance
- Directory Structure

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Research papers in PDF format to be analysized

## Installation & Execution

1. Clone this repository:
   ```bash
   git clone [url-github](https://github.com/marcupm/data-analysis.git)
   cd data-analysis
   ```

2. Place your research papers in the `data/` directory.

3. Start the service:
   ```bash
   docker-compose up -d
   ```

## Pipeline Steps

The pipeline follow the following steps to perform the data analysis automatically when the main is executed

### 1. Extracting Metadata from PDFs
The pipeline begins by sending the PDF files to GROBID for processing. This extracts structured metadata such as title, authors, affiliations, DOI, and abstract for each paper.

### 2. Enriching Metadata with OpenAlex Topics
Using the extracted DOIs, the pipeline queries the OpenAlex API to retrieve additional topical information. This helps classify each paper within broader research areas.

### 3. Creating an RDF Knowledge Graph
The enriched metadata is then transformed into an RDF knowledge graph, enabling semantic analysis and integration with other linked data systems.

### 4. Enriching RDF with Wikidata Links
Entities within the graph—such as authors, institutions, or topics—are linked to corresponding Wikidata resources. This enhances the semantic richness and interoperability of the graph.

### 5. Running Topic Modeling on Abstracts
Topic modeling techniques (LDA and BERTopic) are applied to the abstracts to identify common research themes and emerging trends across the papers.

### 6. Calculating Paper Similarities
Transformer-based embeddings are used to compute similarity scores between papers, helping uncover related or thematically similar research.

### 7. Extracting Named Entities from Acknowledgements
The acknowledgements sections are processed using Named Entity Recognition (NER) to identify funding organizations and other mentioned entities.

### 8. Documenting Data Provenance
A PROV-compliant provenance document is generated to describe the full workflow, ensuring transparency and traceability of all data transformations.

### 9. Packaging as a Research Object
Finally, all outputs are bundled into a standardized Research Object Crate (RO-Crate), making the results portable, interoperable, and reusable within the scientific ecosystem.

## Component Details

### Metadata Extraction
Uses GROBID to extract structured metadata from PDFs, including titles, authors, abstracts, and references.

### Topic Modeling
Two approaches:
- **LDA (Latent Dirichlet Allocation)**: Traditional statistical approach
- **BERTopic**: Transformer-based approach using HuggingFace models

### Similarity Analysis
Uses sentence-transformers to create embeddings for each paper abstract, then computes cosine similarity to identify related papers.

### NER Analysis
Applies Hugging Face's NER models to extract funding organizations and other entities from acknowledgements sections.

### Knowledge Graph Creation
Converts extracted information into RDF format, linking papers with:
- Authors
- Topics
- Publication details
- External resources (Wikidata)

## Query the Knowledge Graph

Start the SPARQL endpoint:

```bash
cd api
python sparql_endpoint.py
```

Visit http://localhost:5000 in your browser to query the knowledge graph.

Example queries:
- Find papers by topic
- Identify collaborating authors
- Discover funding patterns

You can also use the API:

```bash
cd api
python api.py
```

Visit http://localhost:5001/api/papers to access the REST API.

## Research Object & Provenance

The pipeline creates:

1. **PROV Documentation**: Captures the entire analysis workflow with detailed provenance information
2. **Research Object Crate**: Packages all research outputs following RO-Crate 1.1 standards

## Directory Structure

```
research-paper-analysis/
├── api/
│   ├── api.py                           # REST API for data access
│   └── sparql_endpoint.py               # SPARQL query interface
├── app/
│   ├── enrich/
│   │   ├── json_to_rdf.py               # Convert JSON to RDF
│   │   ├── openalex_query.py            # Query OpenAlex API
│   │   └── wikidata_enrich.py           # Wikidata entity linking
│   ├── grobid/
│   │   ├── grobid_client.py             # Client for GROBID service
│   │   └── metadata_extractor.py        # Extract metadata from GROBID output
│   ├── ner/
│   │   └── extract_acknowledgements.py  # Extract entities from acknowledgements
│   ├── provenance/
│   │   └── create_prov.py               # Create PROV documentation
│   ├── ro_create/
│   │   └── create_ro_crate.py           # Create RO-Crate metadata
│   ├── similarity/
│   │   └── paper_similarity.py          # Calculate paper similarities
│   ├── topic_modeling/
│   │   └── abstract_topics.py           # Topic modeling on abstracts
│   ├── main.py                          # main file that runs all the scripts
│   └── rationale.md
├── test/
│   └── test_sparql.md                   # Example queries to test sparql endpoint
├── data/                                # Raw PDF papers 
└── docs/
    ├── index.md                         # Index of the structure of the project
    ├── install.md                       # Instructions to correctly install the project
    ├── requirements.txt                 # List of programs that have to be installed
    └── usage.md                         # Explanation of how to use the app
```

## Model Decisions

- **GROBID**: Specialized for scientific document processing
- **Transformer Models**: State-of-the-art for text understanding
- **BERTopic**: Combines transformers with topic modeling
- **RDF**: Standard format for knowledge graphs with reasoning capabilities
- **PROV & RO-Crate**: Follow FAIR data principles for reproducibility
