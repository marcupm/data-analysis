# Usage

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

## After running the project
After execution, an `output` folder will be created inside the IndividualAssessment directory, containing three files:
- `figures_per_article.png`: A graph showing the number of figures per article
- `keyword_cloud.png`: A word cloud generated from the abstracts
- `links.txt`: A list of links extracted from the papers

For more details, check the full [documentation](index.md) 