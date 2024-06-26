import { useNavigate, useParams } from 'react-router-dom';
import FlightImages from '../components/FlightImages';
import HouseIcon from '@mui/icons-material/House';
import { IconButton, Typography } from '@mui/material';
import PublishedWithChangesIcon from '@mui/icons-material/PublishedWithChanges';
import SyncIcon from '@mui/icons-material/Sync';
import SyncProblemIcon from '@mui/icons-material/SyncProblem';
import Snackbar from '@mui/material/Snackbar';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { useState } from 'react';
import { liveFlightId } from './App';
import { useEffect } from 'react';

export default function Flight() {
  const { flightId } = useParams();
  const navigate = useNavigate();
  const [imageIds, setImageIds] = useState([]);

  const [isOpen, setIsOpen] = useState(false);

  const { lastJsonMessage, sendJsonMessage, readyState } = useWebSocket(
    'ws://localhost:5000/ws',
    {
      shouldReconnect: () => true,
      reconnectAttempts: 1000,
      share: false,
    },
  );

  useEffect(() => {
    if (readyState === ReadyState.OPEN) {
      sendJsonMessage({
        type: 'connect',
        flight_id: flightId === liveFlightId ? '' : flightId,
      });
    }
  }, [readyState, sendJsonMessage]);

  useEffect(() => {
    if (lastJsonMessage !== null && lastJsonMessage.type === 'img') {
      if (flightId === liveFlightId) {
        navigate(`/${lastJsonMessage.flight_id}/flight`, { replace: true });
        setImageIds((prev) => [...prev, lastJsonMessage.img_id]);
      } else if (lastJsonMessage.flight_id !== flightId) {
        console.error(`Received image which doesn't belong to this flight`);
        console.error(lastJsonMessage);
      } else {
        setImageIds((prev) => [...prev, lastJsonMessage.img_id]);
      }
    }
  }, [lastJsonMessage, setImageIds]);

  const [connectionIcon, snackbarMessage] = {
    [ReadyState.CONNECTING]: [
      <SyncIcon className='animate-spin transform rotate-180' />,
      'Connecting...',
    ],
    [ReadyState.OPEN]: [<PublishedWithChangesIcon />, 'Connection is live'],
    [ReadyState.CLOSING]: [<SyncProblemIcon />, 'Connection closing'],
    [ReadyState.CLOSED]: [<SyncProblemIcon />, 'Connection closed'],
    [ReadyState.UNINSTANTIATED]: [<SyncProblemIcon />, 'Not connected'],
  }[readyState];

  return (
    <main>
      <nav className='flex flex-row justify-between items-center p-2 bg-red-500 rounded-b-xl'>
        <IconButton onClick={() => navigate('/')} className='p-0'>
          <HouseIcon />
        </IconButton>
        <Typography variant='h6'>{flightId}</Typography>
        <IconButton onClick={() => setIsOpen(true)}>
          {connectionIcon}
        </IconButton>
      </nav>
      <FlightImages imageIds={imageIds} />
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
