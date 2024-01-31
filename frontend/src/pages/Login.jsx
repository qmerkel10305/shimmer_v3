import { Autocomplete, TextField, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const navigate = useNavigate();

  return (
    <main className='flex flex-col items-center w-screen h-screen justify-center'>
      <Typography variant='h3' className='italic'>
        Shimmer
      </Typography>
      <Autocomplete
        disablePortal
        id='combo-box-demo'
        options={['something', 'another']}
        sx={{ width: 300 }}
        renderInput={(params) => <TextField {...params} label='Flight Id' />}
        onChange={(event) => {
          let flightId = event.target.textContent;
          console.log(flightId);
          navigate(`/${flightId}/flight`);
        }}
      />
    </main>
  );
}
