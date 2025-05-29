/**
 * API service for Unit endpoints (/api/v1/units).
 *
 * TODO:
 *  - listUnits(limit?, offset?): GET /api/v1/units
 *  - getUnit(id): GET /api/v1/units/{id}
 *  - createUnit(data): POST /api/v1/units
 *  - updateUnit(id, data): PUT /api/v1/units/{id}
 *  - deleteUnit(id): DELETE /api/v1/units/{id}
 */

import { apiClient } from '../utils/apiClient';
import type { UnitRead, UnitCreate, UnitUpdate } from '../types';

export async function listUnits(limit?: number, offset?: number): Promise<UnitRead[]> {
  // TODO: implement API call using apiClient
  return [];
}

export async function getUnit(id: string): Promise<UnitRead> {
  // TODO: implement API call
  throw new Error('Not implemented');
}

export async function createUnit(data: UnitCreate): Promise<UnitRead> {
  // TODO: implement API call
  throw new Error('Not implemented');
}

export async function updateUnit(id: string, data: UnitUpdate): Promise<UnitRead> {
  // TODO: implement API call
  throw new Error('Not implemented');
}

export async function deleteUnit(id: string): Promise<void> {
  // TODO: implement API call
  throw new Error('Not implemented');
}
