# backend/flask_app.py
from flask import Flask, request, jsonify
from scoring_engine import ScoringEngine
import os

app = Flask(__name__)
engine = ScoringEngine(rubric_path=os.path.abspath('/mnt/data/Case study for interns.xlsx'))

@app.route('/score', methods=['POST'])
def score():
data = request.get_json() or {}
text = data.get('text', '')
if not text:
return jsonify({'error': 'No text provided'}), 400
result = engine.score_transcript(text)
return jsonify(result)

if __name__ == '__main__':
app.run(host='0.0.0.0', port=8000, debug=True)
