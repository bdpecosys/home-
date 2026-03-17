const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Company {
  id: string;
  name: string;
  domain: string;
  description: string;
  industry: string;
  cosell_score: number;
  buying_intent_score: number;
  overall_score: number;
  claude_summary: string;
  signals: unknown[];
}

export async function fetchCompanies(): Promise<Company[]> {
  const res = await fetch(`${API_URL}/companies/`);
  if (!res.ok) throw new Error("Failed to fetch companies");
  return res.json();
}

export async function addCompany(data: {
  name: string;
  domain: string;
  description?: string;
  industry?: string;
}): Promise<Company> {
  const res = await fetch(`${API_URL}/companies/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to add company");
  return res.json();
}

export async function analyzeCompany(companyId: string): Promise<Company> {
  const res = await fetch(`${API_URL}/companies/${companyId}/analyze`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Failed to analyze company");
  return res.json();
}

export async function streamRecommendations(
  context: string,
  onChunk: (text: string) => void,
): Promise<void> {
  const res = await fetch(`${API_URL}/companies/recommendations/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ context }),
  });
  if (!res.ok || !res.body) throw new Error("Failed to stream recommendations");

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    onChunk(decoder.decode(value, { stream: true }));
  }
}
