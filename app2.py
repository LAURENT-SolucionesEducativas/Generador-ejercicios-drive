import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Evaluación por DNI", page_icon="🧠")

# 1. Clasificación por DNI
clasificacion_dni = {
    "12345678": "F",
    "87654321": "M",
    "11223344": "D",
    "44332211": "F",
    # Agrega más DNIs
}

# 2. Cargar ejercicios desde Google Sheets
@st.cache_data
def cargar_ejercicios():
    url_csv = "https://docs.google.com/spreadsheets/d/1oLZCNVpCbPBQYKIrLEFxouqY5SujGy5H/export?format=csv"
    try:
        df = pd.read_csv(url_csv)
        df = df[["Enunciado", "Respuesta", "Nivel"]]  # Validar columnas
        return df
    except Exception as e:
        st.error("❌ No se pudo cargar la base de datos. Verifica que el enlace esté en modo público.")
        return pd.DataFrame()

df_ejercicios = cargar_ejercicios()

# 3. Interfaz
st.title("📘 Evaluación Automática por DNI")
dni = st.text_input("🔑 Ingresa tu DNI")

if dni:
    nivel = clasificacion_dni.get(dni)
    if nivel:
        st.success(f"Estás clasificado en el nivel: **{nivel}**")

        # Guardar ejercicios en session_state para evitar cambios con cada recarga
        if "ejercicios_asignados" not in st.session_state:
            ejercicios_filtrados = df_ejercicios[df_ejercicios["Nivel"] == nivel].sample(5).to_dict("records")
            st.session_state.ejercicios_asignados = ejercicios_filtrados

        ejercicios = st.session_state.ejercicios_asignados

        with st.form("form_evaluacion"):
            respuestas_usuario = []
            for i, ejercicio in enumerate(ejercicios):
                resp = st.text_input(f"{i+1}. {ejercicio['Enunciado']}", key=f"resp_{i}")
                respuestas_usuario.append(resp)
            enviar = st.form_submit_button("📤 Enviar respuestas")

        if enviar:
            aciertos = 0
            for i, (user_resp, ejercicio) in enumerate(zip(respuestas_usuario, ejercicios)):
                correcta = str(ejercicio["Respuesta"]).strip()
                if user_resp.strip() == correcta:
                    st.success(f"{i+1}. ✅ Correcto")
                    aciertos += 1
                else:
                    st.error(f"{i+1}. ❌ Incorrecto. Respuesta correcta: {correcta}")
            st.info(f"🔎 Puntaje final: {aciertos}/5")

    else:
        st.warning("❗ Este DNI no está clasificado por el profesor.")
else:
    st.info("Por favor, ingresa tu DNI para comenzar.")
