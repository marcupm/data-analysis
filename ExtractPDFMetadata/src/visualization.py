import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud

def generate_keyword_cloud(keyword_data, output_file):
    """Generate a word cloud from the keyword data."""
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(keyword_data)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(output_file)
    plt.close()

def figures_per_article(papers):
    figure_counts = {}

    for paper, text in papers.items():

        figure_count = len(re.findall(r"<head>Figure \d+", text))
        ref_count = len(re.findall(r'<ref type="figure">\d+</ref>', text))
        generic_heads = re.finditer(r"<head>\s*Figure\s*</head>", text) #Some papers have figures without numbers
        for match in generic_heads:
            # Find the figure number in the figDesc tag
            figdesc_match = re.search(r"<figDesc>[^<]*?(\d+(?:,\s*\d+)*)", text[match.end():])
            if figdesc_match:
                numbers = set(figdesc_match.group(1).replace(" and ", ",").split(","))
                figure_count += len(numbers)
        if figure_count == 0:
            figure_counts[paper] = ref_count #Some papers have references to figures instead of the actual figure
        else:
            figure_counts[paper] = figure_count
    return figure_counts

def plot_figures_per_article(papers, output_file):
    """Chart of the number of figures per article"""
    figure_counts = figures_per_article(papers)

    plt.figure(figsize=(20, 14))
    plt.bar(figure_counts.keys(), figure_counts.values(), color="skyblue")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Papers")
    plt.ylabel("Number of Figures")
    plt.title("Figures per Article")
    plt.tight_layout() # Adjust the plot to ensure everything fits without overlapping
    plt.savefig(output_file)
    plt.close()
