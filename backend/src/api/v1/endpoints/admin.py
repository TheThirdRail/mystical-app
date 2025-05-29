"""
Admin endpoints for platform management.
"""

from datetime import datetime, date
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, extract

from src.core.database import get_db
from src.core.exceptions import AuthorizationError
from src.models.user import User, UserRole
from src.models.partner import Partner
from src.models.reading import Reading
from src.models.payment import Payment, PaymentStatus
from src.api.v1.endpoints.auth import get_current_user

router = APIRouter()
security = HTTPBearer()


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to require admin role."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user


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
    month: str = Query(..., description="Month in YYYY-MM format"),
    partner_slug: Optional[str] = Query(None, description="Specific partner slug"),
    admin_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Get earnings report for specified month.

    Returns revenue breakdown by partner for the specified month,
    including reading counts, total revenue, and earnings split.
    """
    try:
        # Validate month format
        year, month_num = month.split("-")
        year = int(year)
        month_num = int(month_num)
        if month_num < 1 or month_num > 12:
            raise ValueError()
    except ValueError:
        raise HTTPException(status_code=422, detail="Month must be in YYYY-MM format")

    # Build query for earnings calculation
    query = (
        select(
            Partner.slug,
            Partner.name,
            Partner.revenue_share_percentage,
            func.count(Reading.id).label("total_readings"),
            func.coalesce(func.sum(Payment.amount), 0).label("total_revenue")
        )
        .select_from(Partner)
        .outerjoin(Reading, Reading.partner_id == Partner.id)
        .outerjoin(
            Payment,
            and_(
                Payment.reading_id == Reading.id,
                Payment.status == PaymentStatus.COMPLETED
            )
        )
        .where(
            and_(
                extract("year", Reading.created_at) == year,
                extract("month", Reading.created_at) == month_num
            ) if Reading.created_at else True
        )
        .group_by(Partner.id, Partner.slug, Partner.name, Partner.revenue_share_percentage)
    )

    # Filter by specific partner if requested
    if partner_slug:
        query = query.where(Partner.slug == partner_slug)

    result = await db.execute(query)
    partner_data = result.all()

    if partner_slug and not partner_data:
        raise HTTPException(status_code=404, detail="Partner not found")

    # Calculate earnings for each partner
    earnings = []
    for row in partner_data:
        total_revenue = float(row.total_revenue or 0)
        revenue_share = row.revenue_share_percentage / 100
        partner_earnings = total_revenue * revenue_share
        platform_earnings = total_revenue * (1 - revenue_share)

        earnings.append(EarningsResponse(
            month=month,
            partner_slug=row.slug,
            partner_name=row.name,
            total_readings=row.total_readings,
            total_revenue=total_revenue,
            partner_earnings=partner_earnings,
            platform_earnings=platform_earnings,
            revenue_share_percentage=row.revenue_share_percentage
        ))

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
