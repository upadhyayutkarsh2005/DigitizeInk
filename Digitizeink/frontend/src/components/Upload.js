import React, { useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import "./Upload.css"; // Import custom styles

const Upload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      toast.error("Please select a file!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData);
      toast.success("Upload successful!");
      onUploadSuccess(response.data);  // Send data to parent component
    } catch (error) {
      toast.error("Upload failed!");
      console.error(error);
    }
  };

  return (
    <div className="upload-container">
      <input type="file" accept="image/*" onChange={handleFileChange} className="file-input" />
      <button className="upload-btn" onClick={handleUpload}>🚀 Upload</button>
    </div>
  );
};

export default Upload;
