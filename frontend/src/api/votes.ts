/**
 * API service for Vote endpoints (/api/v1/votes).
 *
 * TODO:
 *  - listVotes(): GET /api/v1/votes
 *  - getVote(id): GET /api/v1/votes/{id}
 *  - createVote(data): POST /api/v1/votes
 *  - castVote(pollId, choice): POST /api/v1/votes/{pollId}
 */

import { apiClient } from '../utils/apiClient';
import type { VoteRead, VoteCreate } from '../types';

export async function listVotes(): Promise<VoteRead[]> {
  // TODO: implement API call
  return [];
}

export async function getVote(id: string): Promise<VoteRead> {
  // TODO: implement API call
  throw new Error('Not implemented');
}

export async function createVote(data: VoteCreate): Promise<VoteRead> {
  // TODO: implement API call
  throw new Error('Not implemented');
}

export async function castVote(pollId: string, choice: string): Promise<void> {
  // TODO: implement API call
  throw new Error('Not implemented');
}
