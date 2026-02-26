import { useLocation, useNavigate } from "react-router-dom";
import "./Result.css";

function Result() {
  const location = useLocation();
  const navigate = useNavigate();

  const data = location.state;
  console.log("Result data:", data);

  if (!data) {
    return (
      <div className="result-page">
        <h2>No result found</h2>
        <button onClick={() => navigate("/check-score")}>
          Go Back
        </button>
      </div>
    );
  }

  return (
    <div className="result-page">
      <h1>Credit Score Result</h1>

      <div className="result-card">
        <h2>CIBIL Score</h2>
        <p className="score">{data.cibil_score}</p>

        <h2>Risk Category</h2>
        <p className={`risk ${data.risk_category}`}>
          {data.risk_category}
        </p>
      </div>

      <button onClick={() => navigate("/check-score")}>
        Check Another PDF
      </button>
    </div>
  );
}

export default Result;
