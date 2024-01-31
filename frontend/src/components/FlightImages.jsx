import Image from '../components/Image.jsx';

export default function FlightImages() {
  const imageUrls = [
    '/0.jpg',
    '/1.jpg',
    '/2.jpg',
    '/3.jpg',
    '/4.jpg',
    '/5.jpg',
    '/6.jpg',
  ];
  return (
    <section className='grid grid-cols-[repeat(auto-fill,minmax(160px,1fr))] pt-4 px-1 justify-items-center gap-4'>
      {imageUrls.map((url) => (
        <Image imageUrl={url} key={url} />
      ))}
    </section>
  );
}
