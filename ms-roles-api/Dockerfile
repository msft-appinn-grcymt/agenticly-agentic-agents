FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables for Cosmos DB (can be overridden at runtime)
ENV USE_COSMOS_DB=false
ENV COSMOS_ENDPOINT=""
ENV COSMOS_KEY=""
ENV COSMOS_DATABASE_NAME=employees-db
ENV COSMOS_CONTAINER_NAME=employees

# Expose port 8000
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
