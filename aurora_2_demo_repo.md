# AURORA-2 — Demo repo (пълен код и инструкции)

Този документ съдържа цялостна, готова за клониране структура на репо за публично, професионално демо на AURORA-2. Включени са: backend (FastAPI), фронтенд (Next.js + React + Tailwind), модули KRE/OmniSphere/AURELIA, Docker/Render/Vercel инструкции и помощни файлове. Копирай файловете в съответните папки и следвай инструкциите за пускане и деплой.

---

## 1) Препоръчана структура на репото
```
AURORA-2-demo/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ kre.py
│  │  ├─ os_module.py
│  │  ├─ aurelia.py
│  │  └─ model.py
│  ├─ requirements.txt
│  └─ Dockerfile
├─ frontend/
│  ├─ package.json
│  ├─ next.config.js
│  ├─ tailwind.config.js
│  ├─ postcss.config.js
│  └─ pages/
│     ├─ index.js
│     └─ api/health.js
├─ README.md
└─ .github/workflows/deploy-backend.yml
```

---

# 2) Backend — FastAPI (файлове)

### backend/app/kre.py
```python
# kre.py
import math

def KRE_module(x, w_K=0.28278):
    """Опрощена версия на KRE: генерира предложение от текущото състояние x.
    В реалния проект замени тази функция с твоя FKRE динамика/интеграл.
    """
    # x може да е число или вектор; тук използваме скаларен пример
    base = float(x)
    # динамичен генератор (пример): нелинейна трансформация
    proposal = base + w_K * (0.5 * base + math.sin(base) * 0.1)
    return proposal
```

### backend/app/os_module.py
```python
# os_module.py
import math

def OS_module(context_vector, w_OS=0.17866):
    """OmniSphere корекция: приема контекст (словар/вектор) и връща корекционен скалар.
    Тук контекст_vector е словар с полета Au,Ag,mineral,FeCu,ID (или числов индикатор).
    """
    # Опростен пример: сума на стандартни фактори
    Au = float(context_vector.get('Au', 1.0))
    Ag = float(context_vector.get('Ag', 1.0))
    mineral = float(context_vector.get('mineral', 1.0))
    fe_cu = float(context_vector.get('fe_cu', 1.0))
    uid = float(context_vector.get('uid', 1.0))

    raw = Au + Ag + mineral + fe_cu + uid
    corr = w_OS * (raw / 5.0)  # нормализирано
    return corr
```

### backend/app/aurelia.py
```python
# aurelia.py

def NIM(I=1.0, E=1.0, C=1.0, A=1.0, S=1.0, eps=0.1):
    # опростена информационно-аналитична функция
    return (I + E + C + A + S) / 5.0


def NOVEMBER(deltaC=1.0, Hs=0.5, El=0.3, Psir=0.8, Tn=1.0, Lam=1.0):
    # опростена оценка на въздействие
    return deltaC * (Hs + El) * Psir * (Tn ** 1.0) * Lam


def AURELIA_module(context, w_A=0.26789, eta=0.27, alpha=0.574, beta=0.426):
    # context е словар с нужните полета
    nim = NIM(
        I=context.get('I',1.0), E=context.get('E',1.0), C=context.get('C',1.0),
        A=context.get('A',1.0), S=context.get('S',1.0), eps=context.get('eps',0.1)
    )
    november = NOVEMBER(
        deltaC=context.get('deltaC',1.0), Hs=context.get('Hs',0.5), El=context.get('El',0.3),
        Psir=context.get('Psir',0.8), Tn=context.get('Tn',1.0), Lam=context.get('Lam',1.0)
    )
    val = eta * (alpha * nim + beta * november)
    # return normalized vector/scale
    return w_A * val
```

### backend/app/model.py
```python
# model.py
from .kre import KRE_module
from .os_module import OS_module
from .aurelia import AURELIA_module

# тежести — използваме твоите числови примери
WEIGHTS = {
    'w_K': 0.28278,
    'w_OS': 0.17866,
    'w_A': 0.26789,
    'w_G': 0.27067
}


def aurora_step(x0, context, params=None):
    """Една итерация/стъпка на AURORA-2: връща X_final и подробности."""
    if params is None:
        params = {}

    # 1) KRE
    x_cand = KRE_module(x0, w_K=WEIGHTS['w_K'])

    # 2) RESTART (опростено: малка итеративна корекция)
    # тук използваме фиксиран му и градиент-грубо
    mu = params.get('mu', 0.1)
    grad_est = 0.05 * x_cand
    x_raw = x_cand - mu * grad_est

    # 3) OmniSphere
    s_corr = OS_module(context, w_OS=WEIGHTS['w_OS'])
    x_corr = x_raw + s_corr

    # 4) AURELIA оценка
    a_val = AURELIA_module(context, w_A=WEIGHTS['w_A'])

    # 5) Етичен градиент (approx)
    grad_Leth = params.get('grad_Leth', 0.5)

    # 6) Комбинация и проекция (за простота: проекция = идентичност)
    v = x_corr + a_val - params.get('eta', 0.27) * grad_Leth
    x_final = v

    return {
        'X_final': x_final,
        'trace': {
            'x_cand': x_cand,
            'x_raw': x_raw,
            's_corr': s_corr,
            'a_val': a_val,
            'v': v
        }
    }
```

