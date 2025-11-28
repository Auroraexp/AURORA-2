from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from aurora_solver import aurora2_solve

app = FastAPI(title="AURORA-2 API")

class AuroraInput(BaseModel):
    kre: float
    os: float
    aurelia: float
    modifiers: dict = {}

@app.get("/")
def root():
    return {"message": "AURORA-2 API running"}

@app.post("/solve")
def solve_aurora2(data: AuroraInput):
    try:
        output = aurora2_solve(
            kre=data.kre,
            os=data.os,
            aurelia=data.aurelia,
            modifiers=data.modifiers
        )
        return {"AURORA2_output": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
