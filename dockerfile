# Use Python 3.9.13 as the base image
FROM python:3.9.13

# Set the working directory inside the container to IndividualAssessment
WORKDIR /IndividualAssessment

# Copy only the dependencies file first (from root/docs)
COPY docs/requirements.txt /docs/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /docs/requirements.txt

# Copy the whole IndividualAssessment folder into the container
COPY IndividualAssessment /IndividualAssessment

# Set the default command to run the main script
CMD ["python", "main.py"]
