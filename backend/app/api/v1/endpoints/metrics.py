"""Endpoints for dashboard metrics and scorecards (placeholder)."""

from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/dashboard", summary="Get dashboard metrics")
async def get_dashboard_metrics():
    """Retrieve high-level dashboard metrics."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")

@router.get("/scorecards", summary="Get scorecards")
async def get_scorecards():
    """Retrieve participation scorecards."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")