import { useCallback, useEffect, useState } from 'react';
import Image from './Image';
import TargetPopup from './TargetPopup';

export default function FlightImages({ imageIds }) {
  const [overlayState, setOverlayState] = useState({
    open: false,
    imageUrl: '',
  });
  const openOverlay = (imageUrl) => setOverlayState({ open: true, imageUrl });

  useEffect(() => {
    if (overlayState.open) {
      console.log('set');
      const close = (e) => {
        if (e.key === `Escape`) {
          console.log('Escape Pressed');
          setOverlayState((prev) => {
            return {
              open: false,
              imageUrl: prev.imageUrl,
            };
          });
          console.log(overlayState);
        }
      };
      window.addEventListener('keydown', close);
      return () => {
        console.log('deleted');
        window.removeEventListener('keydown', close);
      };
    }
  }, [overlayState]);

  return (
    <section className='grid grid-cols-[repeat(auto-fill,minmax(160px,1fr))] pt-4 px-1 justify-items-center gap-4 relative'>
      {imageIds.map((imageId) => (
        <Image imageId={imageId} key={imageId} onClick={openOverlay} />
      ))}
      {imageIds && <TargetPopup overlayState={overlayState} />}
    </section>
  );
}
