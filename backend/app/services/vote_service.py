"""Business logic for voting operations."""

from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import (
    proposal as proposal_crud,
    user as user_crud,
    vote as vote_crud,
)
from app.core.exceptions import ProposalNotFoundException

QUORUM_PERCENTAGE = 0.50  # 50%

async def is_quorum_reached(db: AsyncSession, proposal_id: str) -> bool:
    """
    Checks if the quorum for voting has been reached for a given proposal.
    """
    proposal = await proposal_crud.get_proposal(session=db, proposal_id=proposal_id)
    if not proposal:
        raise ProposalNotFoundException(f"Proposal with id {proposal_id} not found.")

    # Determine total number of eligible voters
    # Assuming all users in the system are eligible voters for simplicity.
    # This could be refined based on proposal type, unit association, etc.
    total_eligible_voters = await user_crud.get_active_users_count(session=db)

    if total_eligible_voters == 0:
        return False # No eligible voters, so quorum cannot be reached.

    # Count unique votes cast for the proposal
    # The current vote_crud.get_votes_count_for_proposal counts all vote entries.
    # If one user can vote multiple times (which shouldn't be the case for proposals),
    # this count would be number of vote entries. If each user votes once, it's unique voters.
    # Assuming current setup implies one vote per user per proposal (enforced elsewhere or by design).
    votes_cast = await vote_crud.get_votes_count_for_proposal(
        session=db, proposal_id=proposal_id
    )

    actual_percentage = votes_cast / total_eligible_voters
    return actual_percentage >= QUORUM_PERCENTAGE

async def get_proposal_results(db: AsyncSession, proposal_id: str) -> dict:
    """
    Calculates and returns the results for a given proposal,
    also indicating if quorum was met.
    """
    proposal = await proposal_crud.get_proposal(session=db, proposal_id=proposal_id)
    if not proposal:
        raise ProposalNotFoundException(f"Proposal with id {proposal_id} not found.")

    quorum_met = await is_quorum_reached(db=db, proposal_id=proposal_id)

    votes = await vote_crud.list_votes_for_proposal(session=db, proposal_id=proposal_id)

    results_summary = {}
    for vote in votes:
        results_summary[vote.choice] = results_summary.get(vote.choice, 0) + 1

    return {
        "proposal_id": proposal_id,
        "title": proposal.title,
        "quorum_met": quorum_met,
        "votes_cast": len(votes),
        "results_summary": results_summary,
        # Add more details like winner if applicable based on rules
    }

# Placeholder for other functions
def tally_votes() -> None: # This name is similar to get_proposal_results
    """Aggregate votes for a proposal into results."""
    # TODO: count votes and return results structure (covered by get_proposal_results)
    pass