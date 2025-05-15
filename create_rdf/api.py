from flask import Flask, jsonify, request
from rdflib import Graph
import json

app = Flask(__name__)

# Load RDF data
graph = Graph()
graph.parse("papers_wikidata_enriched.ttl", format="turtle")

@app.route('/api/papers', methods=['GET'])
def get_papers():
    """Return list of all papers"""
    query = """
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX ex: <http://example.org/resource/>
    
    SELECT ?paper ?title ?year 
    WHERE {
        ?paper dcterms:title ?title .
        OPTIONAL { ?paper dcterms:issued ?year }
    }
    """
    
    results = graph.query(query)
    papers = [
        {
            "id": str(row.paper).split('/')[-1],
            "title": str(row.title),
            "year": str(row.year) if row.year else "Unknown"
        }
        for row in results
    ]
    
    return jsonify({"papers": papers})

@app.route('/api/papers/<paper_id>', methods=['GET'])
def get_paper(paper_id):
    """Return details for a specific paper"""
    paper_uri = f"http://example.org/resource/{paper_id}"
    
    query = f"""
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    
    SELECT ?title ?year ?publisher ?topic ?topicLabel ?creator ?creatorName
    WHERE {{
        <{paper_uri}> dcterms:title ?title .
        OPTIONAL {{ <{paper_uri}> dcterms:issued ?year }}
        OPTIONAL {{ <{paper_uri}> dcterms:publisher ?publisher }}
        OPTIONAL {{ 
            <{paper_uri}> dcterms:subject ?topic .
            ?topic skos:prefLabel ?topicLabel 
        }}
        OPTIONAL {{ 
            <{paper_uri}> dcterms:creator ?creator .
            ?creator foaf:name ?creatorName 
        }}
    }}
    """
    
    results = graph.query(query)
    
    if not results:
        return jsonify({"error": "Paper not found"}), 404
    
    paper = {
        "id": paper_id,
        "title": None,
        "year": None,
        "publisher": None,
        "topics": [],
        "authors": []
    }
    
    topics_set = set()
    authors_set = set()
    
    for row in results:
        paper["title"] = str(row.title)
        if row.year:
            paper["year"] = str(row.year)
        if row.publisher:
            paper["publisher"] = str(row.publisher)
        if row.topic and row.topicLabel:
            topic_info = {
                "uri": str(row.topic),
                "label": str(row.topicLabel)
            }
            topic_key = topic_info["uri"]
            if topic_key not in topics_set:
                topics_set.add(topic_key)
                paper["topics"].append(topic_info)
        if row.creator and row.creatorName:
            author_info = {
                "uri": str(row.creator),
                "name": str(row.creatorName)
            }
            author_key = author_info["uri"]
            if author_key not in authors_set:
                authors_set.add(author_key)
                paper["authors"].append(author_info)
    
    return jsonify(paper)

@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Return all topics with their papers"""
    query = """
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    
    SELECT ?topic ?label (COUNT(?paper) AS ?paperCount)
    WHERE {
        ?paper dcterms:subject ?topic .
        ?topic skos:prefLabel ?label .
    }
    GROUP BY ?topic ?label
    ORDER BY DESC(?paperCount)
    """
    
    results = graph.query(query)
    topics = [
        {
            "uri": str(row.topic),
            "label": str(row.label),
            "paperCount": int(row.paperCount)
        }
        for row in results
    ]
    
    return jsonify({"topics": topics})

if __name__ == '__main__':
    app.run(debug=True, port=5001)