import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const FileUploadPage = () => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      if (!selectedFile.type.startsWith("image/")) {
        setError("Only image files are allowed.");
        setFile(null);
        return;
      }
      setFile(selectedFile);
      setError("");
    }
  };

  const handleSubmit = () => {
    if (!file) {
      setError("Please upload a valid file.");
      return;
    }
    navigate("/summary", { state: { file } });
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.headerTitle}>Summary Site</h1>
        <p style={styles.headerSubtitle}>
          Upload your files and see the extracted text and summary.
        </p>
      </header>
      <main style={styles.main}>
        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Welcome to the Summary Site!</h2>
          <div style={styles.uploadBox}>
            <h3 style={styles.uploadTitle}>Upload Your File</h3>
            <input
              type="file"
              onChange={handleFileChange}
              style={styles.fileInput}
            />
            {error && <p style={styles.errorText}>{error}</p>}
            {file && (
              <div style={styles.previewContainer}>
                <h4 style={styles.previewTitle}>Preview:</h4>
                <img
                  src={URL.createObjectURL(file)}
                  alt="Preview"
                  style={styles.imagePreview}
                />
              </div>
            )}
            <button onClick={handleSubmit} style={styles.submitButton}>
              Process File
            </button>
          </div>
        </div>
      </main>
      <footer style={styles.footer}>
        <p>&copy; 2025 Summary Site. All rights reserved.</p>
      </footer>
    </div>
  );
};

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    minHeight: "100vh",
    background: "linear-gradient(135deg, #f0f4f8, #d9e8ff)",
    fontFamily: "'Roboto', sans-serif",
    color: "#333",
  },
  header: {
    backgroundColor: "#4a90e2",
    color: "#fff",
    textAlign: "center",
    padding: "20px 10px",
  },
  headerTitle: {
    fontSize: "2.5rem",
    margin: "0",
  },
  headerSubtitle: {
    fontSize: "1.2rem",
    margin: "10px 0 0",
  },
  main: {
    flex: "1",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    padding: "20px",
  },
  card: {
    background: "#fff",
    borderRadius: "10px",
    boxShadow: "0 4px 20px rgba(0, 0, 0, 0.1)",
    padding: "30px",
    maxWidth: "500px",
    width: "100%",
    textAlign: "center",
  },
  cardTitle: {
    fontSize: "1.8rem",
    color: "#4a90e2",
    marginBottom: "20px",
  },
  uploadBox: {
    marginTop: "20px",
  },
  uploadTitle: {
    fontSize: "1.5rem",
    marginBottom: "15px",
  },
  fileInput: {
    display: "block",
    margin: "10px auto",
    padding: "10px",
    fontSize: "1rem",
    borderRadius: "5px",
    border: "1px solid #ccc",
    width: "90%",
  },
  errorText: {
    color: "#e74c3c",
    fontSize: "0.9rem",
    marginTop: "10px",
  },
  previewContainer: {
    marginTop: "20px",
  },
  previewTitle: {
    fontSize: "1.2rem",
    marginBottom: "10px",
  },
  imagePreview: {
    width: "100%",
    maxWidth: "200px",
    borderRadius: "10px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  },
  submitButton: {
    marginTop: "20px",
    padding: "10px 20px",
    fontSize: "1rem",
    color: "#fff",
    backgroundColor: "#4a90e2",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    transition: "background 0.3s ease",
  },
  submitButtonHover: {
    backgroundColor: "#357ABD",
  },
  footer: {
    textAlign: "center",
    backgroundColor: "#f0f4f8",
    padding: "10px 0",
    fontSize: "0.9rem",
  },
};

export default FileUploadPage;
