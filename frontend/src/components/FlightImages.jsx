import { useEffect, useState } from 'react';
import Image from './Image';

export default function FlightImages({ lastJsonMessage }) {
  const [imageIds, setImageIds] = useState([]);

  useEffect(() => {
    if (lastJsonMessage !== null && lastJsonMessage.type === 'img') {
      setImageIds((prev) => [...prev, lastJsonMessage.img_id]);
    }
  }, [lastJsonMessage, setImageIds]);

  return (
    <section className='grid grid-cols-[repeat(auto-fill,minmax(160px,1fr))] pt-4 px-1 justify-items-center gap-4'>
      {imageIds.map((imageId) => (
        <Image imageId={imageId} key={imageId} />
      ))}
    </section>
  );
}
