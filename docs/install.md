# Installation

## Prerequisites
Before installing, make sure you have the following dependencies installed:
- Python 3.x
- Git
- pip (Python package manager)

## Installation Steps
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