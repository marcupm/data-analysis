import os
import json
import xml.etree.ElementTree as ET
import re
import logging
import csv  # Importar el módulo CSV

def extract_metadata_from_grobid_output(processed_papers, output_folder):
    """
    Extrae metadatos de los papers procesados por GROBID y los guarda en un archivo JSON.
    
    Args:
        processed_papers: dict con {filename: grobid_xml_text}
        output_folder: carpeta donde se guardará el archivo JSON
    """
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, "papers_metadata.json")
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    papers_data = []
    
    for filename, xml_text in processed_papers.items():
        try:
            # Limpieza básica de XML mal formado
            xml_text = xml_text.replace("&", "&amp;").replace("<abstract></abstract>", "<abstract/>")
            
            root = ET.fromstring(xml_text)
            ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

            # Extracción de título
            title = (root.findtext('.//tei:titleStmt/tei:title', namespaces=ns) or 
                    root.findtext('.//tei:analytic/tei:title[@level="a"][@type="main"]', namespaces=ns) or
                    root.findtext('.//tei:analytic/tei:title', namespaces=ns) or 
                    root.findtext('.//tei:body//tei:p[contains(text(), "Robotics")]', namespaces=ns) or "")
            
            # Extracción de año de publicación
            publicationYear = ""
            date_elem = root.find('.//tei:publicationStmt/tei:date[@type="published"]', namespaces=ns)
            if date_elem is not None:
                date_text = date_elem.attrib.get('when', '')
                match = re.search(r'(19|20)\d{2}', date_text)
                if match:
                    publicationYear = match.group(0)
            
            if not publicationYear:
                date_elem = root.find('.//tei:imprint/tei:date[@type="published"]', namespaces=ns)
                if date_elem is not None:
                    date_text = date_elem.attrib.get('when', '')
                    match = re.search(r'(19|20)\d{2}', date_text)
                    if match:
                        publicationYear = match.group(0)
            
            # Extracción de revista/conferencia
            publishedIn = (
                root.findtext('.//tei:monogr/tei:title[@level="j"][@type="main"]', namespaces=ns) or 
                root.findtext('.//tei:monogr/tei:title[@level="j"]', namespaces=ns) or
                root.findtext('.//tei:monogr/tei:meeting', namespaces=ns) or
                ""
            )
            
            # Extracción de DOI o identificador alternativo
            doi = root.findtext('.//tei:idno[@type="DOI"]', namespaces=ns) or ""
            
            if not doi:
                arxiv_id = root.findtext('.//tei:idno[@type="arXiv"]', namespaces=ns)
                if arxiv_id:
                    doi = f"arXiv:{arxiv_id}"
            
            # Extracción de abstract
            abstract = ""
            
            abstract_elem = root.find('.//tei:profileDesc/tei:abstract/tei:p', namespaces=ns)
            if abstract_elem is not None and abstract_elem.text:
                abstract = abstract_elem.text
            
            if not abstract:
                abstract_div = root.find('.//tei:profileDesc/tei:abstract/tei:div/tei:p', namespaces=ns)
                if abstract_div is not None and abstract_div.text:
                    abstract = abstract_div.text
            
            if not abstract:
                abstract_elem = root.find('.//tei:profileDesc/tei:abstract', namespaces=ns)
                if abstract_elem is not None:
                    abstract = ''.join(abstract_elem.itertext()).strip()
            
            if not abstract:
                body_paragraphs = root.findall('.//tei:body//tei:p', namespaces=ns)
                for p in body_paragraphs:
                    p_text = p.text if p.text else ""
                    if p_text and (p_text.startswith('Abstract') or p_text.strip().startswith('Abstract')):
                        abstract = p_text
                        break
                
                if not abstract:
                    for p in body_paragraphs[:5]:
                        p_text = ''.join(p.itertext()) if p is not None else ""
                        if len(p_text) > 100 and ("we" in p_text.lower() or "introduce" in p_text.lower()):
                            abstract = p_text
                            break
            # Extracción de autores SOLO del artículo principal (no de la bibliografía)
            authors = []
            # Usamos una ruta XPath específica para los autores principales
            author_elements = root.findall('.//tei:sourceDesc/tei:biblStruct/tei:analytic/tei:author', namespaces=ns)

            # Si no encontramos autores con la ruta específica, no buscamos en otras partes
            for author_elem in author_elements:
                persName = author_elem.find('./tei:persName', namespaces=ns)
                if persName is not None:
                    firstname = persName.findtext('./tei:forename[@type="first"]', namespaces=ns) or ""
                    middlename = persName.findtext('./tei:forename[@type="middle"]', namespaces=ns) or ""
                    surname = persName.findtext('./tei:surname', namespaces=ns) or ""
                    
                    # Si hay nombre o apellido, añadir a la lista de autores
                    if firstname or surname:
                        author_data = {
                            "firstname": firstname,
                            "middlename": middlename,
                            "lastname": surname
                        }
                        authors.append(author_data)

            # Verificamos si obtuvimos autores; si la lista está vacía, registramos en log
            if not authors:
                logging.warning(f"No se encontraron autores principales para {filename}")

            # Crear diccionario de datos del paper
            paper_data = {
                "filename": filename,
                "title": title,
                "authors": authors,  # Nueva entrada para autores
                "publicationYear": publicationYear,
                "publishedIn": publishedIn,
                "doi": doi,
                "abstract": abstract
            }
            
            papers_data.append(paper_data)
            logging.info(f"Procesado correctamente: {filename}")
            
        except Exception as e:
            logging.error(f"Error procesando {filename}: {e}")
            import traceback
            logging.error(traceback.format_exc())
    
    # Escribir todos los datos al archivo JSON
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({"papers": papers_data}, f, ensure_ascii=False, indent=2)
        logging.info(f"Archivo JSON guardado en: {output_file}")
    except Exception as e:
        logging.error(f"Error guardando archivo JSON: {e}")

    # Escribir todos los datos al archivo CSV
    try:
        csv_file = os.path.join(output_folder, "papers_metadata.csv")
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            # Escribir encabezados
            writer.writerow(["filename", "title", "authors", "publicationYear", "publishedIn", "doi", "abstract"])
            # Escribir datos
            for paper in papers_data:
                writer.writerow([
                    paper["filename"],
                    paper["title"],
                    "; ".join([f"{author['firstname']} {author['middlename']} {author['lastname']}".strip() for author in paper["authors"]]),
                    paper["publicationYear"],
                    paper["publishedIn"],
                    paper["doi"],
                    paper["abstract"]
                ])
        logging.info(f"Archivo CSV guardado en: {csv_file}")
    except Exception as e:
        logging.error(f"Error guardando archivo CSV: {e}")