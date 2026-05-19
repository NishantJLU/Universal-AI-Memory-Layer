# 🌌 Universal AI Layer v4.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005850?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

**Universal AI Layer** is an autonomous intelligence memory platform designed for high-performance engineering teams. It provides AI agents with deep, long-term context about complex software ecosystems by unifying semantic depth, keyword precision, and architectural relationships.

---

## 🚀 The Triple-Hybrid Engine
Unlike traditional vector databases, v4.0 introduces the **Triple-Hybrid Search** strategy, ensuring that AI agents never lose the "forest for the trees."

1.  **Semantic Depth:** Leverages `pgvector` for high-dimensional embedding similarity.
2.  **Keyword Precision:** Utilizes PostgreSQL `tsvector` for exact match and BM25-grade keyword recall.
3.  **Graph Context:** Powered by **Apache Age**, mapping complex code dependencies and architectural relationships into a queryable knowledge graph.

---

## ✨ Key Features

- **🧠 Deep Code Intelligence:** AST-aware ingestion via `tree-sitter` to map logic, not just text.
- **⚙️ Autonomous Scalability:** Distributed background processing with **Celery + Redis** for massive codebase ingestion.
- **🔍 Explainable AI (XAI):** Transparent score breakdowns and source citations for every recalled memory.
- **🛡️ Proactive Watchdogs:** Real-time Slack/Discord alerts for architectural deviations or conflicting decisions.
- **🏢 Enterprise Ready:** Multi-tenancy with **PostgreSQL Row-Level Security (RLS)** and high-speed semantic caching.
- **🔒 Hybrid Privacy:** Toggle between OpenAI for speed and **Ollama** for air-gapped, local-first security.
- **📊 Visual Dashboard:** Interactive React UI featuring a **Memory Constellation** visualization and conflict resolution suite.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI (Python 3.13), SQLAlchemy (Async) |
| **Database** | PostgreSQL, `pgvector`, Apache Age (Graph) |
| **Task Queue** | Celery, Redis |
| **Frontend** | React, Vite, Tailwind CSS, `react-force-graph` |
| **Ingestion** | `tree-sitter`, GitPython |

---

## 🏗️ Architecture
```mermaid
graph TD
    A[Repo/Commits] -->|Tree-Sitter AST| B(Ingestion Pipeline)
    B -->|Task Queue| C[Celery Workers]
    C -->|Vector + Keyword| D[(Postgres + pgvector)]
    C -->|Relationships| E[(Apache Age Graph)]
    F[AI Agent] -->|MCP/REST| G(Recall Engine)
    G -->|Triple-Hybrid Search| D
    G -->|Graph Walk| E
    G -->|Contextual Response| F
```

---

## 🏁 Quick Start

### 1. Clone & Prepare
```bash
git clone https://github.com/NishantJLU/Universal-AI-Layer.git
cd Universal-AI-Layer
cp .env.example .env   # Configure your API keys and providers
```

### 2. Launch Infrastructure
Spin up the database, Redis, and Graph extensions:
```bash
docker-compose up -d
```

### 3. Initialize Backend
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

### 4. Launch Visual Dashboard
```bash
cd dashboard
npm install
npm run dev
```

---

## 📂 Project Structure
```text
├── src/           # FastAPI Backend (Recall, Ingest, Providers)
├── dashboard/     # React + Vite Frontend (Visualization, Management)
├── tests/         # Comprehensive Async Test Suite
├── Dockerfile     # Optimized multi-stage build
├── requirements.txt
└── .env.example
```

---

## 🤝 Contributing
We welcome contributions that push the boundaries of AI memory. Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## 📄 License
MIT License — Created by **NishantJLU**
