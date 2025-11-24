# Nirmaan-Case-Study

This project implements a rubric-based scoring system for evaluating students’ spoken communication (converted from audio → transcript). It follows all requirements given in the Nirmaan AI Intern Case Study.

**Project Overview**

This system takes a transcript text as input and produces:

a) Overall score (0–100)

b) Per-criterion scores

c) Keyword match analysis

d) Semantic similarity scores

e) Detailed feedback for each criterion

It combines:

i) Rule-based scoring — keywords, word count, structure

ii) NLP scoring — TF-IDF semantic similarity

iii) Rubric-based weighting — using extracted weights from the provided Excel file

**How Scoring Works**

a) Keyword Score (40%): Matches transcript text with rubric keywords.

b) Semantic Similarity (40%): TF-IDF-based cosine similarity between transcript and each criterion description.

c) Length Match (20%): Checks whether transcript meets min/max word expectations (if available).

d) Weighted Rubric Score: Each criterion has a weight extracted from the Excel rubric.

Final score is normalized to 0–100.

**Setup Instructions (Local)**

1️) Create virtual env + install requirements: python3 -m venv venv source venv/bin/activate pip install -r requirements.txt

2️)Run Backend (Flask): 
python backend/flask_app.py
This starts API on: http://localhost:8000/score

3️) Run Frontend (Streamlit UI): 
streamlit run frontend/streamlit_app.py

4️) Test Using cURL or Postman: 
curl -X POST http://localhost:8000/score
-H "Content-Type: application/json"
-d @tests/sample_input.json

Final normalized score

The tool includes both backend and frontend code, a scoring engine, rubric parser, and deployment notes.
