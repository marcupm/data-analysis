import json
import requests

# Cargar datos desde el archivo original
with open("../extract_pdf_data/output/papers_metadata.json", "r", encoding="utf-8") as f:
    data = json.load(f)

papers = data["papers"]

def get_openalex_topics(doi):
    """
    Dado un DOI, consulta OpenAlex y devuelve la lista de topicos relacionados.
    """
    if not doi:
        return []
    
    url = f"https://api.openalex.org/works/https://doi.org/{doi}"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            info = resp.json()
            topics = info.get("topics", [])
            return [t["display_name"] for t in topics]
        else:
            print(f"❌ Error {resp.status_code} para DOI {doi}")
            return []
    except Exception as e:
        print(f"⚠️ Excepción para DOI {doi}: {e}")
        return []

# Obtener temas para cada artículo
for paper in papers:
    doi = paper.get("doi")
    topics = get_openalex_topics(doi)
    paper["openalex_topics"] = topics
    print(f"{paper['title'][:60]}... → {topics}")

# Guardar los resultados enriquecidos
with open("output/papers_with_openalex.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Temas agregados y guardados en 'output/papers_with_openalex.json'")
