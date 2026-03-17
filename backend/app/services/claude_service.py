"""
Claude Opus 4.6 service for analyzing co-selling and buying-intent signals.

Uses:
  - Adaptive thinking for deep signal analysis
  - Streaming for real-time CEO recommendations
  - Structured output (JSON) for machine-readable scores
"""
import json
import anthropic
from typing import Any, AsyncIterator

from app.config import settings

client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

ANALYSIS_SYSTEM_PROMPT = """You are an expert go-to-market strategist for a B2B SaaS startup CEO.
Your job is to analyze open-source signals about companies and determine:
1. Co-selling potential (0-1): how likely is this company to become a technology partner or reseller
2. Buying intent (0-1): how likely is this company to purchase our product in the next 90 days
3. An actionable summary for the CEO explaining WHY to meet with this company

Base your analysis on: recent news, funding rounds, hiring signals, product launches, tech stack, GitHub activity.

Always respond with valid JSON in this exact structure:
{
  "cosell_score": <float 0-1>,
  "buying_intent_score": <float 0-1>,
  "overall_score": <float 0-1>,
  "summary": "<2-3 sentence CEO-facing explanation>",
  "top_signals": ["<signal 1>", "<signal 2>", "<signal 3>"]
}"""


async def analyze_company(
    company_name: str,
    domain: str,
    description: str,
    signals: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Analyze a company's co-selling and buying intent using Claude Opus 4.6
    with adaptive thinking and structured JSON output.
    """
    signals_text = json.dumps(signals[:20], indent=2) if signals else "No signals collected yet."

    user_message = f"""Analyze this company for co-selling and buying intent:

Company: {company_name}
Domain: {domain}
Description: {description or "Unknown"}

Recent signals from open sources:
{signals_text}

Provide scores and a CEO-facing summary."""

    # Use streaming + get_final_message to handle long thinking + avoid timeouts
    async with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=2048,
        thinking={"type": "adaptive"},
        system=ANALYSIS_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        response = await stream.get_final_message()

    # Extract the JSON text block (thinking blocks come first)
    text = next(
        (block.text for block in response.content if block.type == "text"),
        "{}",
    )

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        # Claude returned prose instead of JSON — extract scores gracefully
        result = {
            "cosell_score": 0.5,
            "buying_intent_score": 0.5,
            "overall_score": 0.5,
            "summary": text[:500],
            "top_signals": [],
        }

    return result


async def stream_recommendation(
    companies: list[dict[str, Any]],
    context: str = "",
) -> AsyncIterator[str]:
    """
    Stream a prioritized meeting recommendation list for the CEO.
    Yields text chunks as they arrive from Claude.
    """
    companies_text = json.dumps(
        [
            {
                "name": c["name"],
                "cosell_score": c["cosell_score"],
                "buying_intent_score": c["buying_intent_score"],
                "overall_score": c["overall_score"],
                "summary": c["claude_summary"],
            }
            for c in sorted(companies, key=lambda x: x["overall_score"], reverse=True)[:10]
        ],
        indent=2,
    )

    user_message = f"""You are advising a startup CEO on which companies to prioritize for meetings this week.

Here are the top companies ranked by signal strength:
{companies_text}

{f"Additional context from the CEO: {context}" if context else ""}

Provide a concise, prioritized meeting recommendation list. For each company, state:
1. Why to meet (specific opportunity)
2. Who to reach out to (title/role)
3. Suggested talking points

Keep it actionable and under 500 words total."""

    async with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        async for text_chunk in stream.text_stream:
            yield text_chunk
