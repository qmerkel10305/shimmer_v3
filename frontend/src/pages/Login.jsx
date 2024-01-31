import { Autocomplete, TextField, Typography } from '@mui/material';
import useFetch from 'react-fetch-hook';
import { useNavigate } from 'react-router-dom';
import CircularProgress from '@mui/material/CircularProgress';

export default function Login() {
  const navigate = useNavigate();

  const apiUrl = 'http://localhost:8000/get_flights/';
  const { isLoading, error, data: flightNames } = useFetch(apiUrl);

  return (
    <main className='flex flex-col items-center w-screen h-screen justify-center'>
      <Typography variant='h3' className='italic'>
        Shimmer
      </Typography>
      <Autocomplete
        disablePortal
        id='combo-box-demo'
        options={flightNames ?? []}
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
          console.log(flightId);
          navigate(`/${flightId}/flight`);
        }}
      />
      <CircularProgress color='success' className={isLoading ? '' : 'hidden'} />
    </main>
  );
}
