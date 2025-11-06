import streamlit as st
import pandas as pd
from io import StringIO

#def seccion_mision():
    #mision = st.text_area("Misión (texto)", height=120, placeholder="Escribe la misión de la municipalidad...")
    #return mision
def seccion_mision():
    """
    Despliega la sección de Misión con guía y ejemplos predefinidos.
    """
    st.markdown("### 🧭 Misión Institucional")
    st.info("**Estructura de redacción:** Rol central de la entidad + Población beneficiaria + Atributos.")

    ejemplos = [
        "Prestar servicios básicos a los vecinos de la localidad, garantizando calidad, eficiencia y oportunidad en su provisión.",
        "Proveer servicios públicos esenciales a la población de la localidad, priorizando cobertura universal, equidad y atención inclusiva.",
        "Brindar servicios básicos a los habitantes de la localidad, promoviendo sostenibilidad, responsabilidad ambiental y uso racional de recursos.",
        "Ofrecer servicios públicos esenciales a los vecinos de la localidad, integrando innovación tecnológica, mejora continua y atención personalizada",
        "Garantizar servicios básicos para la población de la localidad, asegurando continuidad, seguridad y respuesta rápida.",
        "Desarrollar servicios públicos esenciales para los habitantes de la localidad, fomentando eficiencia operativa, transparencia y participación ciudadana.",
        "Suministrar servicios básicos a la población de la localidad, optimizando recursos, reduciendo brechas y mejorando la accesibilidad.",
        "Administrar servicios públicos esenciales para los vecinos de la localidad, fortaleciendo gestión participativa, control social y corresponsabilidad.",
        "Proporcionar servicios básicos a los habitantes de la localidad, priorizando bienestar social, inclusión y equidad territorial.",
        "Asegurar servicios públicos esenciales a la población de la localidad, incorporando estándares de calidad, modernización y sostenibilidad.",
        "Brindar servicios públicos orientadas al bienestar de la población, mediante una gestión sostenible, ética, inclusiva y transparente."
    ]

    opcion = st.selectbox("Selecciona un ejemplo de misión (opcional)", [""] + ejemplos)
    mision_texto = st.text_area("✍️ Redacta o ajusta la misión de la municipalidad:", value=opcion, height=150)

    return mision_texto

def _editar_tabla_interna(default_columns, default_rows=3, key=None):
    # Usa st.experimental_data_editor si está disponible, de lo contrario usa textarea CSV
    try:
        df = st.experimental_data_editor(pd.DataFrame([""], columns=["_dummy"]).drop(columns=["_dummy"]), num_rows="fixed", key=key)
    except Exception:
        # Fallback: textarea con CSV simple
        csv = st.text_area("Ingresa filas separadas por nueva línea (cada columna separada por ;)", height=120, key=(key or 'csv'))
        if csv:
            rows = [r.split(";") for r in csv.splitlines() if r.strip()]
            if rows:
                maxcols = max(len(r) for r in rows)
                cols = [f"col{i+1}" for i in range(maxcols)]
                df = pd.DataFrame(rows, columns=cols)
            else:
                df = pd.DataFrame(columns=cols)
        else:
            df = pd.DataFrame()
    return df

# =====================================================
# 🎯 OEI (Objetivos Estratégicos Institucionales)
# =====================================================
def seccion_oei():
    st.markdown("### 🎯 Objetivos Estratégicos Institucionales (OEI)")

    # Dataset base con 11 OEI (ejemplo)
    oei_data = pd.DataFrame({
        #"Código": [f"OEI{i:02d}" for i in range(1, 12)],
        #"Denominación": [
        {"Código": "OEI.01", "Denominación": "Promover el ordenamiento territorial en beneficio de población local", "Nombre del Indicador": "Porcentaje de la población local que reside en zonas que cumplen con los instrumentos técnicos sustentatorios para el ordenamiento territorial"},
        {"Código": "OEI.02", "Denominación": "Fortalecer el acceso a la atención primaria de salud preventiva de la población local", "Nombre del Indicador": "Porcentaje de personas satisfechas con las campañas y actividades de promoción de salud realizadas por la municipalidad"},
        {"Código": "OEI.03", "Denominación": "Promover el acceso a servicios educativos, deportivos y recreacionales con enfoque intercultural e inclusivo para la población local", "Nombre del Indicador": "Porcentaje de participantes satisfechos con los programas educativos organizados por la municipalidad"},
        {"Código": "OEI.04", "Denominación": "Promover condiciones ambientales saludables y sostenibles para la población local", "Nombre del Indicador": "Porcentaje de ciudadanos satisfechos con el servicio de recojo de residuos sólidos"},
        {"Código": "OEI.04", "Denominación": "Promover condiciones ambientales saludables y sostenibles para la población local", "Nombre del Indicador": "Porcentaje de zonas de la localidad donde se han reducido puntos críticos de contaminación"},
        {"Código": "OEI.05", "Denominación": "Reducir la exposición al riesgo de desastres de origen natural o antrópico de la población local", "Nombre del Indicador": "Porcentaje de zonas de la localidad con factores de riesgo de desastres eliminados o minimizados"},
        {"Código": "OEI.06", "Denominación": "Mejorar el acceso a servicios de protección social y defensa de derechos de la población en situación de vulnerabilidad de la localidad", "Nombre del Indicador": "Porcentaje de la población en situación de vulnerabilidad atendida por programas sociales municipales"},
        {"Código": "OEI.07", "Denominación": "Fortalecer la prevención y disuasión del delito y violencia en beneficio de la población local", "Nombre del Indicador": "Porcentaje de zonas con alta incidencia delictiva con servicio de patrullaje integrado"},
        {"Código": "OEI.08", "Denominación": "Garantizar la provisión de los servicios de agua potable y saneamiento en beneficio de la población local", "Nombre del Indicador": "Porcentaje de viviendas con servicio de agua potable y alcantarillado"},
        {"Código": "OEI.09", "Denominación": "Impulsar el crecimiento de la actividad empresarial, de emprendimientos y MYPES en la localidad", "Nombre del Indicador": "Porcentaje de micro y pequeñas empresas que operan con licencias municipales adecuadas"},
        {"Código": "OEI.10", "Denominación": "Mejorar el sistema de transporte y transitabilidad en beneficio de la población local", "Nombre del Indicador": "Porcentaje de puntos críticos de tránsito en vías locales atendidos y mitigados"},
        {"Código": "OEI.11", "Denominación": "Modernizar la Gestión Institucional", "Nombre del Indicador": "Porcentaje de ciudadanos satisfechos con la gestión institucional de la municipalidad"}
        })

    seleccionados = st.multiselect(
        "Selecciona uno o más OEI:",
        options=oei_data.apply(lambda r: f"{r['Código']} - {r['Denominación']}", axis=1).tolist()
    )

    if seleccionados:
        # extraer códigos seleccionados
        codigos = [s.split(' - ')[0] for s in seleccionados]
        df_sel = oei_data[oei_data["Código"].isin(codigos)][["Código","Denominación","Nombre del Indicador"]]
        st.dataframe(df_sel.reset_index(drop=True), hide_index=True, use_container_width=True)
        return df_sel
    else:
        st.warning("Selecciona al menos un OEI para continuar.")
        return pd.DataFrame(columns=["Código","Denominación","Nombre del Indicador"])


