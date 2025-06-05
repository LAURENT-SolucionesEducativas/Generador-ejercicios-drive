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
    try:
        df = pd.read_csv(url_csv)
        df = df[["Enunciado", "Respuesta", "Nivel"]]
        return df
    except Exception as e:
        st.error("❌ No se pudo cargar la base de datos.")
        return pd.DataFrame()

df_ejercicios = cargar_ejercicios()

# Interfaz
st.title("📘 Evaluación Automática por DNI")
dni = st.text_input("🔑 Ingresa tu DNI")

if dni:
    nivel = clasificacion_dni.get(dni)
    if nivel:
        st.success(f"Estás clasificado en el nivel: **{nivel}**")

        # Guardar ejercicios solo una vez
        if "ejercicios_asignados" not in st.session_state:
            ejercicios_filtrados = df_ejercicios[df_ejercicios["Nivel"] == nivel]
            st.session_state.ejercicios_asignados = ejercicios_filtrados.sample(5).to_dict("records")
            st.session_state.respuestas = [""] * 5
            st.session_state.resultados_mostrados = False

        ejercicios = st.session_state.ejercicios_asignados

        # Formulario de respuestas
        with st.form("formulario_evaluacion"):
            for i, ejercicio in enumerate(ejercicios):
                st.session_state.respuestas[i] = st.text_input(
                    f"{i+1}. {ejercicio['Enunciado']}",
                    key=f"respuesta_{i}",
                    value=st.session_state.respuestas[i]
                )

            enviar = st.form_submit_button("📤 Enviar respuestas")

        # Procesar resultados SOLO cuando se envía el formulario
        if enviar:
            st.session_state.resultados_mostrados = True
            st.session_state.resultados = []
            aciertos = 0

            for i, (respuesta, ejercicio) in enumerate(zip(st.session_state.respuestas, ejercicios)):
                correcta = str(ejercicio["Respuesta"]).strip()
                if respuesta.strip() == correcta:
                    st.session_state.resultados.append((i+1, True, correcta))
                    aciertos += 1
                else:
                    st.session_state.resultados.append((i+1, False, correcta))

            st.session_state.aciertos = aciertos

        # Mostrar resultados SOLO si se presionó "Enviar respuestas"
        if st.session_state.get("resultados_mostrados", False):
            for num, es_correcto, correcta in st.session_state.resultados:
                if es_correcto:
                    st.success(f"{num}. ✅ Correcto")
                else:
                    st.error(f"{num}. ❌ Incorrecto. Respuesta correcta: {correcta}")
            st.info(f"🔎 Puntaje final: {st.session_state.aciertos}/5")

    else:
        st.warning("❗ Este DNI no está clasificado por el profesor.")
else:
    st.info("Por favor, ingresa tu DNI para comenzar.")
