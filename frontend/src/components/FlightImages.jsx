import Image from './Image';

export default function FlightImages({ imageIds }) {
  return (
    <section className='grid grid-cols-[repeat(auto-fill,minmax(160px,1fr))] pt-4 px-1 justify-items-center gap-4'>
      {imageIds.map((imageId) => (
        <Image imageId={imageId} key={imageId} />
      ))}
    </section>
  );
}
