# Universal AI Layer v4.0

## Autonomous Intelligence Memory Platform for Engineering Teams

Universal AI Layer is a high-performance, distributed, and explainable memory platform designed to give AI agents long-term context about complex software projects. It combines semantic vector search, keyword precision, and graph-based relationship mapping into a single, unified "Triple-Hybrid" search engine.

### 🚀 Key Features

*   **Triple-Hybrid Search:** Semantic (Vector) + Precision (Keyword) + Context (Graph - Apache Age).
*   **Deep Code Intelligence:** AST-aware ingestion using `tree-sitter` to map code logic and dependencies.
*   **Autonomous Scalability:** Distributed background workers (Celery + Redis) for heavy processing tasks.
*   **Explainable AI (XAI):** Full transparency with score breakdowns and source citations for every memory.
*   **Proactive Watchdogs:** Real-time Slack/Discord alerts for architectural deviations and conflicts.
*   **Enterprise Ready:** Multi-tenancy with Postgres Row-Level Security (RLS) and semantic caching.
*   **Hybrid Privacy:** Support for both OpenAI and local LLMs (Ollama) for sensitive projects.
*   **Visual Workspace:** Interactive React dashboard for memory constellation visualization and conflict resolution.

### 🛠️ Architecture

*   **Backend:** FastAPI (Python 3.13)
*   **Database:** PostgreSQL with `pgvector` and `Apache Age` (Graph)
*   **Async Processing:** Celery + Redis
*   **Frontend:** React + Vite + Tailwind CSS + react-force-graph
*   **AI Orchestration:** OpenAI API / Ollama (Local)

### 🚦 Quick Start

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/universal-ai-layer.git
    cd universal-ai-layer
    ```

2.  **Set Environment Variables:**
    Copy `.env.example` to `.env` and fill in your keys.
    ```bash
    cp .env.example .env
    ```

3.  **Launch Infrastructure:**
    ```bash
    docker-compose up -d
    ```

4.  **Start API:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # or .\venv\Scripts\activate on Windows
    pip install -r requirements.txt
    python src/main.py
    ```

5.  **Run Dashboard:**
    ```bash
    cd dashboard
    npm install
    npm run dev
    ```

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### 📄 License

MIT License - Created by **NishantJLU**
