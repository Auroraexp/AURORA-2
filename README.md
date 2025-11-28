# AURORA-2 MVP

Minimal working MVP for AURORA-2 (demo). Backend: FastAPI; Frontend: Next.js.

## Repo structure
```
aurora2/
├── backend/
│   ├── main.py
│   ├── aurora_solver.py
│   ├── models/
│   │   ├── kre.py
│   │   ├── os_model.py
│   │   └── aurelia.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── package.json
│   ├── pages/
│   │    └── index.js
│   └── public/
│
└── docs/
    ├── deploy.md
    └── api.md
```

## Quick start (local)
1. Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

2. Frontend:
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 (frontend) and backend at http://localhost:8000