### backend/app/main.py
```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .model import aurora_step

app = FastAPI(title='AURORA-2 API')

# CORS за локален frontend/хост
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuroraInput(BaseModel):
    x0: float
    context: dict = {}
    params: dict = {}

@app.post('/aurora')
async def aurora_endpoint(inp: AuroraInput):
    res = aurora_step(inp.x0, inp.context, inp.params)
    return res

@app.get('/health')
async def health():
    return {"status":"ok"}
```

### backend/requirements.txt
```text
fastapi
uvicorn[standard]
pydantic
```

### backend/Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY ./app /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# 3) Frontend — Next.js + Tailwind (файлове)

### frontend/package.json
```json
{
  "name": "aurora-2-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "13.4.4",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "axios": "1.4.0"
  },
  "devDependencies": {
    "autoprefixer": "10.4.14",
    "postcss": "8.4.24",
    "tailwindcss": "3.4.12"
  }
}
```

### frontend/tailwind.config.js
```js
module.exports = {
  content: ['./pages/**/*.{js,jsx}', './components/**/*.{js,jsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### frontend/postcss.config.js
```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### frontend/pages/index.js
```jsx
import { useState } from 'react'
import axios from 'axios'

export default function Home() {
  const [x0, setX0] = useState(10)
  const [contextJson, setContextJson] = useState(JSON.stringify({I:5,E:3,C:2,A:1,S:4,eps:0.1,deltaC:1.5,Hs:0.5,El:0.3,Psir:0.8,Tn:2,Lam:1.2},null,2))
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'

  const runAurora = async () => {
    setLoading(true)
    try {
      const ctx = JSON.parse(contextJson)
      const resp = await axios.post(`${API_URL}/aurora`, { x0: parseFloat(x0), context: ctx, params: {} })
      setResult(resp.data)
    } catch (e) {
      alert('Грешка: ' + (e.message || e))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded shadow">
        <h1 className="text-2xl font-semibold mb-4">AURORA-2 Demo</h1>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium">Начално състояние x0</label>
            <input value={x0} onChange={e=>setX0(e.target.value)} className="mt-1 block w-full border p-2 rounded" />

            <label className="block text-sm font-medium mt-4">Контекст (JSON)</label>
            <textarea rows={12} value={contextJson} onChange={e=>setContextJson(e.target.value)} className="mt-1 block w-full border p-2 rounded font-mono text-sm"></textarea>

            <button onClick={runAurora} className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded" disabled={loading}>{loading? 'Running...':'Run AURORA'}</button>
          </div>

          <div>
            <h2 className="text-lg font-medium">Резултат</h2>
            <pre className="mt-2 bg-gray-100 p-3 rounded text-sm">{result? JSON.stringify(result, null, 2) : 'Няма резултат още'}</pre>

            <div className="mt-4">
              <h3 className="font-medium">Инфографика (символична)</h3>
              <div className="mt-2 p-3 bg-white border rounded">
                <p>KRE — логика (силата е конфигурируема)</p>
                <p>OmniSphere — идентичност</p>
                <p>AURELIA — етика и оценка на риск</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
```

### frontend/pages/api/health.js
```js
export default function handler(req, res) {
  res.status(200).json({status: 'ok'})
}
```

### frontend/next.config.js
```js
module.exports = {
  reactStrictMode: true,
}
```

---

# 4) README.md (главен за репото)
```markdown
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

## Бележки
- Демото е минимално, но показва цялостен pipeline и лесно се разширява.
```

---

# 5) CI / workflow за автоматичен деплой (пример за backend на Render или Docker registry)

Файл: .github/workflows/deploy-backend.yml
```yaml
name: Build and Push Backend

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Build and push Docker image
      run: |
        docker build -t ${{ github.repository_owner }}/aurora-backend:latest ./backend
        echo "Docker image built. Push to your registry or deploy manually."
```

---

# 6) Инструкции за публикуване като доказателство (presentation checklist)
1. Подготви README с кратко резюме, архитектурна диаграма и видео (екранна запис) на системата, работеща локално.  
2. Публикувай кода в публично GitHub репо (master/main).  
3. Деплой фронтенд на Vercel (с NEXT_PUBLIC_BACKEND_URL = https://... на твоя backend).  
4. Деплой backend на Render (или друг хост) и свържи CORS.  
5. Създай GitHub release и wiki с инструкции.  
6. Подготви демо видео 2–5 мин. (запис как пускаш вход и показваш резултатите).  
7. Документ за проверка: кратко technical note (формули и съответствие с AURORA-2 документа).  

---

# 7) Правни и етични бележки
- В README добави секция "Ethical notice" с обяснение, че демото е прототип, не контролира физически системи, и че решенията са концептуални.  
- Ако планираш публичен достъп, добави rate-limiting и input validation.

---

# 8) Следващи стъпки от моя страна (мога да направя веднага)
- Генерирам ZIP с всички файлове за директно изтегляне. (мога да създам файловете тук и да ти дам копия)
- Създам готов `README.md` и `ARCHITECTURE.md` с диаграми.
- Подготвя примерна страница в Vercel/Render deployment guide стъпка по стъпка.

Казвай коя от опциите искаш да стартирам първо — аз ще генерирам файловете (code blocks горе) като реални файлове, готови за качване в GitHub. 

