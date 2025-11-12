import streamlit as st
import pandas as pd
from io import StringIO

#def seccion_mision():
    #mision = st.text_area("Misión (texto)", height=120, placeholder="Escribe la misión de la municipalidad...")
    #return mision
import streamlit as st

def seccion_mision():
    """
    Despliega la sección de Misión Institucional con guía y ejemplos predefinidos.
    """

    st.info("**Estructura recomendada:** Rol central de la entidad + Población beneficiaria + Atributos del servicio o gestión.")

    ejemplos = [
        "Prestar servicios básicos a los vecinos de la localidad, garantizando calidad, eficiencia y oportunidad en su provisión.",
        "Proveer servicios públicos esenciales a la población de la localidad, priorizando cobertura universal, equidad y atención inclusiva.",
        "Brindar servicios básicos a los habitantes de la localidad, promoviendo sostenibilidad, responsabilidad ambiental y uso racional de recursos.",
        "Ofrecer servicios públicos esenciales a los vecinos de la localidad, integrando innovación tecnológica, mejora continua y atención personalizada.",
        "Garantizar servicios básicos para la población de la localidad, asegurando continuidad, seguridad y respuesta rápida.",
        "Desarrollar servicios públicos esenciales para los habitantes de la localidad, fomentando eficiencia operativa, transparencia y participación ciudadana.",
        "Suministrar servicios básicos a la población de la localidad, optimizando recursos, reduciendo brechas y mejorando la accesibilidad.",
        "Administrar servicios públicos esenciales para los vecinos de la localidad, fortaleciendo gestión participativa, control social y corresponsabilidad.",
        "Proporcionar servicios básicos a los habitantes de la localidad, priorizando bienestar social, inclusión y equidad territorial.",
        "Asegurar servicios públicos esenciales a la población de la localidad, incorporando estándares de calidad, modernización y sostenibilidad.",
        "Brindar servicios públicos orientados al bienestar de la población, mediante una gestión sostenible, ética, inclusiva y transparente."
    ]

    # Mostrar el selector de ejemplos
    opcion = st.selectbox("Selecciona un ejemplo de misión (opcional)", ["Selecciona un ejemplo..."] + ejemplos)

    # Si el usuario selecciona un ejemplo, se actualiza automáticamente el campo de texto
    if opcion != "Selecciona un ejemplo...":
        st.session_state["mision_texto"] = opcion

    # Campo para redactar o editar la misión
    mision_texto = st.text_area(
        "✍️ Redacta o ajusta la misión institucional:",
        value=st.session_state.get("mision_texto", ""),
        height=150,
        key="mision_texto_input"
    )

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
    #st.markdown("### 🎯 Objetivos Estratégicos Institucionales (OEI)")

    oei_data = pd.DataFrame([
        {"Código": "OEI.01", "Denominación": "Promover el ordenamiento territorial en beneficio de población local", "Nombre del Indicador": "Porcentaje de la población local que reside en zonas que cumplen con los instrumentos técnicos sustentatorios para el ordenamiento territorial"},
        {"Código": "OEI.02", "Denominación": "Fortalecer el acceso a la atención primaria de salud preventiva de la población local", "Nombre del Indicador": "Porcentaje de personas satisfechas con las campañas y actividades de promoción de salud realizadas por la municipalidad"},
        {"Código": "OEI.03", "Denominación": "Promover el acceso a servicios educativos, deportivos y recreacionales con enfoque intercultural e inclusivo para la población local", "Nombre del Indicador": "Porcentaje de participantes satisfechos con los programas educativos organizados por la municipalidad"},
        {"Código": "OEI.04", "Denominación": "Promover condiciones ambientales saludables y sostenibles para la población local", "Nombre del Indicador": "Ind.1 Porcentaje de ciudadanos satisfechos con el servicio de recojo de residuos sólidos / Ind.2 Porcentaje de zonas de la localidad donde se han reducido puntos críticos de contaminación"},
        {"Código": "OEI.05", "Denominación": "Reducir la exposición al riesgo de desastres de origen natural o antrópico de la población local", "Nombre del Indicador": "Porcentaje de zonas de la localidad con factores de riesgo de desastres eliminados o minimizados"},
        {"Código": "OEI.06", "Denominación": "Mejorar el acceso a servicios de protección social y defensa de derechos de la población en situación de vulnerabilidad de la localidad", "Nombre del Indicador": "Porcentaje de la población en situación de vulnerabilidad atendida por programas sociales municipales"},
        {"Código": "OEI.07", "Denominación": "Fortalecer la prevención y disuasión del delito y violencia en beneficio de la población local", "Nombre del Indicador": "Porcentaje de zonas con alta incidencia delictiva con servicio de patrullaje integrado"},
        {"Código": "OEI.08", "Denominación": "Garantizar la provisión de los servicios de agua potable y saneamiento en beneficio de la población local", "Nombre del Indicador": "Porcentaje de viviendas con servicio de agua potable y alcantarillado"},
        {"Código": "OEI.09", "Denominación": "Impulsar el crecimiento de la actividad empresarial, de emprendimientos y MYPES en la localidad", "Nombre del Indicador": "Porcentaje de micro y pequeñas empresas que operan con licencias municipales adecuadas"},
        {"Código": "OEI.10", "Denominación": "Mejorar el sistema de transporte y transitabilidad en beneficio de la población local", "Nombre del Indicador": "Porcentaje de puntos críticos de tránsito en vías locales atendidos y mitigados"},
        {"Código": "OEI.11", "Denominación": "Modernizar la Gestión Institucional", "Nombre del Indicador": "Porcentaje de ciudadanos satisfechos con la gestión institucional de la municipalidad"}
    ])

    # Leer selecciones anteriores si existen
    oei_previas = st.session_state.get("oei_json", pd.DataFrame())

    opciones = oei_data.apply(
        lambda r: f"{r['Código']} - {r['Denominación']} - {r['Nombre del Indicador']}", axis=1
    ).tolist()

    seleccionadas_previas = []
    if not oei_previas.empty:
        seleccionadas_previas = [
            f"{r['Código']} - {r['Denominación']} - {r['Nombre del Indicador']}"
            for _, r in oei_previas.iterrows()
        ]

    seleccionados = st.multiselect(
        "Selecciona uno o más OEI:",
        options=opciones,
        default=seleccionadas_previas
    )

    if seleccionados:
        codigos = [s.split(' - ')[0] for s in seleccionados]
        df_sel = oei_data[oei_data["Código"].isin(codigos)][
            ["Código", "Denominación", "Nombre del Indicador"]
        ]
        st.dataframe(df_sel.reset_index(drop=True), hide_index=True, use_container_width=True)
        return df_sel
    else:
        return pd.DataFrame(columns=["Código", "Denominación", "Nombre del Indicador"])

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
    #st.markdown("### 🧩 Acciones Estratégicas Institucionales (AEI)")

    if oei_seleccionados is None or oei_seleccionados.empty:
        st.info("Primero selecciona al menos un OEI para ver las AEI disponibles.")
        return pd.DataFrame(columns=["Código OEI", "Código AEI", "Denominación", "Nombre del Indicador"])

    aei_base = cargar_aei_excel()

    codigos_oei = oei_seleccionados["Código"].astype(str).tolist()
    aei_filtrado = aei_base[aei_base["Código OEI"].isin(codigos_oei)][
        ["Código OEI", "Código AEI", "Denominación", "Nombre del Indicador"]
    ]

    aei_previas = st.session_state.get("aei_json", pd.DataFrame())
    seleccionadas_list = []

    for codigo in codigos_oei:
        subset = aei_filtrado[aei_filtrado["Código OEI"] == codigo]
        opciones = subset.apply(
            lambda r: f"{r['Código AEI']} - {r['Denominación']}", axis=1
        ).tolist()

        default_values = []
        if not aei_previas.empty:
            default_values = [
                f"{r['Código AEI']} - {r['Denominación']}"
                for _, r in aei_previas[aei_previas["Código OEI"] == codigo].iterrows()
            ]

        seleccion = st.multiselect(
            f"Selecciona AEI para {codigo}",
            options=opciones,
            default=default_values,
            key=f"aei_{codigo}"
        )
        seleccionadas_list.extend(seleccion)

    if seleccionadas_list:
        codigos_aei_sel = [s.split(' - ')[0] for s in seleccionadas_list]
        df_sel = aei_filtrado[aei_filtrado["Código AEI"].isin(codigos_aei_sel)][
            ["Código OEI", "Código AEI", "Denominación", "Nombre del Indicador"]
        ]
        st.dataframe(df_sel.reset_index(drop=True), hide_index=True, use_container_width=True)
        return df_sel
    else:
        return pd.DataFrame(columns=["Código OEI", "Código AEI", "Denominación", "Nombre del Indicador"])

