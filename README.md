# ⚡ Renewable Energy Visualizer

A full-stack web application to track, analyze, and visualize renewable energy data — powered by FastAPI, React, PostgreSQL, and Docker. Features secure user authentication, energy data dashboards, and a beautiful developer experience.

---

## 🌿 Features

- 🔐 User authentication (register/login) using JWT
- 📊 Energy consumption & generation tracking
- 📈 Chart.js for interactive visualizations
- 🐳 Dockerized backend, frontend, and database
- 🚀 CI/CD pipeline with GitHub Actions
- 💡 Fully type-safe with static analysis and tests

---

## 🧰 Tech Stack

**Frontend**: React (TypeScript), Tailwind CSS, Axios, Chart.js  
**Backend**: FastAPI, SQLAlchemy (async), Pydantic, bcrypt, JWT  
**Database**: PostgreSQL  
**DevOps**: Docker, Docker Compose, GitHub Actions  
**Testing & Linting**: Pytest, httpx, Ruff, Mypy, Bandit

---

## 🚀 Getting Started

1. Clone the repository

2. Create a `.env` file for the backend. You can start with the provided `.env.example`.

3. Build and run the entire stack using Docker Compose

   - This will automatically initialize the database
   - Backend will run on port 8000
   - Frontend (Vite dev server) will run on port 3000

4. Access the application:
   - Frontend: `http://localhost:3000`
   - Backend API docs: `http://localhost:8000/docs`

---

## 📁 Project Structure

```
renewable-energy-visualizer/
├── backend/
│   ├── app/
│   ├── tests/
│   └── Dockerfile
├── frontend/
│   ├── src/
│   ├── public/
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## ✅ Environment Variables

The backend uses a `.env` file with variables like:

- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- SECRET_KEY
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES
- LOG_LEVEL
- SQLALCHEMY_ECHO

The frontend reads:

- VITE_API_URL

These are automatically used during Docker builds — no need to manually copy if Docker handles it internally.

---

## 📊 Energy Data Goals

The platform tracks:

- Energy **consumption** with timestamp, kWh, source, location
- Energy **generation** with source type (solar, wind)

Visualizations are done using Chart.js in the frontend.

---
