import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Evaluación por DNI", page_icon="🧠")
# Cabecera institucional
st.markdown("""
<h1 style='text-align: center; color: #2c3e50;'>Consorcio Educativo LAURENT</h1>
""", unsafe_allow_html=True)

# Clasificación por DNI
clasificacion_dni = {
    "12345678": "F",
    "87654321": "M",
    "46850511": "D",
    "44332211": "F",
}

# Nombres asociados al DNI
nombres_dni = {
    "12345678": "Lucía Martínez",
    "87654321": "Carlos G. Suárez",
    "46850511": "Ana T. Rodríguez",
    "44332211": "Luis M. Vargas",
}

# Cargar ejercicios desde Google Sheets
@st.cache_data
def cargar_ejercicios():
    url_csv = "https://docs.google.com/spreadsheets/d/1oLZCNVpCbPBQYKIrLEFxouqY5SujGy5H/export?format=csv"
    df = pd.read_csv(url_csv)
    return df[["Enunciado", "Respuesta", "Nivel"]]

df_ejercicios = cargar_ejercicios()

st.title("📘 Practicando en casa - R.M")

dni = st.text_input("🔑 Ingresa tu DNI")

if dni:
    nivel = clasificacion_dni.get(dni)
    nombre_completo = nombres_dni.get(dni, "Alumno desconocido")

    if nivel:
        st.success(f"👤 Bienvenido/a: **{nombre_completo}**")
        st.success(f"📘 Estás clasificado en el nivel: **{nivel}**")

        if "dni_actual" not in st.session_state or st.session_state.dni_actual != dni:
            ejercicios_nivel = df_ejercicios[df_ejercicios["Nivel"] == nivel]
            st.session_state.ejercicios = ejercicios_nivel.sample(5).to_dict("records")
            st.session_state.respuestas = [""] * 5
            st.session_state.resultados = []
            st.session_state.aciertos = 0
            st.session_state.mostrar_resultados = False
            st.session_state.dni_actual = dni

        st.subheader("📝 Responde las siguientes preguntas:")

        for i, ejercicio in enumerate(st.session_state.ejercicios):
            st.session_state.respuestas[i] = st.text_input(
                f"{i+1}. {ejercicio['Enunciado']}",
                value=st.session_state.respuestas[i],
                key=f"input_{i}"
            )

        if st.button("📤 Enviar respuestas"):
            resultados = []
            aciertos = 0
            for i, (resp, ejercicio) in enumerate(zip(st.session_state.respuestas, st.session_state.ejercicios)):
                correcta = str(ejercicio["Respuesta"]).strip()
                if resp.strip().lower() == correcta.lower():
                    resultados.append((i + 1, True, correcta))
                    aciertos += 1
                else:
                    resultados.append((i + 1, False, correcta))
            st.session_state.resultados = resultados
            st.session_state.aciertos = aciertos
            st.session_state.mostrar_resultados = True

        if st.session_state.mostrar_resultados:
            st.subheader("📊 Resultados:")
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
