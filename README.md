# 🏦 Personal Finance Coach

A privacy-first personal finance coaching application that helps users understand their financial health, organizes money into smart buckets, and generates personalized action plans.

## 🚀 Features

- **Smart Financial Analysis**: Automatic calculation of net worth, savings rate, debt ratios
- **Bucket-Based Organization**: Emergency, Debt, Short-term, Long-term wealth buckets
- **Personalized Plans**: Top 3 priority actions with monthly targets
- **Progress Tracking**: Self-reported monthly check-ins with trend analysis
- **Explainable AI**: RAG-powered Q&A with cited sources (LangChain + LangGraph)
- **Privacy-First**: Self-reported data, no bank access required

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python)
- **Backend**: FastAPI
- **Database**: SQLite (local) → PostgreSQL (production)
- **ORM**: SQLAlchemy
- **AI/ML**: LangChain, LangGraph, HuggingFace, OpenRouter
- **Vector DB**: ChromaDB

## 📋 Prerequisites

- Python 3.10+
- pip or uv package manager

## 🔧 Setup Instructions

### 1. Clone and Setup Environment

```bash
cd C:\react\00p\project-x

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy example env file
copy .env.example .env

# Edit .env and add your API keys
# - OPENROUTER_API_KEY
# - HUGGINGFACE_API_KEY
# - JWT_SECRET_KEY
```

### 3. Initialize Database

```bash
cd backend

# Run migrations
alembic upgrade head
```

### 4. Start Backend Server

```bash
# From backend directory
uvicorn main:app --reload --port 8000
```

### 5. Start Frontend (Streamlit)

```bash
# From project root, new terminal
streamlit run frontend/app.py
```

### 6. Access Application

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📁 Project Structure

```
project-x/
├── backend/
│   ├── models/          # SQLAlchemy models
│   ├── api/             # FastAPI routes
│   ├── engine/          # Financial calculation & rule engine
│   ├── rag/             # LangChain RAG system
│   ├── services/        # Notifications, email
│   ├── utils/           # Security, helpers
│   ├── alembic/         # Database migrations
│   └── main.py          # FastAPI app entry
├── frontend/
│   ├── pages/           # Streamlit pages
│   ├── utils/           # API client, charts
│   └── app.py           # Streamlit entry
├── docs/                # Documentation
├── tests/               # Test suite
└── requirements.txt     # Python dependencies
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_calculator.py -v
```

## 🔄 Database Migration (SQLite → PostgreSQL)

To switch from SQLite to PostgreSQL:

1. Update `.env`:
   ```ini
   ENV=production
   DATABASE_URL=postgresql://user:pass@host:5432/finance_coach
   ```

2. Run migrations:
   ```bash
   alembic upgrade head
   ```

No code changes needed! SQLAlchemy handles both databases seamlessly.

## 📚 Key Documentation

- [High-Level Design](docs/HLD.md)
- [Database Schema](docs/database-schema.md)
- [API Contracts](docs/api-contracts.md)
- [Implementation Plan](docs/detailed-plan.md)

## 🔐 Security Notes

- All passwords hashed with bcrypt
- JWT tokens for authentication
- PII encrypted at rest
- No direct bank access (privacy-first)
- Deterministic rules (versioned & auditable)

## 📈 Development Workflow

Following the [Agentic Workflow](agent/AGENTIC_WORKFLOW.md):

1. **Plan** - Design before coding
2. **Implement** - Incremental changes
3. **Verify** - Test every change
4. **Loop** - Iterate based on feedback

## 🎯 MVP Roadmap

- [x] Project setup
- [ ] Database layer
- [ ] Authentication
- [ ] Financial analysis engine
- [ ] API endpoints
- [ ] RAG system
- [ ] Streamlit frontend
- [ ] Notification system
- [ ] Testing & deployment

## 📄 License

MIT

## 🤝 Contributing

Please read the [Agentic Workflow](agent/AGENTIC_WORKFLOW.md) before contributing.
