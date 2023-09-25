# Use the official Python image as the base image
FROM python:3.8

# Set the working directory within the container
WORKDIR /Stay_Synergy

RUN pip install email-validator
RUN pip install python-multipart

# Copy the requirements file into the container
COPY requirements.txt /Stay_Synergy/

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /Stay_Synergy/
WORKDIR /Stay_Synergy/

# Specify the command to run your application
CMD ["python", "main.py"]
