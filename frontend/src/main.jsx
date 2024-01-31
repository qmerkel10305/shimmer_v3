import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './pages/App.jsx';
import './main.css';
import CssBaseline from '@mui/material/CssBaseline';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import '@fontsource/roboto/300-italic.css';
import '@fontsource/roboto/400-italic.css';
import '@fontsource/roboto/500-italic.css';
import '@fontsource/roboto/700-italic.css';
import { StyledEngineProvider } from '@mui/material/styles';
import { BrowserRouter } from 'react-router-dom';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <StyledEngineProvider>
        <CssBaseline>
          <App />
        </CssBaseline>
      </StyledEngineProvider>
    </BrowserRouter>
  </React.StrictMode>,
);
