import json
from datetime import datetime
import streamlit as st
import pandas as pd
from modules.inputs import seccion_mision, seccion_oei, seccion_aei, seccion_ruta_estrategica, seccion_anexo_b1, seccion_anexo_b2, seccion_anexo_b3
from modules.word_generator import generar_pei_word
from modules.db import guardar_pei_en_bd, cargar_pei_desde_bd

# ✅ Verificar que DATABASE_URL existe en los secretos (sin mostrar la clave)
if "SUPABASE_URL" in st.secrets:
    st.success("🔒 Se detectó correctamente la clave DATABASE_URL en los secretos de Streamlit.")
else:
    st.error("❌ No se encontró DATABASE_URL en los secretos. Verifica en Edit secrets.")
st.set_page_config(page_title="Generador PEI Municipal", layout="wide")
st.title("📘 Generador del Plan Estratégico Institucional (PEI)")
st.write("Aplicación para municipalidades provinciales y distritales del Perú.")
st.write("Esta herramienta considera lo establecido en la Guía para el Planeamiento Institucional, actualizada por Resolución de Presidencia de Consejo Directivo N°0055-2024-CEPLAN/PCD.")

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

# ============================================================
# 📂 CARGAR AVANCE ANTERIOR (ANTES DE LAS SECCIONES)
# ============================================================
if "codigo_ingresado" in locals() and codigo_ingresado:
    if st.button("📂 Cargar avance anterior"):
        try:
            registro = cargar_pei_desde_bd(str(codigo_ingresado).strip())

            if registro:
                st.success(f"✅ Avance cargado (última actualización: {registro['fecha_actualizacion']})")

                # 🧠 Guardar en sesión para persistencia
                st.session_state["pei_registro"] = registro

                # Rellenar campos visibles
                st.session_state["mision_texto"] = registro["mision"]

                st.session_state["oei_json"] = pd.DataFrame(registro["oei_json"]) if registro["oei_json"] else pd.DataFrame()
                st.session_state["aei_json"] = pd.DataFrame(registro["aei_json"]) if registro["aei_json"] else pd.DataFrame()
                st.session_state["ruta_json"] = pd.DataFrame(registro["ruta_json"]) if registro["ruta_json"] else pd.DataFrame()
                st.session_state["anexo_b2_json"] = pd.DataFrame(registro["anexo_b2_json"]) if registro["anexo_b2_json"] else pd.DataFrame()
                st.session_state["anexos_json"] = registro["anexos_json"]

                st.info("Los campos se han precargado con la información guardada.")
            else:
                st.warning("No hay avances guardados aún para esta municipalidad.")
        except Exception as e:
            st.error(f"❌ Error al cargar el avance: {e}")
else:
    st.warning("⚠️ Selecciona primero una municipalidad para poder cargar su avance.")

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

st.header(" Anexos B-1")
anexos = seccion_anexo_b1()

st.header(" Anexo B-2: Vinculación con Políticas Nacionales")

RUTA_ANEXO_B2 = "data/anexo_b2_politicas.xlsx"
anexo_b2_df = seccion_anexo_b2(aei_seleccionadas, RUTA_ANEXO_B2)

st.header(" Anexos B-3")
anexos = seccion_anexo_b3()

# ============================================================
# 💾 GUARDAR AVANCE (DESPUÉS DE LAS SECCIONES)
# ============================================================
if "codigo_ingresado" in locals() and codigo_ingresado:
    if st.button("💾 Grabar avance"):
        try:
            data = {
                "codigo_pliego": str(codigo_ingresado).strip(),
                "mision": mision,
                "oei_json": oei_seleccionados.to_dict(orient="records") if not oei_seleccionados.empty else [],
                "aei_json": aei_seleccionadas.to_dict(orient="records") if not aei_seleccionadas.empty else [],
                "ruta_json": ruta_estrategica_df.to_dict(orient="records") if not ruta_estrategica_df.empty else [],
                "anexo_b2_json": anexo_b2_df.to_dict(orient="records") if not anexo_b2_df.empty else [],
                "anexos_json": anexos,
            }

            guardar_pei_en_bd(data)
            st.success("✅ Avance del PEI guardado correctamente en Supabase.")
        except Exception as e:
            st.error(f"❌ Error al guardar el avance: {e}")
else:
    st.warning("⚠️ Selecciona primero una municipalidad para grabar su avance.")

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
