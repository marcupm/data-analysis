import json
import os
import datetime

def create_ro_crate_metadata():
    """Create Research Object Crate metadata file following RO-Crate 1.1 specification"""
    
    # Base metadata structure
    metadata = {
        "@context": "https://w3id.org/ro/crate/1.1/context",
        "@graph": [
            {
                "@id": "./",
                "@type": "Dataset",
                "name": "Research Paper Analysis and Knowledge Graph",
                "description": "A research project analyzing a corpus of scientific papers, extracting topics, calculating similarities, and building a knowledge graph.",
                "datePublished": datetime.datetime.now().strftime("%Y-%m-%d"),
                "license": "https://creativecommons.org/licenses/by/4.0/",
                "creator": [
                    {
                        "@id": "#researcher"
                    }
                ],
                "hasPart": [
                    {"@id": "data/"},
                    {"@id": "output/"},
                    {"@id": "papers_wikidata_enriched.ttl"}
                ]
            },
            {
                "@id": "#researcher",
                "@type": "Person",
                "name": "UPM Researcher",
                "affiliation": {
                    "@id": "#upm"
                }
            },
            {
                "@id": "#upm",
                "@type": "Organization",
                "name": "Universidad Politécnica de Madrid",
                "url": "https://www.upm.es/"
            },
            {
                "@id": "ro-crate-metadata.json",
                "@type": "CreativeWork",
                "about": {"@id": "./"},
                "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"}
            },
            {
                "@id": "data/",
                "@type": "Dataset",
                "name": "Research Papers Dataset",
                "description": "Collection of scientific papers for analysis"
            },
            {
                "@id": "output/",
                "@type": "Dataset",
                "name": "Analysis Results",
                "description": "Output files from the analysis, including visualizations and JSON data"
            },
            {
                "@id": "papers_wikidata_enriched.ttl",
                "@type": "File",
                "name": "Knowledge Graph (Turtle format)",
                "description": "RDF knowledge graph of papers with Wikidata links",
                "encodingFormat": "text/turtle"
            },
            {
                "@id": "topic_modeling/abstract_topics.py",
                "@type": "SoftwareSourceCode",
                "name": "Topic Modeling Script",
                "description": "Python script for modeling topics from paper abstracts",
                "programmingLanguage": "Python"
            },
            {
                "@id": "similarity/paper_similarity.py",
                "@type": "SoftwareSourceCode",
                "name": "Paper Similarity Analysis",
                "description": "Python script for calculating similarity between papers",
                "programmingLanguage": "Python"
            },
            {
                "@id": "ner/extract_acknowledgements.py",
                "@type": "SoftwareSourceCode",
                "name": "Acknowledgements NER Script",
                "description": "Python script for extracting entities from acknowledgements",
                "programmingLanguage": "Python"
            },
            {
                "@id": "create_rdf/json_to_rdf.py",
                "@type": "SoftwareSourceCode",
                "name": "Knowledge Graph Creation Script",
                "description": "Python script for creating RDF knowledge graph",
                "programmingLanguage": "Python"
            }
        ]
    }
    
    # Save the RO-Crate metadata
    os.makedirs("ro_crate", exist_ok=True)
    with open("ro_crate/ro-crate-metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print("✓ RO-Crate metadata created at ro_crate/ro-crate-metadata.json")
    return metadata

if __name__ == "__main__":
    create_ro_crate_metadata()