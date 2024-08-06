# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    postgresql-client \
    python3.10 \
    python3-pip \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Azure CLI
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

# Install Azure Developer CLI (azd)
RUN curl -fsSL https://aka.ms/install-azd.sh | bash

# Set up Python
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Install Docker
RUN curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh

# Set the working directory
WORKDIR /workspace

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Install pgvector (assuming it's a Python package in this context)
RUN pip install pgvector

# Upgrade npm and install latest LTS version of Node.js
RUN npm install -g n && n lts

# Clean up
RUN apt-get autoremove -y && apt-get clean -y

# Set the default command
CMD ["/bin/bash"]