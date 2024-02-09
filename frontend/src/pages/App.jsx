import { Navigate, Route, Routes } from 'react-router-dom';
import Login from './Login.jsx';
import Flight from './Flight.jsx';

export const liveFlightId = 'Live';

export default function App() {
  return (
    <div>
      <Routes>
        <Route path='/' element={<Navigate to='/login' />} />
        <Route path='/login' element={<Login />} />
        <Route path='/:flightId/flight' element={<Flight />} />
      </Routes>
    </div>
  );
}
