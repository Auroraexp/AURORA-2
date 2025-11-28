# Deploy guide

## Backend (Render)
1. Create a free Render account.
2. New -> Web Service -> Connect GitHub repository -> select `backend` folder.
3. Set the start command: `uvicorn main:app --host 0.0.0.0 --port 8000`.
4. Set environment (Python 3.10) and deploy.

## Frontend (Vercel)
1. Create a free Vercel account.
2. Import project -> choose `frontend` folder.
3. Set environment variable `AURORA_BACKEND_URL` to the Render backend URL.
4. Deploy. Frontend will be live on `*.vercel.app`.

## Local run
Follow README.md quick start section.
