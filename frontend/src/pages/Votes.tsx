import React from 'react';
import { VoteChart } from '../components/VoteChart';

/**
 * Votes page
 *
 * - Lists active proposals and allows users to cast votes.
 * - Displays results using VoteChart component.
 *
 * TODO:
 *  - Implement proposals list, vote form, and results visualization.
 */

export default function VotesPage() {
  return (
    <div>
      <h1>Votes</h1>
      {/* TODO: Implement voting UI */}
      <VoteChart />
    </div>
  );
}
