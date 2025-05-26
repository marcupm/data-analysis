import streamlit as st
import json
import networkx as nx
from pyvis.network import Network
from streamlit.components.v1 import html

# Load JSON graph file
@st.cache_data
def load_graph(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_graph("../app/output/paper_similarities.json")

papers = data["papers"]
links = data["links"]

# Build mapping from id to title
id_to_title = {p["id"]: p["title"] for p in papers}

# Sidebar: Select paper to highlight
selected_title = st.sidebar.selectbox(
    "Select paper to highlight", 
    options=[p["title"] for p in papers]
)

# Find id of selected paper
selected_id = None
for p in papers:
    if p["title"] == selected_title:
        selected_id = p["id"]
        break

# Build NetworkX graph
G = nx.Graph()
for p in papers:
    G.add_node(p["id"], title=p["title"])

for link in links:
    if link["similarity"] >= data.get("similarity_threshold", 0.6):
        G.add_edge(link["source"], link["target"], weight=link["similarity"])

# Create PyVis network
net = Network(height="800px", width="100%", notebook=False)

# Add nodes with coloring: red if selected, else default blue
for node_id, attrs in G.nodes(data=True):
    if node_id == selected_id:
        color = "rgba(255,0,0,1)"  # bright red, fully opaque
    else:
        color = "rgba(0,0,255,0.3)"  # blue, 20% opacity
    net.add_node(node_id, label=attrs["title"], title=attrs["title"], color=color, font={"size": 24, "face": "arial"})

# Add edges
for source, target, attrs in G.edges(data=True):
        net.add_edge(source, target, value=0.02)


net.set_options("""
var options = {
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -30000,
      "centralGravity": 0.3,
      "springLength": 800,
      "springConstant": 0.1,
      "damping": 0.5,
      "avoidOverlap": true
    },
    "minVelocity": 0.75
  },
  "interaction": {
    "hover": true,
    "multiselect": true,
    "dragNodes": true
  },
  "stabilization": {
    "enabled": true,
    "iterations": 3000,
    "updateInterval": 50,
    "fit": true
  }
}
""")

# Generate and display graph
net.write_html("graph.html")
html(open("graph.html", "r", encoding="utf-8").read(), height=650)
