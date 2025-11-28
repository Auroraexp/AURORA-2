# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .model import aurora_step

app = FastAPI(title='AURORA-2 API')

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
