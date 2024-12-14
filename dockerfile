# Use the official Python base image
FROM python:3.10.14-slim

# Set the working directory in the container
WORKDIR /earnest_llm

# Install git
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install dependencies
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
