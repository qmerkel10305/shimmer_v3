import { useCallback, useEffect, useState } from 'react';
import Image from './Image';
import TargetPopup from './TargetPopup';

export default function FlightImages({ imageIds }) {
  const [overlayState, setOverlayState] = useState({
    open: false,
    imageId: null,
  });
  const openOverlay = (imageUrl, imageId) => setOverlayState({ open: true, imageUrl, imageId });
  const closeOverlay = () => setOverlayState({ open: false });

  useEffect(() => {
    if (overlayState.open) {
      const close = (e) => {
        if (e.key === `Escape`) {
          console.log('Escape Pressed');
          setOverlayState((prev) => {
            return {
              open: false,
              imageUrl: prev.imageUrl,
              imageId: prev.imageId,
            };
          });
          console.log(overlayState);
        }
      };
      window.addEventListener('keydown', close);
      return () => window.removeEventListener('keydown', close);
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
        <TargetPopup overlayState={overlayState} closeOverlay={closeOverlay}/>
      )}
    </section>
  );
}
