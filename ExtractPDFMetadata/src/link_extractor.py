import re

def extract_links(papers):
    """Extract links from the papers."""
    links_per_paper = {}

    for paper, text in papers.items():
        links = re.findall(r"https?://\S+", text)  # Find all URLs
        filtered_links = [link for link in links if "http://www.tei-c.org/ns/1.0" not in link]
        links_per_paper[paper] = filtered_links

    return links_per_paper
