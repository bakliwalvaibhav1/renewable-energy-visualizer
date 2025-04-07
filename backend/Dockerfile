# 1️⃣ Use an official lightweight Python image
FROM python:3.11-slim

# 2️⃣ Set working directory inside the container
WORKDIR /app

# 3️⃣ Copy only requirements file first for layer caching
COPY requirements.txt .

# 4️⃣ Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copy the rest of the backend app into the container
COPY . .

# 6️⃣ Expose port 8000 (FastAPI via uvicorn)
EXPOSE 8000

# 7️⃣ Run the application (with hot-reload for dev)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
