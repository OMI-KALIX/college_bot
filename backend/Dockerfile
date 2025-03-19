# Use the official Python image
FROM python:3.11

# Install system dependencies, including SQLite3
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Set the working directory inside the container
WORKDIR /backend

# Copy only the backend directory contents into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI on port 8000
EXPOSE 8000

# ✅ Run Uvicorn with the correct path
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
