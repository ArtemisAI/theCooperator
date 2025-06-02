import React, { useState } from 'react';
import {
  Container, Box, Button, Typography, Paper,
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  IconButton, Dialog, DialogTitle, DialogContent, DialogActions,
  TextField, CircularProgress, Alert, Tooltip
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';

import { useUnits, useCreateUnit, useUpdateUnit, useDeleteUnit } from '@api/units'; // Assuming alias
import type { Unit, UnitCreate, UnitUpdate } from '@src/types'; // Assuming alias

const UnitsPage: React.FC = () => {
  const { data: units, isLoading: isLoadingUnits, isError: isErrorUnits, error: errorUnits } = useUnits();
  const createUnitMutation = useCreateUnit();
  const updateUnitMutation = useUpdateUnit();
  const deleteUnitMutation = useDeleteUnit();

  // Dialog states
  const [openCreateDialog, setOpenCreateDialog] = useState(false);
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);

  // Form states
  const [currentUnit, setCurrentUnit] = useState<Partial<UnitCreate> | Partial<UnitUpdate>>({});
  const [editingUnit, setEditingUnit] = useState<Unit | null>(null);
  const [unitToDeleteId, setUnitToDeleteId] = useState<string | null>(null);

  // --- Dialog Handlers ---
  const handleOpenCreateDialog = () => {
    setCurrentUnit({});
    setOpenCreateDialog(true);
  };
  const handleCloseCreateDialog = () => setOpenCreateDialog(false);

  const handleOpenEditDialog = (unit: Unit) => {
    setEditingUnit(unit);
    setCurrentUnit({ name: unit.name, address: unit.address, description: unit.description || '' });
    setOpenEditDialog(true);
  };
  const handleCloseEditDialog = () => {
    setOpenEditDialog(false);
    setEditingUnit(null);
    setCurrentUnit({});
  };

  const handleOpenDeleteDialog = (unitId: string) => {
    setUnitToDeleteId(unitId);
    setOpenDeleteDialog(true);
  };
  const handleCloseDeleteDialog = () => {
    setOpenDeleteDialog(false);
    setUnitToDeleteId(null);
  };

  // --- Form Input Handler ---
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setCurrentUnit(prev => ({ ...prev, [name]: value }));
  };

  // --- Mutation Handlers ---
  const handleCreateUnit = () => {
    if (!currentUnit.name || !currentUnit.address) {
      alert('Name and Address are required.'); // Simple validation
      return;
    }
    createUnitMutation.mutate(currentUnit as UnitCreate, {
      onSuccess: handleCloseCreateDialog,
    });
  };

  const handleUpdateUnit = () => {
    if (!editingUnit || !currentUnit.name || !currentUnit.address) {
      alert('Name and Address are required.'); // Simple validation
      return;
    }
    // Only send changed data
    const payload: UnitUpdate = {};
    if (currentUnit.name !== editingUnit.name) payload.name = currentUnit.name;
    if (currentUnit.address !== editingUnit.address) payload.address = currentUnit.address;
    if (currentUnit.description !== (editingUnit.description || '')) payload.description = currentUnit.description;

    if (Object.keys(payload).length > 0) {
        updateUnitMutation.mutate({ unitId: editingUnit.id, unitData: payload }, {
          onSuccess: handleCloseEditDialog,
        });
    } else {
        handleCloseEditDialog(); // No changes
    }
  };

  const handleDeleteUnit = () => {
    if (unitToDeleteId) {
      deleteUnitMutation.mutate(unitToDeleteId, {
        onSuccess: handleCloseDeleteDialog,
        onError: handleCloseDeleteDialog, // Close dialog even on error
      });
    }
  };

  // --- Render Logic ---
  if (isLoadingUnits) {
    return <Container sx={{ display: 'flex', justifyContent: 'center', mt: 5 }}><CircularProgress /></Container>;
  }
  if (isErrorUnits && errorUnits) {
    return <Container><Alert severity="error">Error fetching units: {errorUnits.message}</Alert></Container>;
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">Manage Units</Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={handleOpenCreateDialog}>Add Unit</Button>
      </Box>

      <TableContainer component={Paper} elevation={3}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 'bold' }}>Name</TableCell>
              <TableCell sx={{ fontWeight: 'bold' }}>Address</TableCell>
              <TableCell sx={{ fontWeight: 'bold' }}>Description</TableCell>
              <TableCell sx={{ fontWeight: 'bold', textAlign: 'right' }}>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {units && units.length > 0 ? units.map((unit) => (
              <TableRow key={unit.id} hover>
                <TableCell>{unit.name}</TableCell>
                <TableCell>{unit.address}</TableCell>
                <TableCell>{unit.description || 'N/A'}</TableCell>
                <TableCell align="right">
                  <Tooltip title="Edit Unit">
                    <IconButton onClick={() => handleOpenEditDialog(unit)} color="primary" size="small">
                      <EditIcon />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Delete Unit">
                    <IconButton onClick={() => handleOpenDeleteDialog(unit.id)} color="error" size="small">
                      <DeleteIcon />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            )) : (
              <TableRow>
                <TableCell colSpan={4} align="center">No units found.</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Create/Edit Dialog */}
      <Dialog open={openCreateDialog || openEditDialog} onClose={openCreateDialog ? handleCloseCreateDialog : handleCloseEditDialog} fullWidth maxWidth="sm">
        <DialogTitle>{openCreateDialog ? 'Add New Unit' : `Edit Unit: ${editingUnit?.name}`}</DialogTitle>
        <DialogContent>
          <TextField autoFocus margin="dense" name="name" label="Unit Name" type="text" fullWidth variant="outlined" value={currentUnit.name || ''} onChange={handleInputChange} required sx={{ mb: 2, mt: 1 }} />
          <TextField margin="dense" name="address" label="Address" type="text" fullWidth variant="outlined" value={currentUnit.address || ''} onChange={handleInputChange} required sx={{ mb: 2 }} />
          <TextField margin="dense" name="description" label="Description (Optional)" type="text" fullWidth multiline rows={3} variant="outlined" value={currentUnit.description || ''} onChange={handleInputChange} />
          {(createUnitMutation.isError && openCreateDialog) && <Alert severity="error" sx={{ mt: 2 }}>{createUnitMutation.error?.message || "Failed to create unit."}</Alert>}
          {(updateUnitMutation.isError && openEditDialog) && <Alert severity="error" sx={{ mt: 2 }}>{updateUnitMutation.error?.message || "Failed to update unit."}</Alert>}
        </DialogContent>
        <DialogActions>
          <Button onClick={openCreateDialog ? handleCloseCreateDialog : handleCloseEditDialog}>Cancel</Button>
          <Button
            onClick={openCreateDialog ? handleCreateUnit : handleUpdateUnit}
            variant="contained"
            disabled={(openCreateDialog && createUnitMutation.isLoading) || (openEditDialog && updateUnitMutation.isLoading)}
          >
            {(createUnitMutation.isLoading || updateUnitMutation.isLoading) ? <CircularProgress size={24} /> : (openCreateDialog ? 'Create' : 'Save Changes')}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={openDeleteDialog} onClose={handleCloseDeleteDialog}>
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent><Typography>Are you sure you want to delete this unit? This action cannot be undone.</Typography></DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDeleteDialog} disabled={deleteUnitMutation.isLoading}>Cancel</Button>
          <Button onClick={handleDeleteUnit} color="error" variant="contained" disabled={deleteUnitMutation.isLoading}>
            {deleteUnitMutation.isLoading ? <CircularProgress size={24} color="inherit" /> : 'Delete'}
          </Button>
        </DialogActions>
        {deleteUnitMutation.isError && <Alert severity="error" sx={{ m: 2 }}>{deleteUnitMutation.error?.message || "Failed to delete unit."}</Alert>}
      </Dialog>
    </Container>
  );
};

export default UnitsPage;
