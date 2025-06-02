"""Business logic for metrics and scorecard computations (placeholder)."""

from app.crud.score_entry import create_score_entry, list_score_entries
from app.schemas.score_entry import ScoreEntryCreate

def recompute_scorecards() -> None:
    """Recompute participation scores for all users."""
    # TODO: implement nightly score recomputation logic
    pass

def aggregate_dashboard_metrics() -> None:
    """Collect high-level metrics for dashboard (member count, task stats, vote stats)."""
    # TODO: aggregate counts and summaries
    pass