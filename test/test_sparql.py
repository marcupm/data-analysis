import requests
import json

# URL del endpoint SPARQL
base_url = "http://localhost:5000/sparql"

def test_query(query, format="json"):
    """Ejecuta una consulta SPARQL y devuelve los resultados"""
    
    # Opción 1: Usar GET con parámetros de consulta
    params = {
        "query": query,
        "format": format
    }
    
    print(f"Ejecutando consulta: {query}")
    print(f"Enviando a: {base_url}")
    
    # Configurar headers para recibir JSON explícitamente
    headers = {"Accept": "application/json"}
    
    # Hacer la solicitud
    response = requests.get(base_url, params=params, headers=headers)
    
    print(f"Código de respuesta: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Respuesta como JSON válido: {json.dumps(data, indent=2)}")
            
            # Analizar resultados
            if "results" in data and "bindings" in data["results"]:
                print(f"Número de resultados: {len(data['results']['bindings'])}")
                if len(data['results']['bindings']) > 0:
                    print("Primer resultado:", data['results']['bindings'][0])
                else:
                    print("Sin resultados en los bindings")
            return data
        except json.JSONDecodeError:
            print("La respuesta no es JSON válido:")
            print(response.text[:500])  # Mostrar los primeros 500 caracteres
            return response.text
    else:
        print(f"Error en la solicitud: {response.text}")
        return None

# Consulta básica que debería funcionar
simple_query = """
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?title 
WHERE {
  ?paper dcterms:title ?title .
}
LIMIT 10
"""

# Consulta para ver autores directamente
author_query = """
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?paper ?authorURI 
WHERE {
  ?paper dcterms:creator ?authorURI .
}
LIMIT 10
"""

# Consulta para ver todas las propiedades de un autor específico
author_properties_query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?p ?o 
WHERE {
  <http://example.org/resource/author_0_0> ?p ?o .
}
"""

# Ejecutar las consultas
print("=== PRUEBA 1: TÍTULOS ===")
test_query(simple_query)

print("\n=== PRUEBA 2: AUTORES ===")
test_query(author_query)

print("\n=== PRUEBA 3: PROPIEDADES DE UN AUTOR ===")
test_query(author_properties_query)