# 🚀 Deploy Web Application  
### FastAPI + Poetry + Docker + Render (Complete Guide)

---

## 📌 Overview

This guide walks you through deploying a **FastAPI web application** using:

- 🐍 Python 3.13  
- 📦 Poetry (dependency management)  
- 🐳 Docker (containerization)  
- ☁️ Render (cloud deployment)  
- 🔗 GitHub (code hosting)

---

## 🧱 Step 1: Project Structure

Make sure your project looks like this:

```
6_document_ai_app/
│
├── main.py
├── pyproject.toml
├── poetry.lock
├── Dockerfile
├── .dockerignore
└── README.md
```

---

## ⚙️ Step 2: Create `Dockerfile`

```dockerfile
# Use lightweight Python image
FROM python:3.13-slim

# Prevent Python from writing pyc files & enable logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=2.2.0
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy dependency files (for caching)
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy project files
COPY . .

# Set port (Render default)
ENV PORT=10000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
````

---

## 📦 Step 3: Create `.dockerignore`

```text
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.git
.gitignore
Dockerfile
node_modules/
```

---

## 🧪 Step 4: Sample `main.py` (FastAPI App)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, FastAPI on Render!"}

@app.get("/health")
def health():
    return {"status": "ok"}
```

---

## ▶️ Step 5: Run Locally (Optional Testing)

### Install dependencies

```bash
poetry install
```

### Run app

```bash
poetry run uvicorn main:app --reload
```

### Test in browser

```
http://127.0.0.1:8000/docs
```

---

## 🔄 Step 6: Push Code to GitHub

### Initialize repo

```bash
git init
git add .
git commit -m "Initial commit - FastAPI Docker app"
```

### Connect remote repo

```bash
git branch -M main
git remote add origin https://github.com/<username>/<repo-name>.git
git push -u origin main
```

---

## ☁️ Step 7: Deploy on Render

### Steps:

1. Go to: [https://render.com](https://render.com)
2. Sign up / Login
3. Click **New → Web Service**
4. Select **Build & Deploy from GitHub**
5. Connect your repository

---

## ⚙️ Step 8: Configure Render Service

| Setting        | Value                  |
| -------------- | ---------------------- |
| Environment    | Docker                 |
| Branch         | main                   |
| Region         | Singapore (or nearest) |
| Root Directory | (leave empty)          |
| Auto Deploy    | Yes                    |

---

## 🔑 Step 9: Environment Variables

Add:

```
PORT=10000
```

(Optional)

```
API_KEY=your_key
MODEL_PATH=/models
```

---

## 🚀 Step 10: Deploy

Click **Deploy Web Service**

Render will:

* Pull code from GitHub
* Build Docker image
* Install dependencies
* Start FastAPI server

---

## 🌐 Step 11: Access Your App

### Base URL

```
https://your-app-name.onrender.com
```

### API Docs

```
https://your-app-name.onrender.com/docs
```

### Health Check

```
https://your-app-name.onrender.com/health
```

---

## 🧠 Best Practices

### 1. Use Dynamic Port (Recommended)

Update Docker CMD:

```dockerfile
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
```

---

### 2. Add Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
```

---

### 3. Use `.env` File

Install:

```bash
poetry add python-dotenv
```

---

### 4. Requirements Optimization

```bash
poetry export -f requirements.txt --output requirements.txt
```

---

### 5. Add Health Check Endpoint

```python
@app.get("/health")
def health():
    return {"status": "running"}
```

---

## ⚠️ Common Issues & Fixes

| Issue             | Solution                |
| ----------------- | ----------------------- |
| Build fails       | Add `build-essential`   |
| App not starting  | Check `CMD`             |
| Port error        | Use `$PORT`             |
| Dependencies fail | Verify `pyproject.toml` |
| Slow build        | Use caching properly    |

---

## 🧩 Advanced Enhancements

### 🔐 Authentication

* JWT Token
* OAuth2

### 📦 CI/CD

* GitHub Actions
* Auto deploy on push

### 📊 Monitoring

* Prometheus
* Grafana

### 🧠 AI Integration

* YOLO (Object Detection)
* CLIP (Vision-Language)
* LLM APIs (OpenAI)

---

## 🎯 Final Summary

You now have:

* ✅ Dockerized FastAPI app
* ✅ Poetry-based dependency management
* ✅ GitHub integration
* ✅ Cloud deployment on Render
* ✅ Production-ready setup

---
