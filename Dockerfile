# Use Python 3.9.13 as the base image
FROM python:3.9.13

RUN apt-get update && apt-get install -y graphviz && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
