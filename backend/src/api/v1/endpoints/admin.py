"""
Admin endpoints for platform management.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field

router = APIRouter()
security = HTTPBearer()


class EarningsRequest(BaseModel):
    """Earnings report request schema."""
    month: str = Field(..., description="Month in YYYY-MM format")
    partner_slug: Optional[str] = Field(None, description="Specific partner slug")


class EarningsResponse(BaseModel):
    """Earnings report response schema."""
    month: str
    partner_slug: str
    partner_name: str
    total_readings: int
    total_revenue: float
    partner_earnings: float
    platform_earnings: float
    revenue_share_percentage: float


@router.get("/earnings")
async def get_earnings_report(
    month: str,
    partner_slug: Optional[str] = None,
    token: str = Depends(security)
):
    """
    Get earnings report for specified month.
    
    Returns revenue breakdown by partner for the specified month,
    including reading counts, total revenue, and earnings split.
    """
    # TODO: Implement earnings calculation from database
    # For now, return mock data
    
    try:
        # Validate month format
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        raise HTTPException(status_code=422, detail="Month must be in YYYY-MM format")
    
    # Mock earnings data
    earnings = [
        EarningsResponse(
            month=month,
            partner_slug="metamystic",
            partner_name="MetaMystic",
            total_readings=0,
            total_revenue=0.0,
            partner_earnings=0.0,
            platform_earnings=0.0,
            revenue_share_percentage=0.0
        )
    ]
    
    if partner_slug:
        earnings = [e for e in earnings if e.partner_slug == partner_slug]
        if not earnings:
            raise HTTPException(status_code=404, detail="Partner not found")
    
    return {
        "success": True,
        "data": {
            "month": month,
            "earnings": earnings,
            "summary": {
                "total_partners": len(earnings),
                "total_readings": sum(e.total_readings for e in earnings),
                "total_revenue": sum(e.total_revenue for e in earnings),
                "total_partner_earnings": sum(e.partner_earnings for e in earnings),
                "total_platform_earnings": sum(e.platform_earnings for e in earnings)
            }
        }
    }


@router.get("/stats")
async def get_platform_stats(token: str = Depends(security)):
    """
    Get platform statistics.
    
    Returns overall platform metrics including user counts,
    reading statistics, and partner information.
    """
    # TODO: Implement stats calculation from database
    return {
        "success": True,
        "data": {
            "users": {
                "total": 0,
                "active_monthly": 0,
                "new_this_month": 0
            },
            "readings": {
                "total": 0,
                "this_month": 0,
                "average_per_day": 0.0,
                "completion_rate": 0.0
            },
            "partners": {
                "total": 1,
                "verified": 1,
                "active": 1
            },
            "revenue": {
                "total": 0.0,
                "this_month": 0.0,
                "average_per_reading": 0.0
            }
        }
    }


@router.get("/health")
async def get_system_health():
    """
    Get system health status.
    
    Returns health status of various system components including
    database, LLM providers, and external services.
    """
    # TODO: Implement actual health checks
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "database": {"status": "healthy", "response_time_ms": 10},
                "redis": {"status": "healthy", "response_time_ms": 5},
                "llm_providers": {
                    "openai": {"status": "unknown", "configured": False},
                    "anthropic": {"status": "unknown", "configured": False},
                    "google": {"status": "unknown", "configured": False},
                    "meta": {"status": "unknown", "configured": False}
                },
                "storage": {"status": "healthy", "available_space": "unlimited"}
            }
        }
    }
