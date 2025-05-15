from prov.model import ProvDocument, Namespace
import prov.dot
import datetime
import os

def create_provenance_document():
    """Create a PROV document describing the data analysis workflow"""
    
    # Create a new provenance document
    doc = ProvDocument()
    
    # Define namespaces
    prov_ns = Namespace("prov", "http://www.w3.org/ns/prov#")
    doc.add_namespace(prov_ns)
    
    ns = Namespace("paper-analysis", "http://example.org/paper-analysis#")
    doc.add_namespace(ns)
    
    # Define entities (data)
    raw_papers = doc.entity(ns['raw-papers'], {'prov:label': 'Raw PDF Files', 'prov:type': 'Collection'})
    grobid_output = doc.entity(ns['grobid-output'], {'prov:label': 'GROBID XML Output', 'prov:type': 'Collection'})
    metadata_json = doc.entity(ns['metadata-json'], {'prov:label': 'Paper Metadata JSON', 'prov:type': 'File'})
    openalex_json = doc.entity(ns['openalex-json'], {'prov:label': 'OpenAlex Enriched JSON', 'prov:type': 'File'})
    rdf_graph = doc.entity(ns['rdf-graph'], {'prov:label': 'RDF Knowledge Graph', 'prov:type': 'File'})
    wikidata_enriched = doc.entity(ns['wikidata-enriched'], {'prov:label': 'Wikidata Enriched RDF', 'prov:type': 'File'})
    topic_model = doc.entity(ns['topic-model'], {'prov:label': 'Topic Model Results', 'prov:type': 'File'})
    similarity_matrix = doc.entity(ns['similarity-matrix'], {'prov:label': 'Paper Similarity Results', 'prov:type': 'File'})
    ner_results = doc.entity(ns['ner-results'], {'prov:label': 'Named Entity Recognition Results', 'prov:type': 'File'})
    
    # Define activities (processing steps)
    extraction = doc.activity(ns['extraction'], datetime.datetime.now(), None, {'prov:label': 'PDF Information Extraction'})
    metadata_processing = doc.activity(ns['metadata-processing'], datetime.datetime.now(), None, {'prov:label': 'Metadata Extraction'})
    openalex_enrichment = doc.activity(ns['openalex-enrichment'], datetime.datetime.now(), None, {'prov:label': 'OpenAlex API Enrichment'})
    rdf_creation = doc.activity(ns['rdf-creation'], datetime.datetime.now(), None, {'prov:label': 'RDF Graph Creation'})
    wikidata_linking = doc.activity(ns['wikidata-linking'], datetime.datetime.now(), None, {'prov:label': 'Wikidata Entity Linking'})
    topic_modeling = doc.activity(ns['topic-modeling'], datetime.datetime.now(), None, {'prov:label': 'Topic Modeling'})
    similarity_calculation = doc.activity(ns['similarity-calculation'], datetime.datetime.now(), None, {'prov:label': 'Similarity Calculation'})
    ner_extraction = doc.activity(ns['ner-extraction'], datetime.datetime.now(), None, {'prov:label': 'Named Entity Recognition'})
    
    # Define agents (software, people)
    researcher = doc.agent(ns['researcher'], {'prov:label': 'Researcher', 'prov:type': 'prov:Person'})
    grobid = doc.agent(ns['grobid'], {'prov:label': 'GROBID', 'prov:type': 'prov:SoftwareAgent'})
    python = doc.agent(ns['python'], {'prov:label': 'Python', 'prov:type': 'prov:SoftwareAgent'})
    openalex = doc.agent(ns['openalex'], {'prov:label': 'OpenAlex API', 'prov:type': 'prov:SoftwareAgent'})
    wikidata = doc.agent(ns['wikidata'], {'prov:label': 'Wikidata API', 'prov:type': 'prov:SoftwareAgent'})
    transformers = doc.agent(ns['transformers'], {'prov:label': 'Hugging Face Transformers', 'prov:type': 'prov:SoftwareAgent'})
    
    # Define relationships
    doc.wasAttributedTo(raw_papers, researcher)
    doc.wasAssociatedWith(extraction, grobid)
    doc.wasAssociatedWith(metadata_processing, python)
    doc.wasAssociatedWith(openalex_enrichment, openalex)
    doc.wasAssociatedWith(rdf_creation, python)
    doc.wasAssociatedWith(wikidata_linking, wikidata)
    doc.wasAssociatedWith(topic_modeling, transformers)
    doc.wasAssociatedWith(similarity_calculation, transformers)
    doc.wasAssociatedWith(ner_extraction, transformers)
    
    # Process flow
    doc.used(extraction, raw_papers)
    doc.wasGeneratedBy(grobid_output, extraction)
    
    doc.used(metadata_processing, grobid_output)
    doc.wasGeneratedBy(metadata_json, metadata_processing)
    
    doc.used(openalex_enrichment, metadata_json)
    doc.wasGeneratedBy(openalex_json, openalex_enrichment)
    
    doc.used(rdf_creation, openalex_json)
    doc.wasGeneratedBy(rdf_graph, rdf_creation)
    
    doc.used(wikidata_linking, rdf_graph)
    doc.wasGeneratedBy(wikidata_enriched, wikidata_linking)
    
    doc.used(topic_modeling, openalex_json)
    doc.wasGeneratedBy(topic_model, topic_modeling)
    
    doc.used(similarity_calculation, metadata_json)
    doc.wasGeneratedBy(similarity_matrix, similarity_calculation)
    
    doc.used(ner_extraction, grobid_output)
    doc.wasGeneratedBy(ner_results, ner_extraction)
    
    # Save the provenance document
    os.makedirs("output", exist_ok=True)
    
    # Save as PROV-N notation
    with open("output/provenance.provn", "w") as f:
        f.write(doc.get_provn())
    
    # Save as PROV-XML
    with open("output/provenance.xml", "w", encoding="utf-8") as f:
        f.write(doc.serialize(format="xml"))
    
    # Save as PROV-JSON
    with open("output/provenance.json", "w", encoding="utf-8") as f:
        f.write(doc.serialize(format="json"))
    
    # Create a visualization
    try:
        dot = prov.dot.prov_to_dot(doc)
        dot.write_png("output/workflow.png")
        print("✓ Workflow visualization created")
    except Exception as e:
        print(f"Could not create visualization: {e}. Install Graphviz from graphviz.org to enable visualizations.")
    
    print("✓ PROV documentation created in output/ directory")
    return doc

if __name__ == "__main__":
    create_provenance_document()