# Installation

## Prerequisites
Before installing, make sure you have the following dependencies installed:
- Docker and Docker Compose
- Python 3.9+
- Git
- pip (Python package manager)
- Research papers in PDF format to be analysized
  
## Installation Steps
Clone the repository:
```bash
   git clone [url-github](https://github.com/marcupm/data-analysis.git)
   cd data-analysis
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
    pip install -r requirements.txt
```

Verify the installation:
```bash
    python --version
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
- Configure the project to work with all the requirements intalled
