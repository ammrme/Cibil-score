# ==========================================================
# PDF UTILS (PHONEPE)
# ==========================================================

import fitz
import pandas as pd
import numpy as np
import cv2
import pytesseract
import re

# ---------------- REGEX ----------------
DATE_REGEX = re.compile(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}\b")
AMOUNT_REGEX = re.compile(r"₹?\s?[\d,]+\.\d{2}")

CREDIT_HINTS = ["credited", "received", "refund", "cashback", "salary"]
DEBIT_HINTS = ["paid", "debit", "sent", "purchase", "bill"]

# ==========================================================
# MAIN FUNCTION
# ==========================================================

def phonepe_pdf_to_dataset(file_path, password=None):

    try:
        doc = fitz.open(file_path)

        # 🔐 PASSWORD CHECK
        if doc.is_encrypted:
            if password:
                if not doc.authenticate(password):
                    return None, "wrong_password"
            else:
                return None, "password_required"

        lines = []

        for page in doc:
            text = page.get_text("text")

            # If scanned PDF → OCR
            if len(text.strip()) < 50:
                pix = page.get_pixmap(dpi=300)
                img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)

                if pix.n == 4:
                    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                text = pytesseract.image_to_string(gray, config="--psm 6")

            lines.extend([l.strip() for l in text.splitlines() if l.strip()])

        doc.close()

        # ================= PARSING =================

        transactions = []
        current = None

        for line in lines:

            date_match = DATE_REGEX.search(line)
            amounts = AMOUNT_REGEX.findall(line)

            if date_match:
                if current:
                    transactions.append(current)

                current = {
                    "Date": date_match.group(),
                    "Description": line,
                    "Amount": None,
                    "Type": "DEBIT"
                }

            if not current:
                continue

            current["Description"] += " " + line

            if amounts:
                try:
                    current["Amount"] = float(amounts[-1].replace("₹","").replace(",", ""))
                except:
                    pass

            low = line.lower()

            if any(k in low for k in CREDIT_HINTS):
                current["Type"] = "CREDIT"

            if any(k in low for k in DEBIT_HINTS):
                current["Type"] = "DEBIT"

            if "+₹" in line.replace(" ", ""):
                current["Type"] = "CREDIT"

        if current:
            transactions.append(current)

        df = pd.DataFrame(transactions)

        if df.empty:
            return pd.DataFrame(), None

        df["Date"] = pd.to_datetime(df["Date"], format="%b %d, %Y", errors="coerce")
        df = df.dropna(subset=["Date","Amount"]).copy()

        if df.empty:
            return pd.DataFrame(), None

        df["is_credit"] = (df["Type"]=="CREDIT").astype(int)
        df["is_debit"]  = (df["Type"]=="DEBIT").astype(int)

        df["year_month"] = df["Date"].dt.to_period("M")

        monthly = df.groupby("year_month").apply(lambda g: pd.Series({

            "monthly_income": g.loc[g["is_credit"]==1,"Amount"].sum(),
            "monthly_spent": g.loc[g["is_debit"]==1,"Amount"].sum(),
            "total_txns": len(g),
            "income_volatility": g.loc[g["is_credit"]==1,"Amount"].std() or 0,
            "working_days": g["Date"].nunique(),
            "txns_per_day": len(g) / (g["Date"].nunique() + 1),
            "debit_credit_ratio": (
                g.loc[g["is_debit"]==1,"Amount"].sum() /
                (g.loc[g["is_credit"]==1,"Amount"].sum() + 1)
            ),
            "savings_ratio": (
                (g.loc[g["is_credit"]==1,"Amount"].sum() -
                 g.loc[g["is_debit"]==1,"Amount"].sum()) /
                (g.loc[g["is_credit"]==1,"Amount"].sum() + 1)
            ),
            "bill_payment_ratio": (
                g.loc[g["is_debit"]==1,"Amount"].count() /
                (len(g) + 1)
            )

        })).reset_index(drop=True)

        monthly = monthly.fillna(0)

        return monthly, None

    except Exception as e:
        return None, str(e)
