import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

const SummaryPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const file = location.state?.file;

  // 가짜 데이터 (원문 텍스트 및 요약문)
  const originalText = "This is the original text extracted from the file.";
  const summaryText = "This is the summarized version of the text.";

  if (!file) {
    return <p>No file uploaded. Please go back and upload a file.</p>;
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Summary Page</h1>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <div style={{ width: "45%" }}>
          <h3>Original Text</h3>
          <p>{originalText}</p>
        </div>
        <div style={{ width: "45%" }}>
          <h3>Summary</h3>
          <p>{summaryText}</p>
        </div>
      </div>
      <button onClick={() => navigate("/")} style={{ marginTop: "20px" }}>
        Back to Upload
      </button>
    </div>
  );
};

export default SummaryPage;
