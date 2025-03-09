import React from "react";
import "./Result.css"; // Import custom styles

const Result = ({ extractedText }) => {
  return (
    <div className="result-container">
      <h2>📜 Extracted Text</h2>
      <textarea className="text-box" value={extractedText} rows="10" readOnly />
    </div>
  );
};

export default Result;
