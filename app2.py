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

if dni:
    nivel = clasificacion_dni.get(dni)
    if nivel:
        st.success(f"Estás clasificado en el nivel: **{nivel}**")

        # Solo cargar ejercicios una vez por DNI
        if "dni_actual" not in st.session_state or st.session_state.dni_actual != dni:
            ejercicios_nivel = df_ejercicios[df_ejercicios["Nivel"] == nivel]
            st.session_state.ejercicios = ejercicios_nivel.sample(5).to_dict("records")
            st.session_state.respuestas = [""] * 5
            st.session_state.resultados = []
            st.session_state.mostrar_resultados = False
            st.session_state.dni_actual = dni

        # Mostrar preguntas
        with st.form("evaluacion_form"):
            for i, ejercicio in enumerate(st.session_state.ejercicios):
                st.session_state.respuestas[i] = st.text_input(
                    f"{i+1}. {ejercicio['Enunciado']}",
                    value=st.session_state.respuestas[i],
                    key=f"input_{i}"
                )
            enviar = st.form_submit_button("📤 Enviar respuestas")

        if enviar:
            resultados = []
            aciertos = 0
            for i, (resp, ejercicio) in enumerate(zip(st.session_state.respuestas, st.session_state.ejercicios)):
                correcta = str(ejercicio["Respuesta"]).strip()
                if resp.strip() == correcta:
                    resultados.append((i + 1, True, correcta))
                    aciertos += 1
                else:
                    resultados.append((i + 1, False, correcta))
            st.session_state.resultados = resultados
            st.session_state.aciertos = aciertos
            st.session_state.mostrar_resultados = True

        # Mostrar resultados solo después del botón
        if st.session_state.mostrar_resultados:
            for i, correcto, correcta in st.session_state.resultados:
                if correcto:
                    st.success(f"{i}. ✅ Correcto")
                else:
                    st.error(f"{i}. ❌ Incorrecto. Respuesta correcta: {correcta}")
            st.info(f"🔎 Puntaje final: {st.session_state.aciertos}/5")
    else:
        st.warning("❗ Este DNI no está clasificado por el profesor.")
else:
    st.info("Por favor, ingresa tu DNI para comenzar.")
