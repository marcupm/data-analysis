import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import networkx as nx
import os

def load_papers():
    """Load paper data from JSON file"""
    with open("../create_rdf/output/papers_with_openalex.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["papers"]

def create_abstract_embeddings(papers):
    """Create embeddings for paper abstracts using a transformer model"""
    # Load model
    print("Loading sentence transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Extract abstracts
    abstracts = []
    paper_ids = []
    titles = []
    
    for i, paper in enumerate(papers):
        abstract = paper.get("abstract", "")
        if abstract and len(abstract) > 50:  # Ensure abstract has meaningful content
            abstracts.append(abstract)
            paper_ids.append(i)
            titles.append(paper.get("title", f"Paper {i}"))
    
    # Create embeddings
    print(f"Creating embeddings for {len(abstracts)} abstracts...")
    embeddings = model.encode(abstracts)
    
    return embeddings, paper_ids, titles

def calculate_similarity_matrix(embeddings):
    """Calculate cosine similarity matrix between embeddings"""
    similarity_matrix = cosine_similarity(embeddings)
    # Set diagonal to 0 to ignore self-similarity
    np.fill_diagonal(similarity_matrix, 0)
    return similarity_matrix

def find_most_similar_pairs(similarity_matrix, paper_ids, titles, top_n=10):
    """Find the top N most similar paper pairs"""
    # Flatten the upper triangle of the similarity matrix
    n = similarity_matrix.shape[0]
    upper_triangle_indices = np.triu_indices(n, k=1)
    similarities = similarity_matrix[upper_triangle_indices]
    
    # Get indices of top N similarities
    top_indices = np.argsort(similarities)[-top_n:]
    
    # Convert flat indices to 2D indices
    pairs = []
    for idx in top_indices:
        i = upper_triangle_indices[0][idx]
        j = upper_triangle_indices[1][idx]
        sim = similarities[idx]
        pairs.append({
            "paper1_id": paper_ids[i],
            "paper1_title": titles[i],
            "paper2_id": paper_ids[j],
            "paper2_title": titles[j],
            "similarity": float(sim)
        })
    
    return sorted(pairs, key=lambda x: x["similarity"], reverse=True)

def visualize_similarity_network(similarity_matrix, paper_ids, titles, threshold=0.5):
    """Create a network visualization of paper similarities"""
    os.makedirs("output", exist_ok=True)
    
    # Create graph
    G = nx.Graph()
    
    # Add nodes
    for i, paper_id in enumerate(paper_ids):
        G.add_node(paper_id, title=titles[i])
    
    # Add edges for similarities above threshold
    n = similarity_matrix.shape[0]
    for i in range(n):
        for j in range(i+1, n):
            if similarity_matrix[i, j] >= threshold:
                G.add_edge(paper_ids[i], paper_ids[j], weight=similarity_matrix[i, j])
    
    # Draw graph
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G, seed=42)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=100, alpha=0.8)
    
    # Draw edges with width proportional to similarity
    edges = [(u, v) for u, v, d in G.edges(data=True)]
    weights = [G[u][v]["weight"] * 2 for u, v in edges]
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=weights, alpha=0.5)
    
    # Draw labels
    labels = {node: G.nodes[node]["title"][:20] + "..." for node in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)
    
    plt.axis("off")
    plt.title(f"Paper Similarity Network (threshold={threshold})")
    plt.tight_layout()
    plt.savefig("output/similarity_network.png", dpi=300)
    
    # Save similarity data
    with open("output/paper_similarities.json", "w") as f:
        json.dump({
            "similarity_threshold": threshold,
            "papers": [{"id": paper_ids[i], "title": titles[i]} for i in range(len(paper_ids))],
            "links": [{"source": paper_ids[i], "target": paper_ids[j], "similarity": float(similarity_matrix[i, j])}
                     for i in range(n) for j in range(i+1, n) if similarity_matrix[i, j] >= threshold]
        }, f, indent=2)
    
    print(f"✓ Similarity network visualization saved to output/similarity_network.png")

if __name__ == "__main__":
    # Load papers
    papers = load_papers()
    print(f"Loaded {len(papers)} papers")
    
    # Create embeddings
    embeddings, paper_ids, titles = create_abstract_embeddings(papers)
    
    # Calculate similarity matrix
    similarity_matrix = calculate_similarity_matrix(embeddings)
    
    # Find most similar pairs
    similar_pairs = find_most_similar_pairs(similarity_matrix, paper_ids, titles, top_n=15)
    print("\nMost similar paper pairs:")
    for i, pair in enumerate(similar_pairs):
        print(f"{i+1}. [{pair['similarity']:.2f}] '{pair['paper1_title']}' and '{pair['paper2_title']}'")
    
    # Visualize similarity network
    visualize_similarity_network(similarity_matrix, paper_ids, titles, threshold=0.45)