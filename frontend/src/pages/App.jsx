import { Navigate, Route, Routes } from "react-router-dom";
import Login from "./Login.jsx";
import Shimmer from "./Shimmer.jsx";

export default function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/shimmer" element={<Shimmer />} />
      </Routes>
    </div>
  );
}
