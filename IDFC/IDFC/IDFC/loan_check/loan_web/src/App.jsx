import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home.jsx";
import CheckScore from "./pages/CheckScore.jsx";
import Result from "./pages/Result.jsx";
import EnterPassword from "./pages/password.jsx";


function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/check-score" element={<CheckScore />} />
      <Route path="/enter-password" element={<EnterPassword />} />
      <Route path="/result" element={<Result />} />
    </Routes>
  );
}

export default App;
