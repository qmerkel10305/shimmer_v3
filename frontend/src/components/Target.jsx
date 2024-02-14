import React from 'react';

export default function Target({ imageUrl, letter, coordinates }) {
  return (
    // no idea why h-[20vw] is necessary as it should have the minimum height of the <img>
    // or why img rounded-2xl works way better than div rounded-2xl + overflow-hidden
    <div className='relative w-[20vw] h-[20vw] aspect-square'>
      <img
        src={imageUrl}
        className='w-full aspect-square object-cover rounded-2xl'
      />
      <span className='absolute -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2 font-medium text-8xl opacity-75'>
        {letter}
      </span>
    </div>
  );
}
