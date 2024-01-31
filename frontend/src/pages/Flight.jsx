import { Navigate, useParams } from 'react-router-dom';
import FlightImages from '../components/FlightImages';
import CircularProgress from '@mui/material/CircularProgress';
import HouseIcon from '@mui/icons-material/House';
import { Icon, IconButton, Typography } from '@mui/material';
import PublishedWithChangesIcon from '@mui/icons-material/PublishedWithChanges';
import SyncIcon from '@mui/icons-material/Sync';
import SyncProblemIcon from '@mui/icons-material/SyncProblem';
import Snackbar from '@mui/material/Snackbar';

import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
export default function Flight() {
  const { flightId } = useParams();
  const navigate = useNavigate();

  const [isOpen, setIsOpen] = useState(false);

  const toServer = new WebSocket('ws://localhost:8000/ws');

  toServer.addEventListener('message', (event) => {
    console.log(`Received message ${event.data}`);
  });
  toServer.addEventListener('close', (event) =>
    console.log(`Socket closed ${event.data}`),
  );
  toServer.addEventListener('error', (event) =>
    console.log(`Error logged ${event.data}`),
  );

  return (
    <main>
      <nav className='flex flex-row justify-between items-center p-2 bg-blue-300 rounded-b-xl'>
        <IconButton onClick={() => navigate('/')} className='p-0'>
          <HouseIcon />
        </IconButton>
        <Typography variant='h6'>{flightId}</Typography>
        <IconButton onClick={() => setIsOpen(true)}>
          <PublishedWithChangesIcon />
        </IconButton>
      </nav>
      <FlightImages />
      <CircularProgress color='success' />
      <Snackbar
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        open={isOpen}
        onClose={() => setIsOpen(false)}
        autoHideDuration={2000}
        message='Refreshing...'
        className='w-fit mx-auto'
      />
    </main>
  );
}
