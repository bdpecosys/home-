"""
Collects co-selling and buying-intent signals from open sources.

Current sources:
  - NewsAPI     (news mentions, funding rounds, product launches)
  - GitHub API  (open-source activity / tech stack signals)
  - Hunter.io   (company info enrichment)

Extend by adding more sources below and registering them in `collect_signals`.
"""
import httpx
from typing import Any
from datetime import datetime, timedelta

from app.config import settings


async def fetch_news_signals(company_name: str) -> list[dict[str, Any]]:
    """Search NewsAPI for recent mentions of the company."""
    if not settings.news_api_key:
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": f'"{company_name}"',
        "from": (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d"),
        "sortBy": "relevancy",
        "language": "en",
        "pageSize": 10,
        "apiKey": settings.news_api_key,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        if resp.status_code != 200:
            return []
        articles = resp.json().get("articles", [])

    return [
        {
            "source": "news",
            "title": a["title"],
            "url": a["url"],
            "published_at": a["publishedAt"],
            "description": a.get("description", ""),
        }
        for a in articles
    ]


async def fetch_github_signals(domain: str) -> list[dict[str, Any]]:
    """
    Check if the company has public GitHub repos with recent activity.
    Uses the unauthenticated GitHub Search API (60 req/h).
    """
    org_name = domain.split(".")[0]  # rough heuristic
    url = f"https://api.github.com/orgs/{org_name}/repos"
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, headers=headers, params={"per_page": 5, "sort": "pushed"})
        if resp.status_code != 200:
            return []
        repos = resp.json()

    return [
        {
            "source": "github",
            "repo": r["full_name"],
            "stars": r["stargazers_count"],
            "last_pushed": r["pushed_at"],
            "description": r.get("description", ""),
        }
        for r in repos
        if isinstance(r, dict)
    ]


async def collect_signals(company_name: str, domain: str) -> list[dict[str, Any]]:
    """Aggregate signals from all sources for a given company."""
    news = await fetch_news_signals(company_name)
    github = await fetch_github_signals(domain)
    return news + github
