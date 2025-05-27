import streamlit as st
import json
import networkx as nx
from pyvis.network import Network
from streamlit.components.v1 import html

st.set_page_config(layout="wide")

@st.cache_data
def load_graph(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_graph("./paper_similarities.json")

papers = data["papers"]
links = data["links"]

id_to_title = {p["id"]: p["title"] for p in papers}

selected_title = st.sidebar.selectbox(
    "Select paper to highlight", 
    options=[p["title"] for p in papers]
)

selected_id = None
for p in papers:
    if p["title"] == selected_title:
        selected_id = p["id"]
        break
      
threshold = st.sidebar.slider(
    "Similarity threshold", 
    min_value=0.5, 
    max_value=0.8, 
    value=0.6, 
    step=0.01
)

G = nx.Graph()
for p in papers:
    G.add_node(p["id"], title=p["title"])

for link in links:
    if link["similarity"] >= threshold:
        G.add_edge(link["source"], link["target"], weight=link["similarity"])

net = Network(height="1000px", width="100%", notebook=False)

related_nodes = set()
if selected_id is not None:
    related_nodes.add(selected_id)
    related_nodes.update(G.neighbors(selected_id))

for node_id, attrs in G.nodes(data=True):
    if node_id == selected_id:
        color = "rgba(255,0,0,1)"
    elif node_id in related_nodes:
        color = "rgba(0,0,255,1)"
    else:
        color = "rgba(0,0,255,0.1)" 
    net.add_node(node_id, label=attrs["title"], title=attrs["title"], color=color, font={"size": 40, "face": "arial"})

for source, target, attrs in G.edges(data=True):
    if selected_id is not None and (source == selected_id or target == selected_id):
        color = "rgba(255,0,0,0.7)" 
    else:
        color = "rgba(0,0,0,0.1)"
    net.add_edge(source, target, value=0.02, color=color)


net.set_options("""
var options = {
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -15000,
      "centralGravity": 0.2,
      "springLength": 1000,
      "springConstant": 0.01,
      "damping": 0.8,
      "avoidOverlap": 1
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

net.write_html("graph.html")
html(open("graph.html", "r", encoding="utf-8").read(), height=2000, width=0, scrolling=False)
