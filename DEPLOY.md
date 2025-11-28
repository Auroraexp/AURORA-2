# DEPLOY GUIDE

## Overview
This guide shows how to deploy frontend to Vercel and backend to Render (or any Docker host).

### Backend (Render / Docker)
1. Build Docker image: docker build -t aurora-backend:latest ./backend
2. Push to registry (Docker Hub / GitHub Container Registry)
3. Create Render service (Docker) or deploy to any cloud provider
4. Ensure port 8000 is exposed and CORS allows your frontend origin

### Frontend (Vercel)
1. Connect your GitHub repo to Vercel
2. Set NEXT_PUBLIC_BACKEND_URL environment variable to your backend URL
3. Deploy

### Environment variables
- NEXT_PUBLIC_BACKEND_URL=https://your-backend.example.com

## Security & Ethics
- Add rate limiting on backend
- Validate and sanitize inputs
- Add an "Ethical notice" in the UI
