# Use Python 3.10 slim image for amd64 CPU
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY app /app/app
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make sure input/output folders exist
RUN mkdir -p /app/input /app/output

# Set the default command
CMD ["python", "app/main.py"]
