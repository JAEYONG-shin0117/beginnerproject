import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App"; // 기본 내보내기로 가져오기

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
);
