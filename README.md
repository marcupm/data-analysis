# AIOSRSE-UPM
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14957145.svg)](https://doi.org/10.5281/zenodo.14957145)

## Description
This repository contains deliverables related to Artificial Intelligence and Open Science in Research Software Engineering. Currently, it only contains IndividualAssessment, which is a Grobid client that extracts links, generates a word cloud from abstracts, and creates a figure-per-article graph from PDF papers.

## Repository Structure
```
AIOSRSE-UPM/
├── IndividualAssessment/  # Main project folder
│   ├── data/              # Place your PDF files here
│   ├── main.py            # Main execution script
│   └── ...
└── docs/
    └── requirements.txt   # Dependencies file
```

## Requirements
- Python 3.9.13 or higher
- A running Grobid service (default: http://localhost:8070)
- Dependencies listed in docs/requirements.txt

## Installation
Clone the repository:
```bash
   git clone https://github.com/AlRos14/AIOSRSE-UPM.git
   cd IndividualAssessment
```

### Local Installation
Follow these instructions if you want to run the project with a Grobid instance on your local machine.

Create and activate a virtual environment (optional but recommended):
```bash
    python3 -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
```

Install the required dependencies:
```bash
    pip install -r docs/requirements.txt
```

Verify the installation:
```bash
    python main.py --help
```

### Docker Installation
Follow these instructions if you prefer using Docker without worrying about dependencies or Grobid setup.

Build docker containers with Docker-Compose
```bash
    docker-compose up --build
```
This will automatically:
- Set up a Grobid instance
- Install all required dependencies
- Configure the project to work with the containerized Grobid

## Execution

### Local Execution

#### Requirements
It is mandatory to have a running Grobid instance, as this project is essentially a Grobid client.
Additionally, Python dependencies must be installed from the requirements.txt file.

#### Before running the project
1. Ensure a Grobid instance is running (by default at http://localhost:8070)
2. Place your PDF files in the `IndividualAssessment/data` folder

#### Running the Project
To run the project, use the following command:
```bash
python main.py
```

### Docker Execution

#### Running the Project
If you've already built the containers, simply run:
```bash
docker-compose up
```
#### Stopping the Project
The Docker containers will run in the background until you stop them:
```bash
# Press CTRL+C in the terminal where docker-compose is running
docker-compose down
```

### After running the project
After execution, an `output` folder will be created inside the IndividualAssessment directory, containing three files:
- `figures_per_article.png`: A graph showing the number of figures per article
- `keyword_cloud.png`: A word cloud generated from the abstracts
- `links.txt`: A list of links extracted from the papers

## Running Example(s)
This is a running example using ten AI-related articles:

    python main.py       
    2025-02-18 14:07:58,742 - INFO - Iniciando el análisis de artículos...
    2025-02-18 14:07:58,742 - INFO - Processing: 2305.04532v2.pdf
    2025-02-18 14:08:32,068 - INFO - Processing: 2309.05519v3.pdf
    2025-02-18 14:08:38,456 - INFO - Processing: 2403.09611v4.pdf
    2025-02-18 14:08:44,838 - INFO - Processing: 2404.17605v1.pdf
    2025-02-18 14:08:48,925 - INFO - Processing: 31664-Article Text-35728-1-2-20241016.pdf
    2025-02-18 14:08:51,934 - INFO - Processing: 3649217.3653594.pdf
    2025-02-18 14:08:55,379 - INFO - Processing: AIp2300031.pdf
    2025-02-18 14:08:57,199 - INFO - Processing: GPT-4Vision_for_Robotics_Multimodal_Task_Planning_From_Human_Demonstration.pdf
    2025-02-18 14:09:00,477 - INFO - Processing: GPT_Generative_Pre-Trained_Transformer_A_Comprehensive_Review_on_Enabling_Technologies_Potential_Applications_Emerging_Challenges_and.pdf
    2025-02-18 14:09:10,667 - INFO - Processing: RTLCoder_Outperforming_GPT-3.5_in_Design_RTL_Generation_with_Our_Open-Source_Dataset_and_Lightweight_Solution.pdf
    2025-02-18 14:09:15,003 - INFO - Análisis completado. Resultados guardados en la carpeta output/

figures_per_article.png:
![alt text](IndividualAssessment/output/figures_per_article.png)
keyword_cloud.png:
![alt text](IndividualAssessment/output/keyword_cloud.png)
links.txt:
[links](IndividualAssessment/output/links.txt)

## Preferred Citation
A citation file is included in this repository. Please refer to the `CITATION.cff` file for proper citation format.

