import { useCallback, useEffect, useState } from 'react';
import Image from './Image';
import TargetPopup from './TargetPopup';

export default function FlightImages({ imageIds }) {
  const [overlayState, setOverlayState] = useState({
    open: false,
  });
  const openOverlay = (imageUrl) => setOverlayState({ open: true, imageUrl });
  const closeOverlay = () => setOverlayState({ open: false });

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
    <section className='grid grid-cols-[repeat(auto-fill,minmax(160px,1fr))] pt-4 px-1 justify-items-center gap-x-3 gap-y-4'>
      {imageIds.map((imageId) => (
        <Image
          imageId={imageId}
          key={imageId}
          openOverlay={openOverlay}
          closeOverlay={closeOverlay}
        />
      ))}
      {imageIds && (
        <TargetPopup overlayState={overlayState} closeOverlay={closeOverlay} />
      )}
    </section>
  );
}
