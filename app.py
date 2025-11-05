import streamlit as st
import pandas as pd
from modules.inputs import seccion_mision, seccion_oei, seccion_aei, seccion_ruta_estrategica, seccion_anexos
from modules.word_generator import generar_pei_word

st.set_page_config(page_title="Generador PEI Municipal", layout="wide")
st.title("📘 Generador de Plan Estratégico Institucional (PEI)")
st.write("Aplicación para municipalidades provinciales y distritales del Perú.")

# Información inicial
tipo = st.selectbox("Tipo de municipalidad", ["Provincial", "Distrital"])
nombre = st.text_input("Nombre de la municipalidad", value="Nombre Municipalidad")

st.markdown("""---
## Completa las secciones del PEI
""")

# Secciones
st.header("1️⃣ Misión")
mision = seccion_mision()

st.header("2️⃣ Objetivos Estratégicos Institucionales (OEI)")
oei_df = seccion_oei()

st.header("3️⃣ Acciones Estratégicas Institucionales (AEI)")
aei_df = seccion_aei()

st.header("4️⃣ Ruta Estratégica")
ruta = seccion_ruta_estrategica()

st.header("5️⃣ Anexos B-1, B-2 y B-3")
anexos = seccion_anexos()

if st.button("📝 Generar documento Word"):
    with st.spinner("Generando PEI..."):
        archivo_bytes = generar_pei_word(nombre, tipo, mision, oei_df, aei_df, ruta, anexos)
        st.success("✅ PEI generado correctamente.")
        st.download_button("Descargar PEI", data=archivo_bytes, file_name=f"PEI_{nombre}.docx", mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
