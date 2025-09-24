from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, UploadFile, File
from pathlib import Path
import pandas as pd
import os
import uuid

from .. import data_store.DATA_STORE as DATA_STORE


# current_path = Path(__file__).resolve()

# # Go up two levels: from /router/ to /app/ and then to /backend/
# backend_dir = router_path.parent.parent.parent

# # Define the UPLOAD_DIR relative to the backend folder
# UPLOAD_DIR = backend_dir / "uploaded_files"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(
    prefix="/upload",
    tags=["Upload Data"]
)


@router.get("/")
async def upload_file(file: UploadFile = File(...)):
    """Handle file upload (CSV or Excel).
    - Reads file into Pandas DataFrame
    - Stores in DATA_STORE with a unique file_id
    - Returns file_id and preview rows"""

    # file_id = str(uuid.uuid4())
    # file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        elif file.filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file.file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Upload CSV or Excel.")

        # Generate unique file_id
        file_id = str(uuid.uuid4())
        DATA_STORE[file_id] = df

        # Build preview (first 5 rows)
        preview = df.head(5).to_dict(orient="records")

        return {
            "file_id": file_id,
            "preview": preview,
            "columns": df.columns.tolist(),
            "rows": len(df)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")