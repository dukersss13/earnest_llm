# Use the official Python base image
FROM python:3.10.0

# Set the working directory in the container
WORKDIR /earnest_llm

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /earnest_llm