#def seccion_ruta_estrategica():
#    ruta = st.text_area("Ruta Estratégica (breve descripción)", height=120, placeholder="Describe la ruta estratégica...")
#    return ruta
def seccion_ruta_estrategica(oei_seleccionados, aei_seleccionadas, ruta_excel_vinculacion):

    #st.header("3️⃣ Ruta Estratégica: Vinculación con la PGG")

    if oei_seleccionados.empty:
        st.warning("⚠️ Primero selecciona los Objetivos Estratégicos Institucionales (OEI).")
        return pd.DataFrame()

    if aei_seleccionadas.empty:
        st.warning("⚠️ Luego selecciona las Acciones Estratégicas Institucionales (AEI).")
        return pd.DataFrame()

    try:
        # 🔹 Cargar archivo Excel con la vinculación PGG
        df_vinc = pd.read_excel(ruta_excel_vinculacion)

        # Aseguramos las columnas esperadas
        columnas_esperadas = [
            "Código OEI", "Denominación OEI", "Vinculación OEI con la PGG",
            "Código AEI", "Denominación AEI", "Vinculación AEI con la PGG"
        ]
        if not all(col in df_vinc.columns for col in columnas_esperadas):
            st.error("❌ El archivo de vinculación no tiene las columnas esperadas.")
            return pd.DataFrame()

        # 🔹 Filtrar por OEI y AEI seleccionados
        cod_oei_sel = oei_seleccionados["Código"].unique().tolist()
        cod_aei_sel = aei_seleccionadas["Código AEI"].unique().tolist()

        df_filtrado = df_vinc[
            (df_vinc["Código OEI"].isin(cod_oei_sel)) &
            (df_vinc["Código AEI"].isin(cod_aei_sel))
        ].copy()

        # 🔹 Si no hay coincidencias
        if df_filtrado.empty:
            st.warning("⚠️ No se encontró vinculación con la PGG para los OEI/AEI seleccionados.")
            return pd.DataFrame()

        # 🔹 Mostrar tabla agrupada
        st.dataframe(df_filtrado, hide_index=True, use_container_width=True)

        # 🔹 Retornar para usar en word_generator.py si se desea exportar
        return df_filtrado

    except Exception as e:
        st.error(f"❌ Error al cargar o procesar la vinculación: {e}")
        return pd.DataFrame()

