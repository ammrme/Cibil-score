import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./password.css";

function EnterPassword() {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const location = useLocation();
  const navigate = useNavigate();

  // ✅ Get file_id from CheckScore.jsx
  const file_id = location.state?.file_id;

  const handleSubmit = async () => {
    if (!password) {
      setError("Please enter the password");
      return;
    }

    if (!file_id) {
      setError("File reference missing. Please upload again.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/verify-password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          file_id: file_id,
          password: password
        })
      });

      const result = await response.json();
      console.log("Verify response:", result);

      // ✅ If password correct and score generated
      if (result.success) {
        navigate("/result", {
          state: {
            cibil_score: result.cibil_score,
            risk_category: result.risk_category
          }
        });
      } else {
        setError(result.message || "Incorrect password");
      }

    } catch (err) {
      console.error(err);
      setError("Something went wrong. Try again.");
    }
  };

  return (
    <div className="password-page">
      <h2>Enter PDF Password</h2>

      <input
        type="password"
        placeholder="Enter PDF Password"
        value={password}
        onChange={(e) => {
          setPassword(e.target.value);
          setError("");
        }}
      />

      {error && <p style={{ color: "red" }}>{error}</p>}

      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}

export default EnterPassword;
