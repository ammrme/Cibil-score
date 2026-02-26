import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./CheckScore.css";

function CheckScore() {
  const [gpayFile, setGpayFile] = useState(null);
  const [phonepeFile, setPhonepeFile] = useState(null);
  const [bankFile, setBankFile] = useState(null);

  const navigate = useNavigate();

 const uploadFile = async (file, endpoint) => {
  if (!file) {
    alert("Please upload a PDF file");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    console.log("Backend response:", result);

    // 🔐 PASSWORD REQUIRED
   // 🔐 PASSWORD REQUIRED
if (result.password_required === true) {
  navigate("/enter-password", {
    state: { 
      file_id: result.file_id,   // ✅ THIS IS REQUIRED
      source: endpoint           // optional but useful
    }
  });
  return;
}


// ✅ SUCCESS
if (result.success === true) {
  navigate("/result", {
    state: {
      cibil_score: result.cibil_score,
      risk_category: result.risk_category
    }
  });
  return;
}

// ❌ OTHER ERRORS
alert("Prediction failed");


  } catch (error) {
    console.error("Upload error:", error);
    alert("Something went wrong");
  }
};

  return (
    <div className="check-score-page">
      <h1>Check Your Credit Score</h1>

      <div className="cards-container">

        {/* ---------------- GPay Card ---------------- */}
        <div className="upload-card-box">
          <h2>Upload Google Pay Statement</h2>

          <input
            type="file"
            id="gpay"
            accept="application/pdf"
            onChange={(e) => setGpayFile(e.target.files[0])}
          />

          <label htmlFor="gpay" className="upload-label">
            {gpayFile ? gpayFile.name : "Choose PDF File"}
          </label>

          <button
            className="upload-btn"
            onClick={() =>
              uploadFile(gpayFile, "http://127.0.0.1:8000/upload-gpay")
            }
          >
            Upload GPay PDF
          </button>
        </div>

        {/* ---------------- PhonePe Card ---------------- */}
        <div className="upload-card-box">
          <h2>Upload PhonePe Statement</h2>

          <input
            type="file"
            id="phonepe"
            accept="application/pdf"
            onChange={(e) => setPhonepeFile(e.target.files[0])}
          />

          <label htmlFor="phonepe" className="upload-label">
            {phonepeFile ? phonepeFile.name : "Choose PDF File"}
          </label>

          <button
            className="upload-btn"
            onClick={() =>
              uploadFile(phonepeFile, "http://127.0.0.1:8000/upload-phonepe")
            }
          >
            Upload PhonePe PDF
          </button>
        </div>

        {/* ---------------- Bank Card ---------------- */}
        <div className="upload-card-box">
          <h2>Upload Bank Statement</h2>

          <input
            type="file"
            id="bank"
            accept="application/pdf"
            onChange={(e) => setBankFile(e.target.files[0])}
          />

          <label htmlFor="bank" className="upload-label">
            {bankFile ? bankFile.name : "Choose PDF File"}
          </label>

          <button
            className="upload-btn"
            onClick={() =>
              uploadFile(bankFile, "http://127.0.0.1:8000/upload-bank")
            }
          >
            Upload Bank Statement
          </button>
        </div>

      </div>
    </div>
  );
}

export default CheckScore;
