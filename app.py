import streamlit as st
import pandas as pd
from modules.inputs import seccion_mision, seccion_oei, seccion_aei, seccion_ruta_estrategica, seccion_anexos, seccion_anexo_b2
from modules.word_generator import generar_pei_word

st.set_page_config(page_title="Generador PEI Municipal", layout="wide")
st.title("📘 Generador del Plan Estratégico Institucional (PEI)")
st.write("Aplicación para municipalidades provinciales y distritales del Perú.")

# =====================================
# 🏛️ Información inicial desde pliegos.xlsx
# =====================================
@st.cache_data
def cargar_pliegos():
    return pd.read_excel("data/pliegos.xlsx", engine="openpyxl")

df_pliegos = cargar_pliegos()

st.subheader("🏛️ Información de la Municipalidad")

# Crear opciones combinadas para búsqueda
opciones = [
    f"{str(row['Codigo_Pliego'])} - {row['Nombre_Municipalidad']}"
    for _, row in df_pliegos.iterrows()
]

# Selectbox con búsqueda tanto por código como por nombre
opcion_seleccionada = st.selectbox(
    "🔍 Selecciona o escribe el código o nombre del pliego",
    opciones,
    index=None,
    placeholder="Escribe el código o nombre..."
)

# Mostrar información cuando el usuario selecciona un pliego

if opcion_seleccionada:
    # Extraer código
    codigo_ingresado = opcion_seleccionada.split(" - ")[0].strip()

    # Obtener datos del pliego seleccionado
    datos = df_pliegos[df_pliegos["Codigo_Pliego"].astype(str) == codigo_ingresado].iloc[0]

    # Mostrar información formateada
    #st.markdown("### 🏛️ Información del Pliego Seleccionado")
    st.markdown(f"""
    **Nombre de la Municipalidad:** {datos['Nombre_Municipalidad']}  
    **Tipo:** {datos['Tipo']}  
    **Departamento:** {datos['Departamento']}  
    **Provincia:** {datos['Provincia']}  
    **Distrito:** {datos['Distrito']}  
    """)

    tipo = datos["Tipo"]
    nombre = datos["Nombre_Municipalidad"]
else:
    st.info("Por favor, selecciona un pliego para continuar.")
    
st.markdown("---")
st.markdown("## Completa las secciones del PEI")

# =====================================
# Secciones del PEI
# =====================================
st.header("1️⃣ Misión")
mision = seccion_mision()

st.header("2️⃣ Objetivos Estratégicos Institucionales (OEI)")
#oei_df = seccion_oei()
oei_seleccionados = seccion_oei()

st.header("3️⃣ Acciones Estratégicas Institucionales (AEI)")
#aei_df = seccion_aei(oei_df)
aei_seleccionadas = seccion_aei(oei_seleccionados)

st.header("4️⃣ Ruta Estratégica: Vinculación con la PGG")
# Ruta al archivo Excel de vinculación
RUTA_VINCULACION_PGG = "data/vinculacion_pgg.xlsx"

# Ejecutar sección
#ruta = seccion_ruta_estrategica()
ruta_estrategica_df = seccion_ruta_estrategica(
    oei_seleccionados,
    aei_seleccionadas,
    RUTA_VINCULACION_PGG
)

st.header(" Anexos B-1, B-2 y B-3")
anexos = seccion_anexos()

st.header(" Anexo B-2: Vinculación con Políticas Nacionales")

RUTA_ANEXO_B2 = "data/anexo_b2_politicas.xlsx"
anexo_b2_df = seccion_anexo_b2(aei_seleccionadas, RUTA_ANEXO_B2)

if st.button("📝 Generar documento Word"):
    with st.spinner("Generando PEI..."):
        #archivo_bytes = generar_pei_word(nombre, tipo, mision, oei_seleccionados, aei_seleccionadas, ruta, anexos)
        word_bytes = generar_pei_word(
            nombre_muni=nombre,
            tipo=tipo,
            mision=mision,
            oei_df=oei_seleccionados,
            aei_df=aei_seleccionadas,
            ruta_df=ruta_estrategica_df,
            anexo_b2_df=anexo_b2_df,
        )
        st.success("✅ PEI generado correctamente.")
        st.download_button("Descargar PEI", data=word_bytes, file_name=f"PEI_{nombre}.docx", mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
