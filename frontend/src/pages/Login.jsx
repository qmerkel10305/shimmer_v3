import { Autocomplete, TextField, Typography } from '@mui/material';
import useFetch from 'react-fetch-hook';
import { useNavigate } from 'react-router-dom';
import CircularProgress from '@mui/material/CircularProgress';
import { liveFlightId } from './App';

export default function Login() {
  const navigate = useNavigate();

  const apiUrl = 'http://localhost:5000/get_flights/';
  let {
    isLoading,
    error,
    data: flightNames,
  } = useFetch(apiUrl, {
    formatter: (response) =>
      response.json().then((flightNames) => {
        flightNames.push(liveFlightId);
        return flightNames;
      }),
  });

  return (
    <main className='flex flex-col items-center w-screen h-screen justify-center'>
      <Typography variant='h3' className='italic'>
        Shimmer
      </Typography>
      <Autocomplete
        disablePortal
        id='combo-box-demo'
        options={flightNames ?? [liveFlightId]}
        sx={{ width: 300 }}
        renderInput={(params) => (
          <TextField
            {...params}
            label='Flight Id'
            error={!!error}
            helperText={error ? `Failed to fetch ${apiUrl}` : ''}
          />
        )}
        onChange={(event) => {
          let flightId = event.target.textContent;
          navigate(`/${flightId}/flight`);
        }}
      />
      <CircularProgress color='success' className={isLoading ? '' : 'hidden'} />
    </main>
  );
}
