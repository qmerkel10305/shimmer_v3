import AddIcon from '@mui/icons-material/Add';
import { IconButton } from '@mui/material';
import React, { useRef, useState, useEffect } from 'react';
import Target from '../components/Target';
import Metadata from '../components/Metadata';
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

  /*
  IMPORTANT
  Max sizings of images is optimized for portrait orientation, to fix, switch height and width style values
  */
  return (
    <>
      {overlayState.open ? (
        <div className='fixed top-0 left-0'>
          <div
            className='fixed z-10 w-screen h-screen bg-stone-800 opacity-35'
            onClick={closeOverlay}
          />
          <div 
            className='fixed top-1/2 left-1/2 z-20 flex flex-row' 
            style={{height: '92vh', width:'auto', maxHeight: '92vh', maxWidth: '90vw', justifyContent:'center', transform:`translate(-50%, -50%)`}}
            
          >
            {/* Images that open in new tab when clicked
            <a href={overlayState.imageUrl} target="_blank" style={{height:'92vh', objectFit: 'contain'}}>
              <img src={overlayState.imageUrl} style={{maxWidth:'100%', maxHeight:'100%', objectFit: 'contain'}}/>
            </a> */}
            {/* Zoomable images */}
            <div className='rounded-xl overflow-auto flex flex-col bg-gray-900'>
              <TransformWrapper>
                <TransformComponent>
                  <div style={{height: '92vh', width: 'auto', objectPosition: 'center', display:'flex'}}>
                    <img 
                      src={overlayState.imageUrl} 
                      style={{maxWidth:'100%', maxHeight:'100%', objectFit: 'contain', objectPosition: 'center'}}
                    />
                  </div>
                </TransformComponent>
              </TransformWrapper>
            </div>
            <div className='flex flex-col' onClick={closeOverlay}>
              <div className='rounded-xl' style={{alignSelf: 'start', width: 'min-content', whiteSpace:'nowrap', backgroundColor:'white', paddingRight:'20px'}} >
                <Metadata imageId={overlayState.imageId}/>
              </div>
            </div>
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