def seccion_anexo_b1():
    st.write("Ingresa contenido para Anexo B-1.")
    b1 = st.text_area("Anexo B-1", height=100, key='b1')
    return b1

def seccion_anexo_b2(aei_seleccionadas, ruta_excel):

#   st.markdown("### 🧭 Anexo B-2: Vinculación de AEI con Políticas Nacionales")
    st.markdown(
        """
        Selecciona la **vinculación con la Política Nacional** correspondiente para cada AEI.  
        En algunos casos, una misma AEI puede estar asociada a más de una política; elige la más adecuada.  
        Se despliega el **nombre de la Política Nacional** y la **denominación del servicio** vinculado.
        """
    )
    
    try:
        # Leer el archivo Excel de vinculaciones
        df_pn = pd.read_excel(ruta_excel)

        # Normalizar nombres de columnas
        df_pn = df_pn.rename(columns={
            "Código AEI": "Código AEI",
            "Denominación AEI": "Denominación AEI",
            "Nombre del indicador AEI": "Nombre del indicador AEI",
            "Nombre de la Política Nacional": "Nombre de la Política Nacional",
            "Código_OP_PN": "Código_OP_PN",
            "Enunciado_OP_PN": "Enunciado_OP_PN",
            "Código_Lin_PN": "Código_Lin_PN",
            "Enunciado_Lin_PN": "Enunciado_Lin_PN",
            "Código_Servicio_PN": "Código_Servicio_PN",
            "Enunciado_Servicio_PN": "Enunciado_Servicio_PN",
            "Indicador_Servicio_PN": "Indicador_Servicio_PN"
        })

        # Filtrar solo AEI seleccionadas
        aei_codigos = aei_seleccionadas["Código AEI"].tolist() if "Código AEI" in aei_seleccionadas.columns else []
        df_filtrado = df_pn[df_pn["Código AEI"].isin(aei_codigos)]

        resultados = []

        # Para cada AEI seleccionada, mostrar las opciones de vinculación
        for codigo_aei in aei_codigos:
            subset = df_filtrado[df_filtrado["Código AEI"] == codigo_aei]

            if subset.empty:
                st.warning(f"No hay vínculos registrados para {codigo_aei}")
                continue

            denominacion = subset["Denominación AEI"].iloc[0]
            indicador = subset["Nombre del indicador AEI"].iloc[0]

            st.markdown(f"#### 🔹 {codigo_aei} — {denominacion}")

            # Mostrar las opciones disponibles
            opciones = [
 #              f"{row['Nombre de la Política Nacional']} | {row['Código_OP_PN']} | {row['Código_Lin_PN']} | {row['Código_Servicio_PN']}"
                f"{row['Nombre de la Política Nacional']} | {row['Enunciado_Servicio_PN']}"

                for _, row in subset.iterrows()
            ]

            seleccion = st.selectbox(
                f"Selecciona la vinculación PN para {codigo_aei}",
                opciones,
                key=f"sel_{codigo_aei}"
            )

            # Recuperar la fila seleccionada
            fila = subset.iloc[opciones.index(seleccion)]
            resultados.append(fila)

        # Construir tabla resumen
        if resultados:
            df_final = pd.DataFrame(resultados)[[
                "Nombre de la Política Nacional",
                "Código_OP_PN", "Enunciado_OP_PN",
                "Código_Lin_PN", "Enunciado_Lin_PN",
                "Código_Servicio_PN", "Enunciado_Servicio_PN",
                "Indicador_Servicio_PN",
                "Código AEI", "Denominación AEI", "Nombre del indicador AEI"
            ]]
          
            # 🔹 Quitar índice numérico de pandas
            df_final.reset_index(drop=True, inplace=True)
            
            st.markdown("### 🧾 Anexo B-2")
            #st.dataframe(df_final, use_container_width=True)
            st.dataframe(df_final, use_container_width=True, hide_index=True)
            return df_final
        else:
            st.info("Selecciona al menos una vinculación para continuar.")
            return pd.DataFrame()

    except Exception as e:
        st.error(f"❌ Error al cargar o procesar el Anexo B-2: {e}")
        return pd.DataFrame()

def seccion_anexo_b3():
    st.write("Ingresa contenido para Anexo B-3.")
    b3 = st.text_area("Anexo B-3", height=100, key='b3')
    return b3
