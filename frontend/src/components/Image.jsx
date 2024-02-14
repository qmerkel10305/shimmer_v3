import useFetch from 'react-fetch-hook';
import CircularProgress from '@mui/material/CircularProgress';

export default function Image({ imageId, openOverlay }) {
  const { isLoading, data } = useFetch(
    `http://localhost:5000/get_img/${imageId}`,
    {
      formatter: (response) =>
        response.blob().then((blob) => URL.createObjectURL(blob)),
    },
  );

  return (
    <>
      {!isLoading && (
        <div className='max-w-40 aspect-auto rounded-xl shadow overflow-clip hover:scale-125 hover:shadow-gray-600 hover:shadow-md transition-all'>
          <img
            src={data}
            className={'w-full h-full'}
            onClick={() => openOverlay(data)}
          />
        </div>
      )}
      {isLoading && <CircularProgress className='m-auto' />}
    </>
  );
}
