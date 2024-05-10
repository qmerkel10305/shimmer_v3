import useFetch from 'react-fetch-hook';
import CircularProgress from '@mui/material/CircularProgress';

export default function Metadata({ imageId }) {
    const {isLoading, data} = useFetch(
      `http://localhost:5000/get_img_metadata/${imageId}`,
    );
    console.log(isLoading);
    console.log("Metadata: ", data);
    return (
      <>
        {!isLoading && data && (
          <ul>
          {Object.entries(data).map(([key, value]) => (
            <li key={key}><strong>{key}:</strong> {value}</li>
          ))}
          </ul>
        )}
        {isLoading && <CircularProgress className='m-auto' />}
      </>
    )
  }
  