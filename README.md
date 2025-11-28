# AURORA-2 Demo

Демо на концептуалната архитектура AURORA-2 (KRE + OmniSphere + AURELIA).

## Цел
Професионално демо, което визуализира работата на AURORA-2 и може да бъде хостнато публично.

## Локално стартиране
1. Клонирай репото
2. Backend:
   - cd backend
   - python -m venv venv && source venv/bin/activate
   - pip install -r requirements.txt
   - uvicorn app.main:app --reload --port 8000
3. Frontend:
   - cd frontend
   - npm install
   - npm run dev
4. Отвори http://localhost:3000

## Деплой
- Backend: Render.com / DigitalOcean App / Docker image
- Frontend: Vercel (Next.js)
