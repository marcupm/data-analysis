# Use Python 3.9.13 as the base image
FROM python:3.9.13

RUN apt-get update && apt-get install -y graphviz && apt-get clean

COPY docs/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory inside the container to IndividualAssessment
WORKDIR /app

# Copy folder into the container
COPY app /app
COPY data /data
COPY api /api

# Set the default command to run the main script
CMD ["python", "main.py"]
