# backend/fastapi_app.py
from fastapi import FastAPI
from pydantic import BaseModel
from scoring_engine import ScoringEngine
import os

app = FastAPI()
engine = ScoringEngine(rubric_path=os.path.abspath('/mnt/data/Case study for interns.xlsx'))

class Transcript(BaseModel):
text: str

@app.post('/score')
def score(payload: Transcript):
return engine.score_transcript(payload.text)

# To run: uvicorn backend.fastapi_app:app --reload --port 8000
