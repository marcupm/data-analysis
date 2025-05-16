# AIOSRSE-UPM
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14957145.svg)](https://doi.org/10.5281/zenodo.14957145)


README NUEVO:

# Research Paper Analysis Pipeline

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
- 30 research papers in PDF format

## Installation

1. Clone this repository:
   ```bash
   git clone url-github
   cd carpeta creada por el clone
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the GROBID service:
   ```bash
   docker-compose up -d
   ```

4. Place your research papers in the `data/` directory.

## Pipeline Steps

Execute these steps in sequence to process your research papers:


docker-compose up ya hace el punto 1. Habria que añadir los demas puntos a docker para que se ejecuten todos en el contenedor con un simple docker-compose up.
Hay que editar el docker para que haga todo.
### 1. Extract Metadata from PDFs

```bash
cd extract_pdf_data
python main.py
```

This sends PDFs to GROBID for processing and extracts structured metadata.

### 2. Enrich Metadata with OpenAlex Topics

```bash
cd ../create_rdf
python openalex_query.py
```

This queries the OpenAlex API to retrieve topic information for each paper based on DOIs.

### 3. Create RDF Knowledge Graph

```bash
python json_to_rdf.py
```

Converts the enriched metadata into an RDF knowledge graph.

### 4. Enrich RDF with Wikidata Links

```bash
python wikidata_enrichment.py
```

Links entities in the knowledge graph to Wikidata resources.

### 5. Run Topic Modeling on Abstracts

```bash
cd ../topic_modeling
python abstract_topics.py
```

Applies both LDA and BERTopic models to identify research themes in paper abstracts.

### 6. Calculate Paper Similarities

```bash
cd ../similarity
python paper_similarity.py
```

Computes similarity scores between papers using transformer-based embeddings.

### 7. Extract Named Entities from Acknowledgements

```bash
cd ../ner
python extract_acknowledgements.py
```

Identifies funding organizations and other entities in paper acknowledgements.

### 8. Document Data Provenance

```bash
cd ../provenance
python create_prov.py
```

Creates PROV documentation describing the entire workflow.

### 9. Package as Research Object

```bash
cd ../ro_crate
python create_ro_crate.py
```

Packages all research outputs as a standardized Research Object Crate.

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
cd create_rdf
python sparql_endpoint.py
```

Visit http://localhost:5000 in your browser to query the knowledge graph.

Example queries:
- Find papers by topic
- Identify collaborating authors
- Discover funding patterns

You can also use the API:

```bash
cd create_rdf
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
├── data/                      # Raw PDF papers 
├── ExtractPDFMetadata/        # PDF extraction components
│   ├── src/
│   │   ├── grobid_client.py   # Client for GROBID service
│   │   └── metadata_extractor.py # Extract metadata from GROBID output
│   └── main.py                # Main extraction script
├── create_rdf/                # Knowledge graph creation
│   ├── json_to_rdf.py         # Convert JSON to RDF
│   ├── openalex_query.py      # Query OpenAlex API
│   ├── sparql_endpoint.py     # SPARQL query interface
│   ├── api.py                 # REST API for data access
│   └── wikidata_enrichment.py # Wikidata entity linking
├── topic_modeling/            # Topic analysis
│   └── abstract_topics.py     # Topic modeling on abstracts
├── similarity/                # Similarity analysis
│   └── paper_similarity.py    # Calculate paper similarities
├── ner/                       # Named entity recognition
│   └── extract_acknowledgements.py # Extract entities from acknowledgements
├── provenance/                # Provenance documentation
│   └── create_prov.py         # Create PROV documentation
└── ro_crate/                  # Research Object packaging
    └── create_ro_crate.py     # Create RO-Crate metadata
```

## Model Decisions

- **GROBID**: Specialized for scientific document processing
- **Transformer Models**: State-of-the-art for text understanding
- **BERTopic**: Combines transformers with topic modeling
- **RDF**: Standard format for knowledge graphs with reasoning capabilities
- **PROV & RO-Crate**: Follow FAIR data principles for reproducibility