# =====================================================
# 🧩 AEI (Acciones Estratégicas Institucionales)
# =====================================================
@st.cache_data
def cargar_aei_excel(path='data/aei.xlsx'):
    try:
        return pd.read_excel(path, engine='openpyxl')
    except Exception as e:
        st.error(f"No se pudo cargar data/aei.xlsx: {e}")
        return pd.DataFrame(columns=["Código OEI","Código AEI","Denominación","Nombre del Indicador"])

def seccion_aei(oei_seleccionados):
    st.markdown("### 🧩 Acciones Estratégicas Institucionales (AEI)")

    if oei_seleccionados is None or oei_seleccionados.empty:
        st.info("Primero selecciona al menos un OEI para ver las AEI disponibles.")
        return pd.DataFrame(columns=["Código OEI","Código AEI","Denominación","Nombre del Indicador"])

    aei_base = cargar_aei_excel()

    # Filtrar AEI por los códigos OEI seleccionados
    codigos_oei = oei_seleccionados["Código"].astype(str).tolist()
    aei_filtrado = aei_base[aei_base["Código OEI"].isin(codigos_oei)][["Código OEI","Código AEI","Denominación","Nombre del Indicador"]]

    if aei_filtrado.empty:
        st.warning("No se encontraron AEI para los OEI seleccionados en data/aei.xlsx.")
        return pd.DataFrame(columns=["Código OEI","Código AEI","Denominación","Nombre del Indicador"])

    # Para cada OEI mostrar las AEI disponibles y permitir seleccionar
    seleccionadas_list = []
    for codigo in codigos_oei:
        subset = aei_filtrado[aei_filtrado["Código OEI"] == codigo]
        opciones = subset.apply(lambda r: f"{r['Código AEI']} - {r['Denominación']}", axis=1).tolist()
        seleccion = st.multiselect(f"Selecciona AEI para {codigo}", options=opciones, key=f"aei_{codigo}")
        seleccionadas_list.extend(seleccion)

    if seleccionadas_list:
        codigos_aei_sel = [s.split(' - ')[0] for s in seleccionadas_list]
        df_sel = aei_filtrado[aei_filtrado["Código AEI"].isin(codigos_aei_sel)][["Código OEI","Código AEI","Denominación","Nombre del Indicador"]]
        st.dataframe(df_sel.reset_index(drop=True), hide_index=True, use_container_width=True)
        return df_sel
    else:
        st.warning("Selecciona al menos una AEI para continuar.")
        return pd.DataFrame(columns=["Código OEI","Código AEI","Denominación","Nombre del Indicador"])

def seccion_ruta_estrategica():
    ruta = st.text_area("Ruta Estratégica (breve descripción)", height=120, placeholder="Describe la ruta estratégica...")
    return ruta

def seccion_anexos():
    st.write("Ingresa contenido para Anexo B-1, B-2 y B-3. Puedes dejar vacío si no aplica.")
    b1 = st.text_area("Anexo B-1", height=100, key='b1')
    b2 = st.text_area("Anexo B-2", height=100, key='b2')
    b3 = st.text_area("Anexo B-3", height=100, key='b3')
    return {'B-1': b1, 'B-2': b2, 'B-3': b3}
