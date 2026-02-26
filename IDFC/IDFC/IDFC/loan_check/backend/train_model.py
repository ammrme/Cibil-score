# ==========================================================
# TRAIN REAL CREDIT RISK MODEL (HACKATHON VERSION)
# ==========================================================

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# ----------------------------------------------------------
# STEP 1: SET RANDOM SEED (For same results every time)
# ----------------------------------------------------------
np.random.seed(42)

# ----------------------------------------------------------
# STEP 2: GENERATE SYNTHETIC DATA (5000 CUSTOMERS)
# ----------------------------------------------------------

n = 5000

data = pd.DataFrame({
    "monthly_income": np.random.randint(5000, 50000, n),
    "monthly_spent": np.random.randint(2000, 40000, n),
    "income_volatility": np.random.randint(500, 8000, n),
    "working_days": np.random.randint(5, 30, n),
    "txns_per_day": np.random.randint(1, 10, n)
})

# ----------------------------------------------------------
# STEP 3: CREATE DERIVED FEATURES
# ----------------------------------------------------------

data["savings_ratio"] = (
    (data["monthly_income"] - data["monthly_spent"]) 
    / data["monthly_income"]
)

data["debit_credit_ratio"] = (
    data["monthly_spent"] / data["monthly_income"]
)

data["bill_payment_ratio"] = np.random.uniform(0.3, 1.0, n)

# Clip unrealistic values
data["savings_ratio"] = data["savings_ratio"].clip(-0.5, 0.6)
data["debit_credit_ratio"] = data["debit_credit_ratio"].clip(0, 2)

# ----------------------------------------------------------
# STEP 4: CREATE REALISTIC RISK LABELS
# ----------------------------------------------------------

def assign_risk(row):

    score = 0

    if row["monthly_income"] > 20000:
        score += 2

    if row["savings_ratio"] > 0.2:
        score += 2

    if row["income_volatility"] < 3000:
        score += 1

    if row["debit_credit_ratio"] < 0.8:
        score += 2

    if row["bill_payment_ratio"] > 0.7:
        score += 2

    if score >= 7:
        return "SAFE"
    elif score >= 4:
        return "MEDIUM"
    else:
        return "RISK"

data["risk_label"] = data.apply(assign_risk, axis=1)

# ----------------------------------------------------------
# STEP 5: TRAIN MODEL
# ----------------------------------------------------------

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

X = data[features]
y = data["risk_label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

print("Model Accuracy:", round(accuracy * 100, 2), "%")

# ----------------------------------------------------------
# STEP 6: SAVE TRAINED MODEL
# ----------------------------------------------------------

joblib.dump(model, "credit_model.pkl")

print("Model saved successfully as credit_model.pkl")
