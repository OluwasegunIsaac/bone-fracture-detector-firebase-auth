# Use official Python slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt before other files to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files (including pages/ directory)
COPY . .

# Expose port
EXPOSE 8080

# Command to run the application
CMD ["streamlit", "run", "main.py", "--server.address", "0.0.0.0", "--server.port", "8080"]
