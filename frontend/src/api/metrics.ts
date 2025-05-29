/**
 * API service for Metrics endpoints (/api/v1/metrics).
 *
 * TODO:
 *  - getDashboardMetrics(): GET /api/v1/metrics/dashboard
 *  - getScorecards(): GET /api/v1/metrics/scorecards
 */

import { apiClient } from '../utils/apiClient';
import type { DashboardMetrics, Scorecard } from '../types';

export async function getDashboardMetrics(): Promise<DashboardMetrics> {
  // TODO: implement API call
  throw new Error('Not implemented');
}

export async function getScorecards(): Promise<Scorecard[]> {
  // TODO: implement API call
  throw new Error('Not implemented');
}
