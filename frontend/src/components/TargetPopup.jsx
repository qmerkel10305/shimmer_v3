export default function TargetPopup({ overlayState }) {
  return <div className={overlayState.open ? 'absolute ' : 'hidden'}>hi</div>;
}
