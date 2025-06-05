import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Evaluación por DNI", page_icon="🧠")

# Clasificación del alumno por DNI
clasificacion_dni = {
    "12345678": "Fácil",
    "87654321": "Medio",
    "11223344": "Difícil",
    "44332211": "Fácil",
}

# Leer ejercicios desde tu Google Sheet
sheet_id = "1oLZCNVpCbPBQYKIrLEFxouqY5SujGy5H"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(sheet_url)

    # Traducir niveles abreviados a nombres completos
    nivel_map = {"F": "Fácil", "M": "Medio", "D": "Difícil"}
    df["Nivel"] = df["Nivel"].map(nivel_map)

except Exception as e:
    st.error("❌ No se pudo cargar la base de datos. Verifica que el documento esté en modo público y tenga las columnas necesarias.")
    st.stop()

# Agrupar ejercicios por nivel
ejercicios_por_nivel = {
    nivel: df[df["Nivel"] == nivel].to_dict("records")
    for nivel in df["Nivel"].unique()
}

# Interfaz
st.title("📘 Evaluación Automática por DNI")
dni = st.text_input("🔑 Ingresa tu DNI")

# Evitar recargar preguntas al presionar Enter
if "ejercicios" not in st.session_state:
    st.session_state.ejercicios = []
    st.session_state.nivel = None

if dni:
    nivel = clasificacion_dni.get(dni)
    if nivel:
        st.success(f"Estás clasificado en el nivel: **{nivel}**")

        if not st.session_state.ejercicios or st.session_state.nivel != nivel:
            st.session_state.ejercicios = random.sample(
                ejercicios_por_nivel[nivel], 5
            )
            st.session_state.nivel = nivel

        with st.form(key="evaluacion"):
            respuestas_usuario = []
            for i, ejercicio in enumerate(st.session_state.ejercicios):
                respuesta = st.text_input(
                    f"{i+1}. {ejercicio['Enunciado']}", key=f"resp_{i}"
                )
                respuestas_usuario.append((respuesta, ejercicio["Respuesta"]))
            enviar = st.form_submit_button("📤 Enviar respuestas")

        if enviar:
            aciertos = 0
            for i, (user_resp, correcta) in enumerate(respuestas_usuario):
                if user_resp.strip() == str(correcta).strip():
                    st.success(f"{i+1}. ✅ Correcto")
                    aciertos += 1
                else:
                    st.error(f"{i+1}. ❌ Incorrecto. Respuesta correcta: {correcta}")
            st.info(f"🔎 Puntaje final: {aciertos}/5")
    else:
        st.warning("❗ Este DNI no está clasificado por el profesor.")
else:
    st.info("Por favor, ingresa tu DNI para comenzar.")
