```markdown
# 📘 DOCUMENTATION COMPLETE – PROJET « TITANIC – SURVIVAL PREDICTOR »

---

## 1. PRÉSENTATION DU PROJET
**Objectif** : prédire la survie d’un passager du Titanic à partir de données socio-démographiques et de réservation.  
**Dataset** : `train.csv` & `test.csv` (OpenClassrooms / Kaggle – 891 passagers, 11 variables).  
**Output** : fichier `submission.csv` (PassengerId, Survived) + **API web** + **interface Streamlit**.

---

## 2. STRUCTURE DU REPOSITORY
```
Titanic/
│  main.py                 # API FastAPI
│  app.py                  # Interface Streamlit
│  titanic_pipeline.pkl    # Pipeline entraîné (One-Hot + RandomForest)
│  requirements.txt        # Librairies nécessaires
│  README.md               # Ce document
│  Dockerfile              # (optionnel) conteneurisation
└─ notebooks/
      titanic_eda.ipynb    # EDA + feature-engineering
```

---

## 3. ÉTAPES DU PROJET
| Étape | Outils / bibliothèques | Résultat |
|-------|------------------------|----------|
| **1. Nettoyage** | pandas, numpy | 0 NA dans Age/Embarked ; outliers conservés |
| **2. EDA** | matplotlib, seaborn, scipy | variables clés identifiées (Sex, Pclass, Fare, Title, etc.) |
| **3. Feature-engineering** | pandas, numpy | 6 nouvelles variables (Title, FamilySize, IsAlone, AgeBand, Fare_log, Sex_Pclass) |
| **4. Modélisation** | scikit-learn | Logistic Regression (80 %) → RandomForest GridSearch (85 %) |
| **5. Évaluation** | accuracy, ROC-AUC, matrice de confusion | Accuracy = 85 %, AUC = 0,91 |
| **6. Sauvegarde** | joblib | pipeline complet (One-Hot + RandomForest) |
| **7. API** | FastAPI | endpoint `/predict` → JSON (survived, probability) |
| **8. Interface web** | Streamlit | formulaire + bouton « Prédire » |
| **9. Conteneurisation** | Docker | image « titanic-app » (ports 8000 & 8501) |

---

## 4) INSTALLATION & LANCEMENT

### Prérequis
- Python ≥ 3.11
- pip

### Installation locale
```bash
git clone https://github.com/VOTRE_COMPTE/Titanic.git
cd Titanic
python -m pip install -r requirements.txt
```

### Lancement
```bash
# Terminal 1 – API
python -m uvicorn main:app --reload --port 8000

# Terminal 2 – Interface web
python -m streamlit run app.py --server.port 8501
```
- **API** : http://localhost:8000/docs  
- **Interface** : http://localhost:8501

---

## 5) UTILISATION

### a) Via l’interface web
1. Remplir le formulaire (classe, sexe, âge, etc.)  
2. Cliquer sur **Prédire**  
3. Lire **survie** (Oui/Non) et **probabilité**

### b) Via l’API (curl ou Swagger)
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"Pclass":1,"Sex":"female","Age":29.0,"SibSp":0,"Parch":0,"Fare":71.28,"Embarked":"C","Cabin":"C85","Name":"Your Name"}'
```
**Réponse**
```json
{"survived": 1, "probability": 0.97}
```

---

## 6) RÉSULTATS OBTENUS
| Modèle | Accuracy | ROC-AUC | Remarque |
|--------|----------|---------|----------|
| Logistic Regression | 80 % | 0,83 | baseline |
| RandomForest (tuned) | 85 % | 0,91 | meilleur modèle retenu |

---

## 7) FICHIERS IMPORTANTS
- `titanic_pipeline.pkl` → pipeline entraîné (à ne **pas modifier**)
- `requirements.txt` → liste des librairies
- `Dockerfile` → build & run partout

---

## 8) AMÉLIORATIONS POSSIBLES
- XGBoost / LightGBM / CatBoost  
- Stacking (RF + XGB + Logit)  
- SHAP pour interprétation fine  
- Déploiement cloud (Render, Railway, Fly.io)

---

## 9) AUTEUR
**Votre nom** – OpenClassrooms – Projet Data Scientist – 2024  
Contact : votre.email@example.com

---

**Enjoy your live Titanic predictor ! 🚢**
```