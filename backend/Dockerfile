# Use the official Python image
FROM python:3.11

# Install system dependencies, including SQLite3
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /backend

# Copy requirements file first for better caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all backend files into the container
COPY . .

# Ensure the backend is a Python package
RUN touch /backend/__init__.py

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI using Uvicorn
CMD ["uvicorn", "backend.app2:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

