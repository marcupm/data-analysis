import json
import re
import os
from transformers import pipeline
import matplotlib.pyplot as plt

def load_papers():
    """Load paper data from JSON file"""
    with open("../create_rdf/papers_with_openalex.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["papers"]

# Modify load_papers function to also load GROBID XML
def load_papers_with_grobid():
    """Load papers with GROBID XML if available"""
    # Load papers metadata
    with open("../create_rdf/papers_with_openalex.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    papers = data["papers"]
    
    # Try to load GROBID output
    grobid_papers = {}
    try:
        with open("../ExtractPDFMetadata/output/grobid_output.json", "r", encoding="utf-8") as f:
            grobid_papers = json.load(f)
    except FileNotFoundError:
        print("No GROBID output file found")
    
    # Merge GROBID data with papers
    for i, paper in enumerate(papers):
        filename = f"paper_{i}.pdf"
        if filename in grobid_papers:
            paper["grobid_xml"] = grobid_papers[filename]
    
    return papers

def extract_acknowledgements(paper_text):
    """Extract acknowledgements section from paper full text"""
    # Common patterns for acknowledgements sections
    patterns = [
        r"(?i)(?:acknowledgements?|funding)\s*(?:\n|:)(.*?)(?:\n\s*\n|\n\s*[A-Z][a-z]*\s+\n|\n\d\.|\nreferences)",
        r"(?i)(?:acknowledgements?|funding)[^\n]*\n(.*?)(?:\n\s*\n|\nreferences|\n\d\.)",
        r"(?i)(?:We (?:gratefully )?acknowledge)(.*?)(?:\n\s*\n|\nreferences|\n\d\.)"
    ]
    
    for pattern in patterns:
        matches = re.search(pattern, paper_text, re.DOTALL)
        if matches:
            section = matches.group(1).strip()
            if len(section) > 20:  # Ensure it's substantial
                return section
    
    return ""

# Add this function to extract acknowledgements from GROBID XML
def extract_acknowledgements_from_grobid(xml_text):
    """Extract acknowledgements from GROBID XML output"""
    if not xml_text:
        return ""
        
    # Look for acknowledgement section in GROBID XML
    ack_pattern = r'<div xmlns="http://www.tei-c.org/ns/1.0">\s*<head>Acknowledgement[s]?</head>(.*?)</div>'
    matches = re.search(ack_pattern, xml_text, re.DOTALL | re.IGNORECASE)
    
    if matches:
        # Clean up the HTML tags
        text = matches.group(1)
        text = re.sub(r'<[^>]+>', ' ', text)  # Remove HTML tags
        text = re.sub(r'\s+', ' ', text).strip()  # Clean up whitespace
        return text
        
    return ""

def extract_entities_from_acknowledgements(acknowledgements):
    """Extract named entities from acknowledgements text using HuggingFace NER model"""
    if not acknowledgements:
        return []
    
    # Load NER pipeline from HuggingFace
    ner = pipeline("ner", model="Jean-Baptiste/roberta-large-ner-english", aggregation_strategy="simple")
    
    # Run NER on acknowledgements text
    try:
        entities = ner(acknowledgements)
        
        # Process entities
        results = []
        for entity in entities:
            # Filter entities by type and length
            if entity["entity_group"] in ["ORG", "PER"] and len(entity["word"]) > 1:
                results.append({
                    "text": entity["word"],
                    "type": entity["entity_group"],
                    "score": float(entity["score"])
                })
        
        return results
    except Exception as e:
        print(f"Error processing text: {str(e)}")
        return []

def identify_funding_organizations(entities):
    """Identify potential funding organizations from extracted entities"""
    # Keywords that suggest funding organizations
    funding_keywords = [
        "grant", "fund", "support", "award", "project", "research", "foundation",
        "nsf", "nih", "funding", "program", "fellowship", "scholarship"
    ]
    
    funders = []
    for entity in entities:
        if entity["type"] == "ORG" and entity["score"] > 0.8:
            # Check if this looks like a funding organization
            is_funder = any(keyword in entity["text"].lower() for keyword in funding_keywords)
            
            if is_funder:
                funders.append({
                    "name": entity["text"],
                    "score": entity["score"],
                    "type": "funder"
                })
    
    return funders

def process_papers_acknowledgements(papers):
    """Process acknowledgements for all papers"""
    os.makedirs("output", exist_ok=True)
    
    results = []
    
    for i, paper in enumerate(papers):
        # Look for text in different possible fields
        text_candidates = []
        
        # Check various possible fields that might contain acknowledgements
        if "full_text" in paper:
            text_candidates.append(paper["full_text"])
        if "abstract" in paper and paper["abstract"]:
            text_candidates.append(paper["abstract"])
        if "body" in paper and paper["body"]:
            text_candidates.append(paper["body"])
        if "grobid_xml" in paper and paper["grobid_xml"]:
            text_candidates.append(extract_acknowledgements_from_grobid(paper["grobid_xml"]))
            
        # If we have no text sources, skip this paper
        if not text_candidates:
            print(f"Skipping paper {i}: No text content found")
            continue
            
        # Try to extract acknowledgements from each text source
        found_ack = False
        for text in text_candidates:
            acknowledgements = extract_acknowledgements(text)
            if acknowledgements:
                found_ack = True
                # Extract entities
                entities = extract_entities_from_acknowledgements(acknowledgements)
                
                # Identify funding organizations
                funders = identify_funding_organizations(entities)
                
                # Save results
                result = {
                    "paper_id": i,
                    "title": paper.get("title", ""),
                    "acknowledgements": acknowledgements,
                    "entities": entities,
                    "funders": funders
                }
                
                results.append(result)
                print(f"Found acknowledgements in paper {i}: '{paper.get('title', '')[:40]}...'")
                break
                
        if not found_ack:
            print(f"No acknowledgements found in paper {i}: '{paper.get('title', '')[:40]}...'")
    
    # Save results
    with open("output/acknowledgements_analysis.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Create visualization
    if results:
        visualize_funding_organizations(results)
    else:
        print("No acknowledgements found in any papers. Cannot create visualization.")
    
    return results

def visualize_funding_organizations(results):
    """Create visualization of funding organizations"""
    # Collect all funders
    all_funders = {}
    for result in results:
        for funder in result["funders"]:
            name = funder["name"]
            if name in all_funders:
                all_funders[name] += 1
            else:
                all_funders[name] = 1
    
    # Sort funders by frequency
    sorted_funders = sorted(all_funders.items(), key=lambda x: x[1], reverse=True)
    
    # Create bar chart
    if sorted_funders:
        plt.figure(figsize=(10, 6))
        names = [name for name, count in sorted_funders[:15]]  # Top 15
        counts = [count for name, count in sorted_funders[:15]]
        
        plt.barh(names, counts)
        plt.xlabel("Number of papers")
        plt.ylabel("Funding organization")
        plt.title("Most common funding organizations")
        plt.tight_layout()
        plt.savefig("output/funding_organizations.png")
        
        print(f"✓ Funding organizations visualization saved to output/funding_organizations.png")

if __name__ == "__main__":
    # Load papers
    papers = load_papers_with_grobid()
    print(f"Loaded {len(papers)} papers")
    
    # Extract acknowledgements and perform NER
    results = process_papers_acknowledgements(papers)
    print(f"Processed acknowledgements for {len(results)} papers")