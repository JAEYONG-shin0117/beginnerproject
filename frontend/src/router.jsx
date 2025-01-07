import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MainPage from "./pages/MainPage";
import MainPage2 from "./pages/MainPage2";

const AppRouter = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/summary" element={<MainPage2 />} />
      </Routes>
    </Router>
  );
};

export default AppRouter;
