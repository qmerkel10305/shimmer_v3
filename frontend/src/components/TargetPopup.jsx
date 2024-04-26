import AddIcon from '@mui/icons-material/Add';
import { IconButton } from '@mui/material';
import React, { useRef, useState } from 'react';
import Target from '../components/Target';
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";

export default function TargetPopup({ overlayState, closeOverlay }) {
  const targetList = ['A', 'B', 'C', 'D', 'E'];
  const coordinates = { x: 0, y: 0 };
  const [imageWidth, setImageWidth] = useState(0); 
  const [imageHeight, setImageHeight] = useState(0);
  const targets = targetList.map((letter) => {
    return {
      letter,
      coordinates,
    };
  });


  return (
    <>
      {overlayState.open ? (
        <div className='fixed top-0 left-0'>
          <div
            className='fixed z-10 w-screen h-screen bg-stone-800 opacity-35'
            onClick={closeOverlay}
          />
          <div 
            className='fixed rounded-xl overflow-auto top-1/2 left-1/2 translate-x-[-50%] translate-y-[-50%] z-20 flex  flex-col w-max max-w-[90vw] max-h-[92vh] bg-gray-800' 
            style={{height: '92vh', width:'auto', maxWidth: '90vw'}}
            
          >
            {/* Images that open in new tab when clicked
            <a href={overlayState.imageUrl} target="_blank" style={{height:'92vh', objectFit: 'contain'}}>
              <img src={overlayState.imageUrl} style={{maxWidth:'100%', maxHeight:'100%', objectFit: 'contain'}}/>
            </a> */}
            {/* Zoomable images */}
            <TransformWrapper>
              <TransformComponent>
                <div style={{height: '92vh', width: 'auto', objectPosition: 'center', display:'flex', alignItems:'center', justifyContent:'center'}}>
                  <img 
                    src={overlayState.imageUrl} 
                    style={{maxWidth:'100%', maxHeight:'100%', objectFit: 'contain', objectPosition: 'center'}}
                  />
                </div>
              </TransformComponent>
            </TransformWrapper>
            {/* --- This may be added back in later. For the time being it causes issues with the aspect ratio ---
            <div className='flex flex-row gap-1 p-1 overflow-x-scroll overflow-y-auto scrollbar-none'>
              {targets.map((target) => (
                <Target
                  letter={target.letter}
                  coordinates={coordinates}
                  imageUrl={overlayState.imageUrl}
                  key={target.letter}
              /> 
              ))}
              <IconButton className='aspect-square w-[20vw] rounded-xl border-2 border-solid border-red-500'>
                <AddIcon className='fill-red-500' />
              </IconButton>
            </div>
            */}
          </div>
        </div>
      ) : (
        ''
      )}
    </>
  );
}
