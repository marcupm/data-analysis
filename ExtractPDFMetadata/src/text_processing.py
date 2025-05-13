import re
from collections import Counter

def extract_abstract_keywords(papers):
    """Extract keywords from the abstracts of the papers."""
    keyword_counts = Counter()

    for paper, text in papers.items():
        match = re.search(r"<abstract>(.*?)</abstract>", text, re.DOTALL) # Extract the abstract text
        if match:
            abstract_text = match.group(1)
            words = re.findall(r"\b\w{4,}\b", abstract_text.lower())  # words of 4 or more characters
            filtered_words = [word for word in words if not any(substring in word for substring in ["http://www.tei-c.org/ns/1.0", "xmlns", "http"])]  # Remove URLs and unwanted substrings from keywords
            keyword_counts.update(filtered_words)

    return keyword_counts
