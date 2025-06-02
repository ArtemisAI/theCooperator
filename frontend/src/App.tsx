import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, Button, Box } from '@mui/material';
import logger from '@utils/logger';
import TodoPage from '@pages/TodoPage'; // Using path alias
import MembersPage from '@pages/Members'; // Import MembersPage

// A simple placeholder for other pages like Dashboard
const DashboardPage = () => (
  <Container>
    <Typography variant="h4" component="h1" gutterBottom sx={{ mt: 2 }}>
      Dashboard
    </Typography>
    <Typography variant="body1">Welcome to the dashboard!</Typography>
  </Container>
);

const navLinkStyle = ({ isActive }: { isActive: boolean }) => ({
  fontWeight: isActive ? 'bold' : 'normal',
  color: isActive ? 'primary.main' : 'inherit', // Use theme's primary color for active link
  textDecoration: 'none',
  marginRight: '16px', // Add some spacing between nav links
});

export default function App() {
  logger.info('App component rendered with Router');

  return (
    <Router>
      <AppBar position="sticky" elevation={1}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, color: 'primary.main' }}>
            TheCooperator
          </Typography>
          <Box sx={{ display: 'flex' }}>
            <Button
              color="inherit"
              component={NavLink}
              to="/"
              style={navLinkStyle}
            >
              Dashboard
            </Button>
            <Button
              color="inherit"
              component={NavLink}
              to="/members"
              style={navLinkStyle}
            >
              Members
            </Button>
            <Button
              color="inherit"
              component={NavLink}
              to="/todos"
              style={navLinkStyle}
            >
              Todos
            </Button>
            {/* TODO: Add other navigation links */}
          </Box>
        </Toolbar>
      </AppBar>
      <Container sx={{ mt: 4, backgroundColor: 'background.default', minHeight: 'calc(100vh - 64px - 32px)', p: 3 }}> {/* 64px AppBar, 32px top margin */}
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/members" element={<MembersPage />} />
          <Route path="/todos" element={<TodoPage />} />
          {/* TODO: Add other routes for Members, Units, Tasks, Votes, Scorecards */}
        </Routes>
      </Container>
    </Router>
  );
}
