from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import uuid

from app.database import get_db
from app.models.company import Company
from app.services.signal_collector import collect_signals
from app.services.claude_service import analyze_company, stream_recommendation

router = APIRouter(prefix="/companies", tags=["companies"])


class CompanyCreate(BaseModel):
    name: str
    domain: str
    description: str = ""
    industry: str = ""


class CompanyOut(BaseModel):
    id: str
    name: str
    domain: str
    description: str
    industry: str
    cosell_score: float
    buying_intent_score: float
    overall_score: float
    claude_summary: str
    signals: list

    class Config:
        from_attributes = True


@router.get("/", response_model=list[CompanyOut])
async def list_companies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Company).order_by(Company.overall_score.desc())
    )
    companies = result.scalars().all()
    return [CompanyOut(
        id=str(c.id), name=c.name, domain=c.domain,
        description=c.description or "", industry=c.industry or "",
        cosell_score=c.cosell_score or 0.0,
        buying_intent_score=c.buying_intent_score or 0.0,
        overall_score=c.overall_score or 0.0,
        claude_summary=c.claude_summary or "",
        signals=c.signals or [],
    ) for c in companies]


@router.post("/", response_model=CompanyOut, status_code=201)
async def add_company(payload: CompanyCreate, db: AsyncSession = Depends(get_db)):
    company = Company(
        name=payload.name,
        domain=payload.domain,
        description=payload.description,
        industry=payload.industry,
    )
    db.add(company)
    await db.commit()
    await db.refresh(company)
    return CompanyOut(
        id=str(company.id), name=company.name, domain=company.domain,
        description=company.description or "", industry=company.industry or "",
        cosell_score=0.0, buying_intent_score=0.0, overall_score=0.0,
        claude_summary="", signals=[],
    )


@router.post("/{company_id}/analyze", response_model=CompanyOut)
async def analyze(company_id: str, db: AsyncSession = Depends(get_db)):
    """Collect signals and run Claude analysis for a specific company."""
    result = await db.execute(select(Company).where(Company.id == uuid.UUID(company_id)))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    signals = await collect_signals(company.name, company.domain)
    analysis = await analyze_company(company.name, company.domain, company.description or "", signals)

    company.signals = signals
    company.cosell_score = analysis.get("cosell_score", 0.0)
    company.buying_intent_score = analysis.get("buying_intent_score", 0.0)
    company.overall_score = analysis.get("overall_score", 0.0)
    company.claude_summary = analysis.get("summary", "")

    await db.commit()
    await db.refresh(company)

    return CompanyOut(
        id=str(company.id), name=company.name, domain=company.domain,
        description=company.description or "", industry=company.industry or "",
        cosell_score=company.cosell_score or 0.0,
        buying_intent_score=company.buying_intent_score or 0.0,
        overall_score=company.overall_score or 0.0,
        claude_summary=company.claude_summary or "",
        signals=company.signals or [],
    )


class RecommendationRequest(BaseModel):
    context: str = ""


@router.post("/recommendations/stream")
async def get_recommendations(
    payload: RecommendationRequest,
    db: AsyncSession = Depends(get_db),
):
    """Stream a CEO meeting recommendation list from Claude."""
    result = await db.execute(
        select(Company).order_by(Company.overall_score.desc()).limit(10)
    )
    companies = result.scalars().all()

    company_dicts = [
        {
            "name": c.name,
            "cosell_score": c.cosell_score or 0.0,
            "buying_intent_score": c.buying_intent_score or 0.0,
            "overall_score": c.overall_score or 0.0,
            "claude_summary": c.claude_summary or "",
        }
        for c in companies
    ]

    return StreamingResponse(
        stream_recommendation(company_dicts, payload.context),
        media_type="text/plain",
    )
