import React, { useState } from "react";
import Upload from "./components/Upload";
import Result from "./components/Result";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./App.css";

const App = () => {
  const [textData, setTextData] = useState(null);

  console.log("Current Text Data:", textData); // Debugging

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>DigitizeInk - Image to Text</h1>
      <Upload onUploadSuccess={setTextData} />
      {textData && textData.extracted_text ? (
        <Result extractedText={textData.extracted_text} />
      ) : (
        <p style={{ color: "gray", fontStyle: "italic" }}>No text extracted yet.</p>
      )}
      <ToastContainer />
    </div>
  );
};

export default App;
