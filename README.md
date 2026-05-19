Universal AI Layer v4.0
Autonomous Intelligence Memory Platform for Engineering Teams
What it is
A high-performance, distributed memory platform that gives AI agents long-term context about complex software projects. It combines three search strategies — semantic vector search, keyword precision, and graph-based relationship mapping — into a unified "Triple-Hybrid" engine.

Key Features

Triple-Hybrid Search — Combines semantic (vector), precision (keyword), and context (graph via Apache Age) search in one engine.
Deep Code Intelligence — Uses tree-sitter for AST-aware ingestion to map code logic and dependencies.
Autonomous Scalability — Distributed background workers via Celery + Redis for heavy processing.
Explainable AI (XAI) — Every memory result comes with score breakdowns and source citations.
Proactive Watchdogs — Real-time Slack/Discord alerts for architectural deviations and conflicts.
Enterprise Ready — Multi-tenancy with PostgreSQL Row-Level Security (RLS) and semantic caching.
Hybrid Privacy — Supports both OpenAI API and local LLMs (Ollama) for sensitive projects.
Visual Dashboard — Interactive React UI for memory constellation visualization and conflict resolution.


Tech Stack
LayerTechnologyBackendFastAPI (Python 3.13)DatabasePostgreSQL + pgvector + Apache Age (Graph)Async ProcessingCelery + RedisFrontendReact + Vite + Tailwind CSS + react-force-graphAIOpenAI API / Ollama (local)

Quick Start
bash# 1. Clone
git clone https://github.com/YOUR_USERNAME/universal-ai-layer.git
cd universal-ai-layer

# 2. Set env vars
cp .env.example .env   # fill in your keys

# 3. Launch infrastructure
docker-compose up -d

# 4. Start API
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py

# 5. Run dashboard
cd dashboard && npm install && npm run dev

Project Structure
├── src/           # Python backend (FastAPI)
├── dashboard/     # React frontend
├── tests/         # Test suite
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
License: MIT — Created by NishantJLU
Contributions: Pull requests welcome.
