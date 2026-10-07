"""API FastAPI : charge le pipeline sérialisé (pkl) et expose /predict."""
import os
import pickle
from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

MODEL_PATH = Path(os.getenv("MODEL_PATH", Path(__file__).resolve().parent.parent / "model" / "diabetes_pipeline.pkl"))

with open(MODEL_PATH, "rb") as f:
    pipeline = pickle.load(f)

app = FastAPI(title="API Prédiction Diabète", version="1.0")


class Patient(BaseModel):
    Pregnancies: int = Field(..., ge=0, le=20, description="Nombre de grossesses")
    Glucose: float = Field(..., ge=0, le=300)
    BloodPressure: float = Field(..., ge=0, le=200)
    SkinThickness: float = Field(..., ge=0, le=100)
    Insulin: float = Field(..., ge=0, le=900)
    BMI: float = Field(..., ge=0, le=80)
    DiabetesPedigreeFunction: float = Field(..., ge=0, le=3)
    Age: int = Field(..., ge=1, le=120)


@app.get("/")
def root():
    return {"message": "API diabète OK", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(patient: Patient):
    df = pd.DataFrame([patient.model_dump()])
    pred = int(pipeline.predict(df)[0])
    proba = float(pipeline.predict_proba(df)[0][1])
    return {
        "prediction": pred,
        "label": "Diabète détecté" if pred == 1 else "Pas de diabète",
        "probability": round(proba, 4),
    }
