# Usage
### Docker Execution
#### Requirements
It is mandatory to first follow the instructions in the [installation](install.md) file to properly install all the requirements to use the program
#### Before running the project
- Place your PDF files in the `data-analysis/data` folder
#### Running the Project
To run the project, use the following command:
```bash
docker-compose up -d
```
#### Stopping the Project
The Docker containers will run in the background until you stop them:
```bash
# Press CTRL+C in the terminal where docker-compose is running
docker-compose down
```
## After running the project
After execution, an `output` folder will be created inside the data-analysis directory, containing all the documents created through the execution, being possible to see every step taken by the program.
Among the output files, the more interesting ones are:
- papers_wikidata_enriched.ttl  # Final RDF file with paper's metadata enriched with openalex and wikidata
- provenance.provn              # Provenance file in .provn format, also available in .xml and .json
- topics_BERTopic.png           # Graph with the topics that appear the most among the papers
- similarity_network.png        # Graph with the relation of topics found between the papers analyzed
- workflow.png                  # Schema with a detailed explanation of the workflow steps

For more details, check the full [documentation](index.md) 
