from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

app = FastAPI(title="Titanic Survival Predictor", version="1.0")

# Chargement du pipeline (One-Hot + RandomForest)
pipeline = joblib.load("titanic_pipeline.pkl")

# Schéma des données d'entrée
class Passenger(BaseModel):
    Pclass: int
    Sex: str
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: str
    Cabin: str = None
    Name: str = "Inconnu"
    Ticket: str = "Inconnu"

@app.post("/predict")
def predict(passenger: Passenger):
    try:
        # Conversion en DataFrame (1 ligne)
        df = pd.DataFrame([passenger.dict()])
        # Application du même feature-engineering que durant l’entraînement
        df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
        title_map = {'Mr':'Mr', 'Miss':'Miss', 'Mrs':'Mrs', 'Master':'Master', 'Dr':'Rare', 'Rev':'Rare', 'Col':'Rare', 'Major':'Rare', 'Mlle':'Miss', 'Ms':'Miss', 'Mme':'Mrs', 'Don':'Rare', 'Dona':'Rare', 'Lady':'Rare', 'Countess':'Rare', 'Jonkheer':'Rare', 'Sir':'Rare', 'Capt':'Rare'}
        df['Title'] = df['Title'].map(title_map).fillna('Rare')
        df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
        df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
        df['AgeBand'] = pd.cut(df['Age'], bins=[0, 16, 60, 100], labels=['Child', 'Adult', 'Senior'])
        df['Fare_log'] = np.log1p(df['Fare'])
        df['HasCabin'] = df['Cabin'].notna().astype(int)
        df['CabinLetter'] = df['Cabin'].str[0].fillna('No')
        df['Sex_Pclass'] = df['Sex'].map({'male':0, 'female':1}).astype(str) + df['Pclass'].astype(str)

        # On retire les colonnes non utilisées par le modèle
        X = df.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1, errors='ignore')

        # Prédiction
        proba = pipeline.predict_proba(X)[0, 1]   # proba de survie
        survie = int(pipeline.predict(X)[0])      # 0 ou 1

        return {"survived": survie, "probability": round(float(proba), 3)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))