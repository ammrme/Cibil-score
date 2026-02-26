# ==========================================================
# FASTAPI MAIN APPLICATION - FINAL CORRECTED VERSION
# ==========================================================

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import uuid

from pdf_utils import phonepe_pdf_to_dataset
from model import run_ml_prediction


# ==========================================================
# INITIALIZE APP
# ==========================================================

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================================
# ROOT CHECK
# ==========================================================

@app.get("/")
def root():
    return {"message": "Credit Scoring API Running 🚀"}


# ==========================================================
# UPLOAD PHONEPE PDF
# ==========================================================

@app.post("/upload-phonepe")
async def upload_phonepe(file: UploadFile = File(...)):
    try:
        # Generate unique file_id
        file_id = str(uuid.uuid4())
        saved_filename = f"{file_id}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, saved_filename)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Try parsing without password
        dataset, error = phonepe_pdf_to_dataset(file_path)

        # If password protected
        if error == "password_required":
            return {
                "success": False,
                "password_required": True,
                "file_id": saved_filename   # ✅ FIXED
            }

        # Other parsing error
        if error:
            return {
                "success": False,
                "message": error
            }

        # No transactions found
        if dataset is None or dataset.empty:
            return {
                "success": False,
                "message": "No transactions found"
            }

        # Run ML prediction
        prediction = run_ml_prediction(dataset)

        return {
            "success": True,
            "password_required": False,
            "cibil_score": prediction["cibil_score"],
            "risk_category": prediction["risk_category"]
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }


# ==========================================================
# PASSWORD VERIFY ENDPOINT
# ==========================================================

class PasswordRequest(BaseModel):
    file_id: str   # ✅ FIXED
    password: str


@app.post("/verify-password")
async def verify_password(data: PasswordRequest):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, data.file_id)  # ✅ FIXED

        if not os.path.exists(file_path):
            return {
                "success": False,
                "message": "File not found"
            }

        # Parse with password
        dataset, error = phonepe_pdf_to_dataset(
            file_path,
            password=data.password
        )

        # Wrong password
        if error == "wrong_password":
            return {
                "success": False,
                "message": "Incorrect password"
            }

        # Other parsing error
        if error:
            return {
                "success": False,
                "message": error
            }

        # No transactions found
        if dataset is None or dataset.empty:
            return {
                "success": False,
                "message": "No transactions found"
            }

        # Run ML prediction
        prediction = run_ml_prediction(dataset)

        return {
            "success": True,
            "cibil_score": prediction["cibil_score"],
            "risk_category": prediction["risk_category"]
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
