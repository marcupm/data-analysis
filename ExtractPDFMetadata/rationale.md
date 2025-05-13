# Rationale

## Project Overview

This project aims to analyze 10 open-access articles using Grobid and other text analysis tools. The program performs the following tasks:
1. Draws a keyword cloud based on the abstract information.
2. Creates a visualization showing the number of figures per article.
3. Creates a list of the links found in each paper.

## Project Structure

The project is organized into the following files:
- `main.py`: The main script that orchestrates the entire analysis process.
- `src/grobid_client.py`: Contains the function to process PDFs using Grobid.
- `src/text_processing.py`: Contains the function to extract keywords from the abstracts.
- `src/link_extractor.py`: Contains the function to extract links from the papers.
- `src/visualization.py`: Contains functions to generate a keyword cloud and plot the number of figures per article.

## Steps and Validation

### 1. Processing PDFs with Grobid

**Function**: `process_papers` in `grobid_client.py`

**Description**: This function sends PDFs to Grobid for processing and returns the extracted text.

**Validation**: 
- Verified that the function correctly sends requests to the Grobid API and handles responses.
- Checked that the extracted text is correctly stored in the `processed_papers` dictionary.

### 2. Extracting Keywords from Abstracts

**Function**: `extract_abstract_keywords` in `text_processing.py`

**Description**: This function extracts keywords from the abstracts of the papers.

**Validation**: 
- Ensured that the function correctly identifies and extracts the abstract text using regular expressions.
- Verified that the extracted keywords are filtered to remove unwanted substrings and URLs.
- Checked that the keyword counts are correctly updated in the `Counter` object.

### 3. Generating a Keyword Cloud

**Function**: `generate_keyword_cloud` in `visualization.py`

**Description**: This function generates a word cloud from the keyword data.

**Validation**: 
- Verified that the function correctly generates a word cloud using the `WordCloud` library.
- Ensured that the word cloud is saved to the specified output file.

### 4. Plotting Figures per Article

**Function**: `plot_figures_per_article` in `visualization.py`

**Description**: This function creates a chart showing the number of figures per article.

**Validation**: 
- Ensured that the function correctly counts the number of figures in each article.
- Verified that the bar chart is correctly generated using `matplotlib`.
- Checked that the chart is saved to the specified output file.

### 5. Extracting Links from Papers

**Function**: `extract_links` in `link_extractor.py`

**Description**: This function extracts links from the papers.

**Validation**: 
- Verified that the function correctly identifies and extracts URLs using regular expressions.
- Ensured that unwanted URLs are filtered out.
- Checked that the extracted links are correctly stored in the `links_per_paper` dictionary.

## Conclusion

The project successfully performs the required analysis on the open-access articles. Each step has been validated to ensure correctness and reliability. The results are saved in the `output` folder, including the keyword cloud, the figures per article chart, and the list of links found in each paper.

By following best practices and validating each step, I ensure that the analysis is accurate and the results are meaningful.