import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@utils/apiClient'; // Assuming alias for ../utils/apiClient
import type { Unit, UnitCreate, UnitUpdate } from '@src/types'; // Assuming alias for ../types

const UNITS_API_BASE_URL = '/api/v1/units';

// Fetch all units
const fetchUnits = async (): Promise<Unit[]> => {
  return apiClient(UNITS_API_BASE_URL) as Promise<Unit[]>;
};

export const useUnits = () => {
  return useQuery<Unit[], Error>({
    queryKey: ['units'],
    queryFn: fetchUnits,
  });
};

// Fetch a single unit by ID
const fetchUnitById = async (unitId: string): Promise<Unit> => {
  return apiClient(`${UNITS_API_BASE_URL}/${unitId}`) as Promise<Unit>;
};

export const useUnit = (unitId: string) => {
  return useQuery<Unit, Error>({
    queryKey: ['units', unitId],
    queryFn: () => fetchUnitById(unitId),
    enabled: !!unitId, // Only run query if unitId is provided
  });
};

// Create a new unit
const createUnit = async (unitData: UnitCreate): Promise<Unit> => {
  return apiClient(UNITS_API_BASE_URL, {
    method: 'POST',
    body: JSON.stringify(unitData),
  }) as Promise<Unit>;
};

export const useCreateUnit = () => {
  const queryClient = useQueryClient();
  return useMutation<Unit, Error, UnitCreate>({
    mutationFn: createUnit,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['units'] });
    },
  });
};

// Update an existing unit
const updateUnit = async ({ unitId, unitData }: { unitId: string; unitData: UnitUpdate }): Promise<Unit> => {
  return apiClient(`${UNITS_API_BASE_URL}/${unitId}`, {
    method: 'PUT',
    body: JSON.stringify(unitData),
  }) as Promise<Unit>;
};

export const useUpdateUnit = () => {
  const queryClient = useQueryClient();
  return useMutation<Unit, Error, { unitId: string; unitData: UnitUpdate }>({
    mutationFn: updateUnit,
    onSuccess: (_data, variables) => { // _data is the updated unit from server
      queryClient.invalidateQueries({ queryKey: ['units'] });
      queryClient.invalidateQueries({ queryKey: ['units', variables.unitId] });
      // Optionally, update the specific query data directly
      // queryClient.setQueryData(['units', variables.unitId], _data);
    },
  });
};

// Delete a unit
const deleteUnit = async (unitId: string): Promise<void> => {
  await apiClient(`${UNITS_API_BASE_URL}/${unitId}`, {
    method: 'DELETE',
  });
  // apiClient for DELETE might not return content. Assuming it handles empty responses for 204.
};

export const useDeleteUnit = () => {
  const queryClient = useQueryClient();
  return useMutation<void, Error, string>({
    mutationFn: deleteUnit,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['units'] });
    },
  });
};
