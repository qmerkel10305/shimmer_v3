import AddIcon from '@mui/icons-material/Add';
import { IconButton } from '@mui/material';

export default function TargetPopup({ overlayState, closeOverlay }) {
  const targets = ['A', 'B', 'C', 'D', 'E'];
  return (
    <>
      {overlayState.open ? (
        <div className='fixed top-0 left-0'>
          <div
            className='fixed z-10 w-screen h-screen bg-stone-800 opacity-35'
            onClick={closeOverlay}
          />
          <div className='fixed rounded-xl overflow-hidden top-1/2 left-1/2 translate-x-[-50%] translate-y-[-50%] z-20 flex flex-col w-max max-w-[90vw] max-h-[92vh] bg-gray-800'>
            <img src={overlayState.imageUrl} />
            <div className='flex flex-row gap-1 p-1 overflow-x-scroll overflow-y-hidden scrollbar-none'>
              {targets.map((letter) => (
                // no idea why h-[20vw] is necessary as it should have the minimum height of the <img>
                // or why img rounded-2xl works way better than div rounded-2xl + overflow-hidden
                <div className='relative w-[20vw] h-[20vw] aspect-square'>
                  <img
                    src={overlayState.imageUrl}
                    className='w-full aspect-square object-cover rounded-2xl'
                  />
                  <span className='absolute -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2 font-medium text-8xl opacity-75'>
                    {letter}
                  </span>
                </div>
              ))}
              <IconButton className='aspect-square w-[20vw] rounded-xl border-2 border-solid border-red-500'>
                <AddIcon className='fill-red-500' />
              </IconButton>
            </div>
          </div>
        </div>
      ) : (
        ''
      )}
    </>
  );
}
