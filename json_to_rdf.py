import json
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, DCTERMS, FOAF

# Cargar archivo JSON
with open("papers_metadata.json", "r", encoding="utf-8") as f:
    data = json.load(f)

papers = data["papers"]

# Crear grafo RDF
g = Graph()

# Namespaces
EX = Namespace("http://example.org/resource/")
BIBO = Namespace("http://purl.org/ontology/bibo/")
g.bind("dcterms", DCTERMS)
g.bind("foaf", FOAF)
g.bind("bibo", BIBO)
g.bind("ex", EX)

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

# Guardar RDF
g.serialize("papers_metadata.ttl", format="turtle")
print("✅ RDF generado en 'papers_metadata.ttl'")
