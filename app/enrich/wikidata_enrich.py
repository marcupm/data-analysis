from time import sleep
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import OWL
import requests

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
    if len(g) == 0:
        print("❌ Error there are no paper to enrich")
        return 1
    
    # Add owl:sameAs predicates
    
    WD = Namespace("http://www.wikidata.org/entity/")
    g.bind("wd", WD)
    
    # Find all topics
    topics = {}
    for s, _, o in g.triples((None, URIRef("http://www.w3.org/2004/02/skos/core#prefLabel"), None)):
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
    for s, _, o in g.triples((None, URIRef("http://xmlns.com/foaf/0.1/name"), None)):
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
    print(f"✅ Enriched RDF saved to {output_file}")
    return 0