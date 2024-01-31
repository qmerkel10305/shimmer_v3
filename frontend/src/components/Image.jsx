export default function Image({ imageUrl }) {
  return (
    <div className='max-w-40 aspect-auto bg-red-500 rounded-xl shadow overflow-clip hover:scale-125 hover:shadow-gray-600 hover:shadow-md transition-all'>
      <img src={imageUrl} className='w-full h-full' />
    </div>
  );
}
