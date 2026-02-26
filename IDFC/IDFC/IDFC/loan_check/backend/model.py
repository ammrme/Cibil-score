# ==========================================================
# LOAD TRAINED CREDIT MODEL FOR PREDICTION
# ==========================================================

import pandas as pd
import joblib

# Load trained model once
model = joblib.load("credit_model.pkl")


def run_ml_prediction(df: pd.DataFrame):

    df = df.copy()

    features = [
        "monthly_income",
        "monthly_spent",
        "savings_ratio",
        "debit_credit_ratio",
        "income_volatility",
        "working_days",
        "bill_payment_ratio",
        "txns_per_day"
    ]

    # Ensure missing values handled
    df = df.fillna(0)

    # Ensure all required columns exist
    for col in features:
        if col not in df.columns:
            df[col] = 0

    # Make prediction
    predictions = model.predict(df[features])

    df["prediction"] = predictions

    # Map to CIBIL-like score
    score_map = {
        "SAFE": 780,
        "MEDIUM": 680,
        "RISK": 580
    }

    df["cibil_score"] = df["prediction"].map(score_map)
    df["risk_category"] = df["prediction"]

    # Take latest month result
    latest = df.iloc[-1]

    return {
        "cibil_score": int(latest["cibil_score"]),
        "risk_category": str(latest["risk_category"]),
        "prediction": str(latest["prediction"])
    }
