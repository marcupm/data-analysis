import os
from flask import Flask, request, jsonify
from rdflib import Graph, URIRef, Literal

app = Flask(__name__)

# Load RDF data
graph = Graph()
rdf_path = os.path.join(os.path.dirname(__file__), "..", "app", "output", "papers_wikidata_enriched.ttl")
graph.parse(rdf_path, format="turtle")

def rdflib_result_to_sparql_json(results):
    vars = results.vars
    bindings = []
    for row in results:
        binding = {}
        for idx, var in enumerate(vars):
            val = row[idx]
            if val is not None:
                if isinstance(val, Literal):
                    value = {
                        "type": "literal",
                        "value": str(val)
                    }
                    if val.language:
                        value["xml:lang"] = val.language
                    if val.datatype:
                        value["datatype"] = str(val.datatype)
                elif isinstance(val, URIRef):
                    value = {
                        "type": "uri",
                        "value": str(val)
                    }
                else:
                    value = {
                        "type": "literal",
                        "value": str(val)
                    }
                binding[str(var)] = value
        bindings.append(binding)
    return {
        "head": {"vars": [str(v) for v in vars]},
        "results": {"bindings": bindings}
    }

@app.route('/sparql', methods=['GET', 'POST'])
def sparql_query():
    query = request.args.get('query') if request.method == 'GET' else request.json.get('query')
    
    if not query:
        return jsonify({"error": "No SPARQL query provided"}), 400
    
    try:
        results = graph.query(query)
        sparql_json = rdflib_result_to_sparql_json(results)
        return jsonify(sparql_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/')
def index():
    default_query = """PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX bibo: <http://purl.org/ontology/bibo/>

SELECT ?paper ?title ?author ?authorName ?type
WHERE {
  ?paper a bibo:Document .
  OPTIONAL { ?paper dcterms:title ?title. }
  OPTIONAL { ?paper dcterms:creator ?author. }
  OPTIONAL { ?author foaf:name ?authorName. }
  OPTIONAL { ?paper a ?type. }
}
LIMIT 20
"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SPARQL Endpoint</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 2em; }}
            textarea {{ width: 100%; height: 120px; }}
            pre {{ background: #f4f4f4; padding: 1em; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h1>SPARQL Endpoint</h1>
        <form id="sparql-form">
            <label for="query">Consulta SPARQL:</label><br>
            <textarea id="query" name="query">{default_query}</textarea><br>
            <button type="submit">Ejecutar</button>
        </form>
        <h2>Resultado</h2>
        <pre id="result"></pre>
        <script>
        document.getElementById('sparql-form').onsubmit = async function(e) {{
            e.preventDefault();
            const query = document.getElementById('query').value;
            const res = await fetch('/sparql?query=' + encodeURIComponent(query), {{
                headers: {{'Accept': 'application/json'}}
            }});
            const data = await res.json();
            document.getElementById('result').textContent = JSON.stringify(data, null, 2);
        }};
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')