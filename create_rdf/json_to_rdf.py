import json
import requests
from time import sleep
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, DCTERMS, FOAF, SKOS, OWL

# Cargar archivo JSON enriquecido
with open("papers_with_openalex.json", "r", encoding="utf-8") as f:
    data = json.load(f)

papers = data["papers"]

# Crear grafo RDF
g = Graph()

# Namespaces
EX = Namespace("http://example.org/resource/")
BIBO = Namespace("http://purl.org/ontology/bibo/")
WD = Namespace("http://www.wikidata.org/entity/")
g.bind("dcterms", DCTERMS)
g.bind("foaf", FOAF)
g.bind("bibo", BIBO)
g.bind("skos", SKOS)
g.bind("ex", EX)
g.bind("wd", WD)

# Procesar cada paper
for idx, paper in enumerate(papers):
    paper_uri = EX[f"paper{idx}"]
    g.add((paper_uri, RDF.type, BIBO.Document))

    # Título
    if paper.get("title"):
        g.add((paper_uri, DCTERMS.title, Literal(paper["title"])))

    # DOI
    if paper.get("doi"):
        g.add((paper_uri, BIBO.doi, Literal(paper["doi"])))

    # Fecha
    if paper.get("publicationYear"):
        g.add((paper_uri, DCTERMS.issued, Literal(paper["publicationYear"])))

    # Revista
    if paper.get("publishedIn"):
        g.add((paper_uri, DCTERMS.publisher, Literal(paper["publishedIn"])))

    # Autores
    for i, author in enumerate(paper.get("authors", [])):
        author_uri = EX[f"author_{idx}_{i}"]
        full_name = " ".join(filter(None, [
            author.get("firstname", "").strip(),
            author.get("middlename", "").strip(),
            author.get("lastname", "").strip()
        ]))
        g.add((author_uri, RDF.type, FOAF.Person))
        g.add((author_uri, FOAF.name, Literal(full_name)))
        g.add((paper_uri, DCTERMS.creator, author_uri))

    # Temas desde OpenAlex (topics)
    for topic in paper.get("openalex_topics", []):
        topic_uri = URIRef(f"http://example.org/topic/{topic.replace(' ', '_')}")
        g.add((topic_uri, RDF.type, SKOS.Concept))
        g.add((topic_uri, SKOS.prefLabel, Literal(topic)))
        g.add((paper_uri, DCTERMS.subject, topic_uri))

# Guardar RDF
g.serialize("papers_with_topics.ttl", format="turtle")
print("✅ RDF enriquecido con topics guardado en 'papers_with_topics.ttl'")

def query_wikidata(search_term, entity_type=None):
    """
    Query Wikidata for entities matching the search term.
    
    Args:
        search_term: The term to search for
        entity_type: Optional Wikidata entity type to filter results
        
    Returns:
        Dictionary with Wikidata ID and label if found, None otherwise
    """
    if not search_term or len(search_term) < 3:
        return None
        
    url = "https://www.wikidata.org/w/api.php"
    
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "search": search_term
    }
    
    # Add type filter if specified
    if entity_type:
        params["type"] = entity_type
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "search" in data and len(data["search"]) > 0:
            item = data["search"][0]
            return {
                "id": item["id"],
                "uri": f"http://www.wikidata.org/entity/{item['id']}",
                "label": item.get("label", search_term)
            }
        return None
    except Exception as e:
        print(f"Error querying Wikidata for {search_term}: {e}")
        return None
    finally:
        # Be nice to the Wikidata API
        sleep(0.1)

def enrich_rdf_with_wikidata(input_file, output_file):
    """Enrich existing RDF graph with Wikidata links"""
    
    # Load the existing graph
    g = Graph()
    g.parse(input_file, format="turtle")
    
    # Add owl:sameAs predicates
    g.bind("wd", WD)
    
    # Find all topics
    topics = {}
    for s, p, o in g.triples((None, URIRef("http://www.w3.org/2004/02/skos/core#prefLabel"), None)):
        topic_name = str(o)
        topics[s] = topic_name
    
    # Enrich topics with Wikidata links
    for topic_uri, topic_name in topics.items():
        wikidata_entity = query_wikidata(topic_name, "item")
        if wikidata_entity:
            g.add((topic_uri, OWL.sameAs, URIRef(wikidata_entity["uri"])))
            print(f"Linked topic '{topic_name}' to {wikidata_entity['uri']}")
    
    # Find all authors
    authors = {}
    for s, p, o in g.triples((None, URIRef("http://xmlns.com/foaf/0.1/name"), None)):
        author_name = str(o)
        authors[s] = author_name
    
    # Enrich authors with Wikidata links
    for author_uri, author_name in authors.items():
        wikidata_entity = query_wikidata(author_name, "item")
        if wikidata_entity:
            g.add((author_uri, OWL.sameAs, URIRef(wikidata_entity["uri"])))
            print(f"Linked author '{author_name}' to {wikidata_entity['uri']}")
    
    # Save the enriched graph
    g.serialize(output_file, format="turtle")
    print(f"Enriched RDF saved to {output_file}")

if __name__ == "__main__":
    enrich_rdf_with_wikidata("papers_with_topics.ttl", "papers_wikidata_enriched.ttl")
