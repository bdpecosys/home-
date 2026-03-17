"use client";
import { useEffect, useState, useCallback } from "react";
import { fetchCompanies, addCompany, analyzeCompany, streamRecommendations, Company } from "@/lib/api";

function ScoreBar({ value, label }: { value: number; label: string }) {
  const pct = Math.round(value * 100);
  const color = pct >= 70 ? "#16a34a" : pct >= 40 ? "#d97706" : "#dc2626";
  return (
    <div style={{ marginBottom: 4 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, marginBottom: 2 }}>
        <span>{label}</span><span style={{ color }}>{pct}%</span>
      </div>
      <div style={{ background: "#e2e8f0", borderRadius: 4, height: 6 }}>
        <div style={{ width: `${pct}%`, background: color, height: 6, borderRadius: 4 }} />
      </div>
    </div>
  );
}

function CompanyCard({ company, onAnalyze }: { company: Company; onAnalyze: (id: string) => void }) {
  const [loading, setLoading] = useState(false);
  return (
    <div style={{ background: "#fff", borderRadius: 10, padding: 20, boxShadow: "0 1px 4px rgba(0,0,0,.08)", marginBottom: 16 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div>
          <h3 style={{ margin: "0 0 4px" }}>{company.name}</h3>
          <a href={`https://${company.domain}`} target="_blank" rel="noreferrer" style={{ color: "#6366f1", fontSize: 13 }}>{company.domain}</a>
          {company.industry && <span style={{ marginLeft: 8, fontSize: 12, background: "#e0e7ff", color: "#3730a3", borderRadius: 4, padding: "2px 8px" }}>{company.industry}</span>}
        </div>
        <button
          onClick={async () => { setLoading(true); await onAnalyze(company.id); setLoading(false); }}
          disabled={loading}
          style={{ background: loading ? "#94a3b8" : "#6366f1", color: "#fff", border: "none", borderRadius: 6, padding: "6px 14px", cursor: loading ? "default" : "pointer", fontSize: 13 }}
        >
          {loading ? "Analyzing…" : "Analyze"}
        </button>
      </div>
      {company.overall_score > 0 && (
        <div style={{ marginTop: 12 }}>
          <ScoreBar value={company.overall_score} label="Overall" />
          <ScoreBar value={company.cosell_score} label="Co-sell" />
          <ScoreBar value={company.buying_intent_score} label="Buying intent" />
        </div>
      )}
      {company.claude_summary && (
        <p style={{ marginTop: 10, fontSize: 14, color: "#475569", borderLeft: "3px solid #6366f1", paddingLeft: 10 }}>
          {company.claude_summary}
        </p>
      )}
    </div>
  );
}

export default function Home() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [form, setForm] = useState({ name: "", domain: "", industry: "" });
  const [adding, setAdding] = useState(false);
  const [recommendation, setRecommendation] = useState("");
  const [streaming, setStreaming] = useState(false);
  const [context, setContext] = useState("");

  const load = useCallback(async () => {
    const data = await fetchCompanies();
    setCompanies(data);
  }, []);

  useEffect(() => { load(); }, [load]);

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    if (!form.name || !form.domain) return;
    setAdding(true);
    await addCompany({ name: form.name, domain: form.domain, industry: form.industry });
    setForm({ name: "", domain: "", industry: "" });
    await load();
    setAdding(false);
  }

  async function handleAnalyze(id: string) {
    await analyzeCompany(id);
    await load();
  }

  async function handleRecommend() {
    setRecommendation("");
    setStreaming(true);
    await streamRecommendations(context, (chunk) => setRecommendation((prev) => prev + chunk));
    setStreaming(false);
  }

  return (
    <>
      <h1 style={{ marginTop: 0 }}>Company Discovery</h1>

      {/* Add company */}
      <form onSubmit={handleAdd} style={{ display: "flex", gap: 8, marginBottom: 28, flexWrap: "wrap" }}>
        <input value={form.name} onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
          placeholder="Company name" required style={inputStyle} />
        <input value={form.domain} onChange={e => setForm(f => ({ ...f, domain: e.target.value }))}
          placeholder="domain.com" required style={inputStyle} />
        <input value={form.industry} onChange={e => setForm(f => ({ ...f, industry: e.target.value }))}
          placeholder="Industry (optional)" style={inputStyle} />
        <button type="submit" disabled={adding}
          style={{ background: "#1e293b", color: "#fff", border: "none", borderRadius: 6, padding: "8px 18px", cursor: adding ? "default" : "pointer" }}>
          {adding ? "Adding…" : "+ Add"}
        </button>
      </form>

      {/* Company list */}
      {companies.length === 0
        ? <p style={{ color: "#94a3b8" }}>No companies yet. Add one above to get started.</p>
        : companies.map(c => <CompanyCard key={c.id} company={c} onAnalyze={handleAnalyze} />)
      }

      {/* AI Recommendations */}
      {companies.some(c => c.overall_score > 0) && (
        <div style={{ marginTop: 32, background: "#fff", borderRadius: 10, padding: 20, boxShadow: "0 1px 4px rgba(0,0,0,.08)" }}>
          <h2 style={{ marginTop: 0 }}>Meeting Recommendations</h2>
          <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
            <input value={context} onChange={e => setContext(e.target.value)}
              placeholder="Any extra context for Claude? (optional)" style={{ ...inputStyle, flex: 1 }} />
            <button onClick={handleRecommend} disabled={streaming}
              style={{ background: "#6366f1", color: "#fff", border: "none", borderRadius: 6, padding: "8px 18px", cursor: streaming ? "default" : "pointer" }}>
              {streaming ? "Thinking…" : "Get recommendations"}
            </button>
          </div>
          {recommendation && (
            <pre style={{ whiteSpace: "pre-wrap", fontSize: 14, color: "#334155", margin: 0 }}>{recommendation}</pre>
          )}
        </div>
      )}
    </>
  );
}

const inputStyle: React.CSSProperties = {
  border: "1px solid #cbd5e1", borderRadius: 6, padding: "8px 12px", fontSize: 14, outline: "none",
};
