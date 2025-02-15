import streamlit as st
import os
from mistralai import Mistral
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv('.env.local')  # Charge spécifiquement le fichier .env.local
api_key = os.getenv("MISTRAL_API_KEY")

st.title("🩺 Health Biomarker Analyzer")

# Vérification de la clé API
if not api_key:
    st.error("Clé API non trouvée dans .env.local - Ajoutez MISTRAL_API_KEY")
    st.stop()

# Configuration modèle dans la sidebar
with st.sidebar:
    st.header("Configuration")
    model_choice = st.selectbox(
        "Modèle",
        ["mistral-large-latest", "mistral-medium-latest", "open-mistral-7b"],
        index=0
    )

# Formulaire biomarqueurs
with st.form("biomarker_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Âge", min_value=0, max_value=120)
        weight = st.number_input("Poids (kg)", min_value=30.0)
        height = st.number_input("Taille (cm)", min_value=100.0)
        systolic = st.number_input("Pression artérielle systolique", min_value=50)
        diastolic = st.number_input("Pression artérielle diastolique", min_value=30)

    with col2:
        glucose = st.number_input("Glucose sanguin (mg/dL)", min_value=50.0)
        cholesterol = st.number_input("Cholestérol total (mg/dL)", min_value=50.0)
        hdl = st.number_input("HDL (mg/dL)", min_value=20.0)
        ldl = st.number_input("LDL (mg/dL)", min_value=20.0)
        creatinine = st.number_input("Créatinine sérique (mg/dL)", min_value=0.1)

    submitted = st.form_submit_button("Analyser les résultats 🔍")

if submitted:
    client = Mistral(api_key=api_key)
    
    prompt = f"""Analyse médicale pour :
    - Âge : {age} ans
    - Poids : {weight} kg
    - Taille : {height} cm
    - Tension : {systolic}/{diastolic} mmHg
    - Glucose : {glucose} mg/dL
    - Cholestérol total : {cholesterol} mg/dL
    - HDL : {hdl} mg/dL
    - LDL : {ldl} mg/dL
    - Créatinine : {creatinine} mg/dL

    Rédigez un rapport avec :
    1. Évaluation des risques
    2. Recommandations personnalisées
    3. Comparaison avec les normes médicales
    """

    try:
        with st.spinner("Génération du rapport..."):
            response = client.chat.complete(
                model=model_choice,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            st.subheader("📋 Rapport d'analyse médicale")
            st.markdown(response.choices[0].message.content)
            
    except Exception as e:
        st.error(f"Erreur de connexion à l'API: {str(e)}")