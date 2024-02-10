export default function TargetPopup({ overlayState, closeOverlay }) {
  return (
    <>
      {overlayState.open ? (
        <div className='fixed top-0 left-0'>
          <div
            className='fixed z-10 w-screen h-screen bg-stone-800 opacity-35'
            onClick={closeOverlay}></div>
          <div
            className={
              'fixed overflow-hidden rounded-xl flex flex-row top-1/2 left-1/2 translate-x-[-50%] translate-y-[-50%] bg-white z-20'
            }>
            <img src={overlayState.imageUrl} className='w-[90vw] h-max' />
          </div>
        </div>
      ) : (
        ''
      )}
    </>
  );
}
