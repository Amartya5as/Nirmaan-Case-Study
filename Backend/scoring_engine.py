# backend/scoring_engine.py
def _keyword_score(self, text: str, keywords: List[str]) -> float:
text_low = text.lower()
if not keywords:
return 0.0
found = sum(1 for k in keywords if k in text_low)
return found / len(keywords)

def score_transcript(self, text: str) -> Dict[str, Any]:
words = re.findall(r"\w+", text)
word_count = len(words)
criteria_out = []
total_weighted = 0.0
for i, c in enumerate(self.rubric):
kw_score = self._keyword_score(text, c.get('keywords', []))
sem_score = self._semantic_similarity(text, i)
length_score = 1.0
if c.get('min_words') and word_count < c['min_words']:
length_score = 0.0
if c.get('max_words') and word_count > c['max_words']:
length_score = 0.0
combined = 0.4 * kw_score + 0.4 * sem_score + 0.2 * length_score
# normalized to 0-100
score_0_100 = combined * 100
weighted = score_0_100 * (c.get('norm_weight', 0) / 100.0)
total_weighted += weighted
criteria_out.append({
'name': c['name'],
'score': round(score_0_100, 2),
'semantic_similarity': round(sem_score, 3),
'keywords_found': [k for k in c.get('keywords', []) if k in text.lower()],
'feedback': self._generate_feedback(kw_score, sem_score, length_score)
})
overall = round(total_weighted, 2)
return {'overall_score': overall, 'word_count': word_count, 'criteria': criteria_out}

def _generate_feedback(self, kw, sem, length):
messages = []
if kw < 0.3:
messages.append('Few rubric keywords detected.')
else:
messages.append('Good keyword coverage.')
if sem < 0.3:
messages.append('Low semantic match — consider aligning content to rubric descriptions.')
else:
messages.append('Content aligns well with rubric intent.')
if not length:
messages.append('Length does not meet rubric suggested limits.')
return ' '.join(messages)

# A thin CLI wrapper for node usage
if __name__ == '__main__':
import sys
data = json.load(sys.stdin)
text = data.get('text', '')
engine = ScoringEngine(rubric_path='/mnt/data/Case study for interns.xlsx')
print(json.dumps(engine.score_transcript(text)))
