"""
Reading endpoints for full spiritual consultations.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.schemas.reading import ReadingRequest, ReadingResponse
from src.services.reading_service import ReadingService
from src.core.exceptions import MetaMysticException

router = APIRouter()


@router.post("/full", response_model=ReadingResponse)
async def create_full_reading(
    request: ReadingRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a comprehensive reading combining astrology, numerology, zodiac, and tarot.
    """
    try:
        reading_service = ReadingService(db)
        
        # Create reading record
        reading = await reading_service.create_reading(request)
        
        # Process reading in background
        background_tasks.add_task(
            reading_service.process_reading,
            reading.id
        )
        
        return ReadingResponse(
            id=reading.id,
            status=reading.status,
            message="Reading is being processed. Check back in a few moments.",
            estimated_completion_time=30,  # seconds
        )
        
    except MetaMysticException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{reading_id}", response_model=ReadingResponse)
async def get_reading(
    reading_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get reading results by ID.
    """
    try:
        reading_service = ReadingService(db)
        reading = await reading_service.get_reading(reading_id)
        
        if not reading:
            raise HTTPException(status_code=404, detail="Reading not found")
            
        return ReadingResponse.from_orm(reading)
        
    except MetaMysticException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/preview")
async def preview_reading(
    request: ReadingRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Preview a reading without saving to database (for testing).
    """
    try:
        reading_service = ReadingService(db)
        preview = await reading_service.preview_reading(request)
        
        return preview
        
    except MetaMysticException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
