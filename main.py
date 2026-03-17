from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from forecast import forecast_sales

app = FastAPI()

# ✅ Enable CORS (allow all origins for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["http://localhost:3000"] for React, etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to the Sales Forecasting API"}

@app.post("/forecast")
async def forecast(file: UploadFile = File(...)):
    try:
        # Read uploaded CSV
        df = pd.read_csv(file.file)

        # Run forecasting pipeline
        forecast_df = forecast_sales(df)

        # Return forecast as JSON
        return forecast_df.to_dict(orient="records")

    except ValueError as ve:
        # User-friendly error (bad CSV format, not enough rows, etc.)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

