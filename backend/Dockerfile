# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy only requirements file first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend app into the container
COPY . .

# Copy the example env file as .env inside the container
COPY .env.example .env

# Expose port 8000 (FastAPI via uvicorn)
EXPOSE 8000

# Run the application (with hot-reload for dev)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
