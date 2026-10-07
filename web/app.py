"""Interface Flask : formulaire -> appel de l'API FastAPI -> affichage du résultat."""
import os

import requests
from flask import Flask, render_template, request

app = Flask(__name__)
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")

FIELDS = [
    ("Pregnancies", "Grossesses", "int", "2"),
    ("Glucose", "Glucose (mg/dL)", "float", "120"),
    ("BloodPressure", "Pression artérielle (mm Hg)", "float", "70"),
    ("SkinThickness", "Épaisseur de peau (mm)", "float", "20"),
    ("Insulin", "Insuline (mu U/ml)", "float", "80"),
    ("BMI", "IMC", "float", "28.5"),
    ("DiabetesPedigreeFunction", "Fonction pedigree diabète", "float", "0.45"),
    ("Age", "Âge", "int", "35"),
]


@app.route("/", methods=["GET", "POST"])
def index():
    result, error, values = None, None, {}
    if request.method == "POST":
        try:
            payload = {}
            for name, _, typ, _ in FIELDS:
                values[name] = request.form[name]
                payload[name] = int(values[name]) if typ == "int" else float(values[name])
            r = requests.post(API_URL, json=payload, timeout=10)
            if r.status_code == 200:
                result = r.json()
            else:
                error = f"Erreur API ({r.status_code}) : {r.text}"
        except ValueError:
            error = "Valeurs invalides : vérifiez les champs."
        except requests.exceptions.ConnectionError:
            error = "Impossible de joindre l'API FastAPI. Est-elle lancée ?"
    return render_template("index.html", fields=FIELDS, result=result, error=error, values=values)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
