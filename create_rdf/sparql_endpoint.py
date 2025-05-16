from rdflib import Graph
from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)

# Load the RDF graph
graph = Graph()
graph.parse("output/papers_wikidata_enriched.ttl", format="turtle")

# HTML template for the SPARQL interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SPARQL Endpoint</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        textarea { width: 100%; height: 150px; }
        pre { background-color: #f5f5f5; padding: 10px; overflow: auto; }
    </style>
</head>
<body>
    <h1>SPARQL Endpoint</h1>
    <form method="post" action="/sparql">
        <textarea name="query">{{ default_query }}</textarea>
        <p>
            <button type="submit">Run Query</button>
            <select name="format">
                <option value="json">JSON</option>
                <option value="xml">XML</option>
                <option value="turtle">Turtle</option>
            </select>
        </p>
    </form>
    {% if results %}
    <h2>Results:</h2>
    <pre>{{ results }}</pre>
    {% endif %}
</body>
</html>
"""

DEFAULT_QUERY = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?title ?author
WHERE {
  ?paper dcterms:title ?title .
  ?paper dcterms:creator ?authorURI .
  ?authorURI foaf:name ?author .
}
LIMIT 10
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, default_query=DEFAULT_QUERY, results=None)

@app.route('/sparql', methods=['GET', 'POST'])
def sparql():
    if request.method == 'POST':
        query = request.form.get('query', DEFAULT_QUERY)
        result_format = request.form.get('format', 'json')
    else:
        query = request.args.get('query', DEFAULT_QUERY)
        result_format = request.args.get('format', 'json')

    try:
        if request.headers.get('Accept') == 'application/json' or result_format == 'json':
            # API mode
            results = graph.query(query)
            result_dict = {"head": {"vars": results.vars}, "results": {"bindings": []}}
            
            for row in results:
                binding = {}
                for var in results.vars:
                    value = row[var] if var in row else None
                    if value:
                        if value.datatype:
                            binding[var] = {"type": "literal", "value": str(value), "datatype": str(value.datatype)}
                        elif isinstance(value, Literal):
                            binding[var] = {"type": "literal", "value": str(value)}
                        else:
                            binding[var] = {"type": "uri", "value": str(value)}
                result_dict["results"]["bindings"].append(binding)
                
            return jsonify(result_dict)
        else:
            # Web interface mode
            results = graph.query(query)
            results_str = json.dumps(
                [
                    {str(var): str(row[var]) for var in results.vars if var in row} 
                    for row in results
                ], 
                indent=2
            )
            return render_template_string(HTML_TEMPLATE, default_query=query, results=results_str)
            
    except Exception as e:
        error_message = str(e)
        if request.headers.get('Accept') == 'application/json':
            return jsonify({"error": error_message}), 400
        else:
            return render_template_string(HTML_TEMPLATE, default_query=query, results=f"Error: {error_message}")

if __name__ == '__main__':
    app.run(debug=True, port=5000)