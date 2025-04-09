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

[![My Skills](https://skillicons.dev/icons?i=react,tailwind,py,fastapi,postgres,docker,githubactions)](https://skillicons.dev)

**Frontend**: React (TypeScript), Tailwind CSS, Axios, Chart.js  
**Backend**: FastAPI, SQLAlchemy (async), Pydantic, bcrypt, JWT  
**Database**: PostgreSQL  
**DevOps**: Docker, Docker Compose, GitHub Actions  
**Testing & Linting**: Pytest, httpx, Ruff, Mypy, Bandit [![Ruff Lint](https://github.com/bakliwalvaibhav1/renewable-energy-visualizer/actions/workflows/lint.yml/badge.svg)](https://github.com/bakliwalvaibhav1/renewable-energy-visualizer/actions/workflows/lint.yml)

---

## 🚀 Getting Started
### Prerequisite
Docker should be installed on the system. (Check with the command - `docker --version`)

### Clone the repository
```bash
git clone https://github.com/bakliwalvaibhav1/renewable-energy-visualizer.git
```

### Change the directory
```bash
cd renewable-energy-visualizer
```

### Build and run the entire stack using Docker Compose
```bash
docker-compose up --build
```

### Access the application:
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
