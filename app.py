import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Titanic Survival Predictor", layout="centered")

st.title("🚢 Prédicteur de survie – Titanic")
st.markdown("Remplissez le formulaire ci-dessous et cliquez sur **Prédire**.")

# ---- Formulaire ----
with st.form("formulaire"):
    pclass = st.selectbox("Classe", [1, 2, 3])
    sex = st.radio("Sexe", ["male", "female"])
    age = st.slider("Âge", 0, 80, 30)
    sibsp = st.number_input("Frères/soeurs à bord", 0, 10, 0)
    parch = st.number_input("Parents/enfants à bord", 0, 10, 0)
    fare = st.number_input("Prix du billet (Fare)", 0.0, 600.0, 30.0)
    embarked = st.selectbox("Port d’embarquement", ["C", "Q", "S"])
    cabin = st.text_input("Cabine (optionnel)", "")
    name = st.text_input("Nom (optionnel)", "Inconnu")
    submitted = st.form_submit_button("Prédire")

if submitted:
    json_data = {
        "Pclass": pclass, "Sex": sex, "Age": age,
        "SibSp": sibsp, "Parch": parch, "Fare": fare,
        "Embarked": embarked, "Cabin": cabin, "Name": name
    }
    response = requests.post("http://127.0.0.1:8000/predict", json=json_data)
    if response.status_code == 200:
        result = response.json()
        st.success(f"Survie estimée : **{'Oui' if result['survived'] else 'Non'}** (probabilité : {result['probability']})")
    else:
        st.error(f"Erreur : {response.text}")