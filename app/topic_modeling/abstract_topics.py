import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from bertopic import BERTopic
import matplotlib.pyplot as plt
import os
import pandas as pd

def load_papers():
    """Load paper data from JSON file"""
    with open(os.path.join("output","papers_with_openalex.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["papers"]

def extract_abstracts(papers):
    """Extract abstracts from papers"""
    abstracts = []
    for paper in papers:
        abstract = paper.get("abstract", "")
        if abstract and len(abstract) > 50:  # Ensure abstract has meaningful content
            abstracts.append(abstract)
    return abstracts

def lda_topic_modeling(abstracts, n_topics=5):
    """Perform LDA topic modeling on abstracts"""
    # Vectorize abstracts
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    X = vectorizer.fit_transform(abstracts)
    
    # Create LDA model
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(X)
    
    # Extract feature names
    feature_names = vectorizer.get_feature_names_out()
    
    # Extract topics
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words_idx = topic.argsort()[:-11:-1]  # Get indices of top 10 words
        top_words = [feature_names[i] for i in top_words_idx]
        topics.append({
            "id": topic_idx,
            "words": top_words
        })
    
    # Assign topics to papers
    doc_topics = lda.transform(X)
    assignments = []
    for i, doc_topic in enumerate(doc_topics):
        primary_topic = doc_topic.argmax()
        assignments.append({
            "abstract_idx": i,
            "topic_id": int(primary_topic),
            "confidence": float(doc_topic[primary_topic])
        })
    
    return {
        "topics": topics,
        "assignments": assignments
    }

def bertopic_modeling(abstracts):
    """Use BERTopic for topic modeling"""
    # Create BERTopic model
    model = BERTopic()
    topics, probs = model.fit_transform(abstracts)
    
    # Extract topic information
    topic_info = model.get_topic_info()
    
    # Convert to serializable format
    topic_data = []
    for index, row in topic_info.iterrows():
        if index != -1:  # Skip outlier topic
            # The issue is here - we need to check if get_topic returns a list
            topic_words = model.get_topic(index)
            if topic_words and isinstance(topic_words, list):
                words = [word for word, _ in topic_words][:10]
                topic_data.append({
                    "id": int(index),
                    "name": row["Name"],
                    "count": int(row["Count"]),
                    "words": words
                })
    
    # Assign topics to abstracts
    assignments = []
    for i, topic_id in enumerate(topics):
        if topic_id != -1:  # Skip outliers
            # Handle the case when topic might not be in probs
            confidence = 0.0
            if i < len(probs) and isinstance(probs[i], dict) and topic_id in probs[i]:
                confidence = float(probs[i][topic_id])
            assignments.append({
                "abstract_idx": i,
                "topic_id": int(topic_id),
                "confidence": confidence
            })
    
    return {
        "topics": topic_data,
        "assignments": assignments
    }

def visualize_topics(topic_data, method):
    """Create visualizations for topic modeling results"""
    os.makedirs("output", exist_ok=True)
    
    # Create bar chart of topics and their word counts
    topics = topic_data["topics"]
    
    plt.figure(figsize=(12, 8))
    for i, topic in enumerate(topics[:5]):  # Show top 5 topics
        words = topic["words"][:5]  # Top 5 words
        plt.bar(
            [f"T{topic['id']}-{word}" for word in words], 
            [1] * len(words),
            label=f"Topic {topic['id']}"
        )
    
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Top Words in Topics ({method})")
    plt.tight_layout()
    plt.savefig(os.path.join("output",f"topics_{method}.png"))
    
    # Save topic data
    with open(os.path.join("output",f"topics_{method}.json"), "w") as f:
        json.dump(topic_data, f, indent=2)
    
    print(f"✓ {method} topic modeling results saved to output folder")

def create_topic_modeling():
    # Load papers
    papers = load_papers()
    print(f"Loaded {len(papers)} papers")
    
    # Extract abstracts
    abstracts = extract_abstracts(papers)
    print(f"Extracted {len(abstracts)} abstracts")
    
    # Perform LDA topic modeling
    lda_results = lda_topic_modeling(abstracts)
    visualize_topics(lda_results, "LDA")
    
    # Perform BERTopic modeling (HuggingFace-based approach)
    bertopic_results = bertopic_modeling(abstracts)
    visualize_topics(bertopic_results, "BERTopic")