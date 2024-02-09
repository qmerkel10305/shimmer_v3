import { Navigate, useParams } from 'react-router-dom';
import FlightImages from '../components/FlightImages';
import HouseIcon from '@mui/icons-material/House';
import { Icon, IconButton, Typography } from '@mui/material';
import PublishedWithChangesIcon from '@mui/icons-material/PublishedWithChanges';
import SyncIcon from '@mui/icons-material/Sync';
import SyncProblemIcon from '@mui/icons-material/SyncProblem';
import Snackbar from '@mui/material/Snackbar';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { liveFlightId } from './App';

export default function Flight() {
  const { flightId } = useParams();
  const navigate = useNavigate();

  const [isOpen, setIsOpen] = useState(false);

  const { lastJsonMessage, sendJsonMessage, readyState } = useWebSocket(
    'ws://localhost:8000/ws',
    {
      shouldReconnect: () => true,
      reconnectAttempts: 1000,
    },
  );

  const [connectionIcon, snackbarMessage] = {
    [ReadyState.CONNECTING]: [
      <SyncIcon className='animate-spin transform rotate-180' />,
      'Connecting...',
    ],
    [ReadyState.OPEN]: [<PublishedWithChangesIcon />, 'Connection opened'],
    [ReadyState.CLOSING]: [<SyncProblemIcon />, 'Connection closing'],
    [ReadyState.CLOSED]: [<SyncProblemIcon />, 'Connection closed'],
    [ReadyState.UNINSTANTIATED]: [<SyncProblemIcon />, 'Not connected'],
  }[readyState];

  if (flightId === liveFlightId) {
    sendJsonMessage(
      JSON.stringify({
        type: 'connect',
        flight_id: flightId,
      }),
    );
  }

  if (lastJsonMessage !== null && lastJsonMessage.type === 'img') {
    if (lastJsonMessage.flight_id !== flightId) {
      console.error(`Received image which doesn't belong to this flight`);
      console.error(lastJsonMessage);
    } else if (flightId === liveFlightId) {
      navigate(`/${lastJsonMessage.flight_id}/flight`);
    }
  }

  return (
    <main>
      <nav className='flex flex-row justify-between items-center p-2 bg-blue-300 rounded-b-xl'>
        <IconButton onClick={() => navigate('/')} className='p-0'>
          <HouseIcon />
        </IconButton>
        <Typography variant='h6'>{flightId}</Typography>
        <IconButton onClick={() => setIsOpen(true)}>
          {connectionIcon}
        </IconButton>
      </nav>
      <FlightImages lastJsonMessage={lastJsonMessage} />
      <Snackbar
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        open={isOpen}
        onClose={() => setIsOpen(false)}
        autoHideDuration={2000}
        message={snackbarMessage}
        className='w-fit mx-auto'
      />
    </main>
  );
}
