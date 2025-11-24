// backend/node_app/index.js
const express = require('express');
const bodyParser = require('body-parser');
const { spawnSync } = require('child_process');
const app = express();
app.use(bodyParser.json());

// This Node server delegates scoring to the Python script scoring_engine.py via stdin/file.
app.post('/score', (req, res) => {
const text = req.body.text || '';
if (!text) return res.status(400).json({ error: 'No text provided' });

// We call python3 scoring script and pass text via JSON stdin.
const proc = spawnSync('python3', ['-u', 'backend/scoring_engine_cli.py'], {
input: JSON.stringify({ text }),
encoding: 'utf-8',
maxBuffer: 10 * 1024 * 1024
});

if (proc.error) return res.status(500).json({ error: proc.error.message });
try {
const out = JSON.parse(proc.stdout);
res.json(out);
} catch (e) {
res.status(500).json({ error: 'Invalid response from scoring script', detail: proc.stdout });
}
});

const PORT = process.env.PORT || 8000;
app.listen(PORT, () => console.log(`Node server running on ${PORT}`));
