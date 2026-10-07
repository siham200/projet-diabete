# Projet : Prédiction du diabète (Pipeline → Pickle → FastAPI → Flask)

## Structure
```
projet_diabete/
├── notebook/projet_diabete.ipynb   # À ouvrir dans Google Colab
├── data/diabetes.csv               # Dataset Pima Indians Diabetes
├── model/diabetes_pipeline.pkl     # Pipeline sérialisé (prétraitement + modèle)
├── api/main.py                     # API FastAPI (charge le pkl)
├── web/app.py                      # Interface Flask (appelle FastAPI)
├── web/templates/index.html
└── requirements.txt
```

## Lancer en local
```bash
pip install -r requirements.txt

# Terminal 1 : API FastAPI (docs : http://127.0.0.1:8000/docs)
uvicorn api.main:app --port 8000 --reload

# Terminal 2 : interface Flask  -> http://127.0.0.1:5000
python web/app.py
```
Si l'API est sur une autre adresse : `API_URL=http://hote:8000/predict python web/app.py`

## Lancer dans Colab
Ouvrir `notebook/projet_diabete.ipynb` > Exécuter tout. Le notebook entraîne, sauvegarde le .pkl,
lance FastAPI et Flask (affiché dans une iframe) puis permet de télécharger le zip.

## Remarque
Le .pkl dépend de la version de scikit-learn : utilisez la même version pour entraîner et servir
(ou ré-exécutez le notebook pour regénérer le .pkl).
