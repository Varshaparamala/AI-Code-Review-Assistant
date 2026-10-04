import { useState } from "react";

const API_URL = "http://127.0.0.1:8000";

export default function App() {
  const [code, setCode] = useState(
    "def add(a, b):\n    print(a)\n    try:\n        return a + b\n    except:\n        pass"
  );
  const [issues, setIssues] = useState([]);
  const [aiFeedback, setAiFeedback] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function runReview(endpoint) {
    setLoading(true);
    setError("");
    setAiFeedback("");
    try {
      const res = await fetch(`${API_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, language: "python" }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Request failed");
      setIssues(data.issues || []);
      if (data.ai_feedback) setAiFeedback(data.ai_feedback);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: 24, textAlign: "left" }}>
      <h1>AI Code Review Assistant</h1>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        rows={14}
        style={{ width: "100%", fontFamily: "monospace", fontSize: 14, padding: 8 }}
      />
      <div style={{ marginTop: 12, display: "flex", gap: 8 }}>
        <button onClick={() => runReview("/review")} disabled={loading}>
          Run checks
        </button>
        <button onClick={() => runReview("/review-ai")} disabled={loading}>
          AI review
        </button>
      </div>

      {loading && <p>Reviewing...</p>}
      {error && <p style={{ color: "crimson" }}>Error: {error}</p>}

      {issues.length > 0 && (
        <>
          <h2>Issues ({issues.length})</h2>
          <ul>
            {issues.map((i, idx) => (
              <li key={idx}>
                <strong>Line {i.line}</strong> [{i.severity}] {i.message}
              </li>
            ))}
          </ul>
        </>
      )}

      {aiFeedback && (
        <>
          <h2>AI feedback</h2>
          <p style={{ whiteSpace: "pre-wrap" }}>{aiFeedback}</p>
        </>
      )}
    </div>
  );
}