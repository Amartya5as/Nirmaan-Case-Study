import React, { useState } from "react";

export default function App() {
  const [text, setText] = useState("");
  const [api, setApi] = useState("http://localhost:8000/score");
  const [result, setResult] = useState(null);

  async function score() {
    const res = await fetch(api, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const json = await res.json();
    setResult(json);
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Nirmaan AI – Transcript Scoring</h1>

      <textarea
        rows={10}
        cols={80}
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <div style={{ marginTop: 10 }}>
        <input
          style={{ width: "60%" }}
          value={api}
          onChange={(e) => setApi(e.target.value)}
        />
        <button onClick={score} style={{ marginLeft: 10 }}>
          Score
        </button>
      </div>

      {result && (
        <div style={{ marginTop: 20 }}>
          <h2>Overall Score: {result.overall_score}</h2>
          <p>Word Count: {result.word_count}</p>

          {result.criteria.map((c) => (
            <div key={c.name} style={{ marginTop: 10, borderTop: "1px solid #ccc", paddingTop: 10 }}>
              <h3>{c.name}</h3>
              <p>Score: {c.score}</p>
              <p>Semantic Similarity: {c.semantic_similarity}</p>
              <p>Keywords Found: {JSON.stringify(c.keywords_found)}</p>
              <p>Feedback: {c.feedback}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
