# scripts/parse_rubric.py
import pandas as pd
import re
import json


def parse_rubric(path):
df = pd.read_excel(path, sheet_name='Rubrics', header=None)
# heuristics tuned for your file structure
rows = df.fillna('').astype(str)
parsed = []
for i in range(len(rows)):
line = ' | '.join(rows.iloc[i].tolist()).strip()
if any(k in line.lower() for k in ['content', 'fluency', 'grammar', 'vocabulary', 'pronunciation', 'confidence']):
# try to extract numeric weight
m = re.search(r"(
