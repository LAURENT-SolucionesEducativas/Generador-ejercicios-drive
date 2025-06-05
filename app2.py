import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Evaluación por DNI", page_icon="🧠")

# Clasificación por DNI
clasificacion_dni = {
    "12345678": "F",
    "87654321": "M",
    "11223344": "D",
    "44332211": "F",
}

# Cargar ejercicios desde Google Sheets
@st.cache_data
def cargar_ejercicios():
    url_csv = "https://docs.google.com/spreadsheets/d/1oLZCNVpCbPBQYKIrLEFxouqY5SujGy5H/export?format=csv"
    df = pd.read_csv(url_csv)
    return df[["Enunciado", "Respuesta", "Nivel"]]

df_ejercicios = cargar_ejercicios()

st.title("📘 Evaluación Automática por DNI")

dni = st.text_input("🔑 Ingresa tu DNI")

# Verifica que exista el DNI
if dni:
    nivel = clasificacion_dni.get(dni)
    if nivel:
        st.success(f"Estás clasificado en el nivel: **{nivel}**")

        # Si aún no se han asignado ejercicios
        if "ejercicios_asignados" not in st.session_state or st.session_state.get("dni_guardado") != dni:
            ejercicios_filtrados = df_ejercicios[df_ejercicios["Nivel"] == nivel]
            st.session_state.ejercicios_asignados = ejercicios_filtrados.sample(5).to_dict("records")
            st.session_state.respuestas = [""] * 5
            st.session_state.resultados_mostrados = False
            st.session_state.resultados = []
            st.session_state.aciertos = 0
            st.session_state.dni_guardado = dni

        ejercicios = st.session_state.ejercicios_asignados

        # Formulario
        with st.form("formulario"):
            for i, ejercicio in enumerate(ejercicios):
                st.session_state.respuestas[i] = st.text_input(
                    f"{i+1}. {ejercicio['Enunciado']}",
                    value=st.session_state.respuestas[i],
                    key=f"resp_{i}"
                )
            enviar = st.form_submit_button("📤 Enviar respuestas")

        if enviar:
            st.session_state.resultados = []
            aciertos = 0
            for i, (resp, ejercicio) in enumerate(zip(st.session_state.respuestas, ejercicios)):
                correcta = str(ejercicio["Respuesta"]).strip()
                if resp.strip() == correcta:
                    st.session_state.resultados.append((i+1, True, correcta))
                    aciertos += 1
                else:
                    st.session_state.resultados.append((i+1, False, correcta))
            st.session_state.aciertos = aciertos
            st.session_state.resultados_mostrados = True

        # Mostrar resultados solo si se presionó el botón
        if st.session_state.resultados_mostrados:
            for i, es_correcto, correcta in st.session_state.resultados:
                if es_correcto:
                    st.success(f"{i}. ✅ Correcto")
                else:
                    st.error(f"{i}. ❌ Incorrecto. Respuesta correcta: {correcta}")
            st.info(f"🔎 Puntaje final: {st.session_state.aciertos}/5")
    else:
        st.warning("❗ Este DNI no está clasificado por el profesor.")
else:
    st.info("Por favor, ingresa tu DNI para comenzar.")
