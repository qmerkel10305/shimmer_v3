import useFetch from 'react-fetch-hook';
import CircularProgress from '@mui/material/CircularProgress';

export default function Image({ imageId }) {
  const { isLoading, data } = useFetch(
    `http://localhost:8000/get_img/${imageId}`,
    { formatter: (response) => response.blob() },
  );

  return (
    <>
      {!isLoading && (
        <div className='max-w-40 aspect-auto rounded-xl shadow overflow-clip hover:scale-125 hover:shadow-gray-600 hover:shadow-md transition-all'>
          <img src={URL.createObjectURL(data)} className={'w-full h-full'} />
        </div>
      )}
      <CircularProgress className={isLoading ? 'm-auto' : 'hidden'} />
    </>
  );
}
