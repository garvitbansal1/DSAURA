# DSAURA — Intelligent DSA Learning & Knowledge Assessment Platform

> *"Solving more problems does not necessarily mean learning more. DSAURA measures demonstrated problem-solving development, not just problem counts."*

DSAURA is an intelligent, full-stack platform that connects a user's coding profiles (LeetCode, Codeforces, GeeksforGeeks, HackerRank), analyzes their DSA problem-solving history, detects true algorithmic blind spots, estimates topic-wise mastery using explainable evidence algorithms, and schedules active recall practice using the SuperMemo SM-2 algorithm.

---

## 🌟 Key Architecture & Capabilities

1. **Evidence-Based Mastery Engine (Phase 6)**:
   Calculates mastery across **5 distinct dimensions** (not raw problem count):
   - **Pattern Coverage (30%)**: How many patterns in a topic have been demonstrated.
   - **Independent Solving (25%)**: Solved independently vs. with editorial/hints.
   - **Difficulty Progression (20%)**: Progression from Easy to Medium and Hard.
   - **Problem Diversity (15%)**: Breadth within the topic space.
   - **Revision Retention (10%)**: Performance and recall retention on spaced repetitions.
   - *Guard*: Topics with fewer than 3 problems are flagged with *"Insufficient Evidence"*.

2. **Knowledge Reality Check & Gap Detection (Phases 7 & 12)**:
   - Detects the **"Illusion of Competence"** — when a user has solved 100+ problems but repeats the same 2 easy patterns (e.g. basic hash maps).
   - Identifies missing patterns and prerequisite gaps (e.g. *0/1 Knapsack*, *Monotonic Stack*, *Binary Search on Answer*).

3. **Interactive Knowledge Graph (Phase 8)**:
   - **React Flow** DAG rendering **48 nodes** (Topic Hubs + Pattern Nodes) and **20 directed prerequisite relations** with interactive node inspector.

4. **Algorithmic Pattern Library (Phases 4 & 11)**:
   - 28 topics and 20 seeded patterns with:
     - Multi-language implementation templates (**Python** and **Java**).
     - **When to Use** & **Recognition Clues**.
     - Time & Space Complexity analysis.
     - Curated related practice problems.

5. **Spaced Repetition System (Phase 13)**:
   - Implements **SuperMemo SM-2** spaced repetition.
   - Tracks ease factors, repetition counts, and due dates across *Due Today*, *Overdue*, and *Upcoming* queues.
   - Interactive review with 4 recall rating buttons: *Again (0)*, *Hard (3)*, *Good (4)*, *Easy (5)*.

6. **Cross-Platform Intelligence & Deduplication (Phase 15)**:
   - Normalizes problem titles and aliases (e.g. LeetCode "Two Sum" vs. GFG "Key Pair").
   - Filters duplicate submissions to report true deduplicated problem volume.
   - Calculates cross-platform learning synergy (LeetCode pattern grounding + Codeforces speed & contest resilience).

7. **Pattern Recognition Assessment (Phase 10)**:
   - Scenario-based algorithmic quiz testing pattern diagnosis skills before writing code.
   - Explains complex edge cases (e.g. why negative weights break sliding window monotonicity).

---

## 🚀 Technology Stack

### Frontend
- **Framework**: React 19 + TypeScript (Vite)
- **Styling**: Tailwind CSS v3 (Custom Dark Palette: `#0f0f1a` background, `#1a1a2e` surfaces, `#6272f1` brand accent)
- **State Management**: Zustand v5 with local storage persistence
- **Visualizations**: Recharts (Pie/Donut difficulty charts, Topic horizontal bar charts, 12-week progression curve)
- **Graph Engine**: React Flow (Interactive DAG with custom topic/pattern nodes)
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI (Modular Routers)
- **Language**: Python 3.12
- **Database**: PostgreSQL 18.7 + SQLAlchemy 2.1 ORM
- **Authentication**: JWT Bearer Tokens + Direct Bcrypt Password Hashing (safely handles 72-byte boundary)
- **Validation**: Pydantic v2 + Pydantic-Settings + Email-Validator
- **Integrations**: LeetCode GraphQL API, Codeforces REST API, GFG CSV Fallback, HackerRank

---

## 🛠️ Running the Application Locally

### Prerequisites
- **PostgreSQL** running on port `5432` with database `dsaura`
- **Node.js** v20+ / v26+
- **Python** 3.12+

### 1. Database Setup
```powershell
# Create user and database
psql -U postgres -c "CREATE USER dsaura WITH PASSWORD 'dsaura_dev';"
psql -U postgres -c "CREATE DATABASE dsaura OWNER dsaura;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE dsaura TO dsaura;"
```

### 2. Backend Setup & Startup
```powershell
cd backend
# Create virtual environment & install dependencies
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt

# Seed taxonomy, patterns, and curated problems
$env:PYTHONPATH = "."
.\venv\Scripts\python -m app.knowledge_base.seed_data

# Start FastAPI API server
.\venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000
```
- API Docs: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- Health Check: [http://localhost:8000/api/health](http://localhost:8000/api/health)

### 3. Frontend Setup & Startup
```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```
- Web Application: [http://localhost:5173](http://localhost:5173)

---

## 🧪 Pre-Registered Account
You can immediately log in on [http://localhost:5173/login](http://localhost:5173/login) using:
- **Email:** `test@dsaura.dev`
- **Password:** `Password123!`

---

## 🔬 Test Suite Execution

Run the complete backend test suite using Pytest:
```powershell
cd backend
$env:PYTHONPATH = "."
.\venv\Scripts\pytest -v
```
All **14 automated tests** pass covering:
- Direct bcrypt password hashing & 72-byte safe boundary
- JWT encode, decode, and expiration
- Title normalization & cross-platform deduplication
- Mastery engine 5-dimension scoring & insufficient evidence guard
- SuperMemo SM-2 interval calculations & ease factor floors
