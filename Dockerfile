# Use Python 3.11 bookworm as base image
FROM python:3.11-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -s /bin/bash jupyter

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir jupyterlab

# set up Jupyter settings
COPY --chown=jupyter:jupyter ./overrides.json /usr/local/share/jupyter/lab/settings/overrides.json

# Create and set permissions on work directory
RUN mkdir -p /home/jupyter/work && chown -R jupyter:jupyter /home/jupyter

# Set the working directory to the jupyter home
WORKDIR /home/jupyter/work

# Switch to non-root user
USER jupyter

# Expose JupyterLab port
EXPOSE 8888

# Command to run JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.password=''"]
