# Use an official Python image as the base
FROM python:3.13.3-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install system dependencies required for tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    libffi-dev \
    libssl-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install required Python dependencies
RUN pip install --no-cache-dir rets

# Command to run the Python script
CMD ["python", "refindly_rets_v2.py"]