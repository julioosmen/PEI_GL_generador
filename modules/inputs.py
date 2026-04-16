import streamlit as st
import pandas as pd
from io import StringIO
from pathlib import Path

def seccion_situacion_futura_deseada():

    st.info("**Debe responder:** ¿Qué alcanzará la entidad? + ¿Cómo lo logrará? + ¿Qué escenarios se mitigarán o aprovecharán?")

    situacion_futura_deseada = st.text_area("Situación futura deseada (texto)", height=120, placeholder="Escribe la situación futura deseada de la municipalidad...")
    return situacion_futura_deseada

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

    # Inicializa los valores de sesión solo si no existen
    if "mision_texto" not in st.session_state:
        st.session_state["mision_texto"] = ""
    if "mision_texto_area" not in st.session_state:
        st.session_state["mision_texto_area"] = ""

    opcion = st.selectbox("Selecciona un ejemplo de misión (opcional)", ["Selecciona un ejemplo..."] + ejemplos)

    # ✅ Si el usuario cambia de ejemplo, actualizamos antes de dibujar el área de texto
    if opcion != "Selecciona un ejemplo..." and opcion != st.session_state["mision_texto"]:
        st.session_state["mision_texto"] = opcion
        st.session_state["mision_texto_area"] = opcion

    # ✅ Renderizamos el área de texto (ya sincronizado)
    mision_texto = st.text_area(
        "✍️ Redacta o ajusta la misión institucional:",
        value=st.session_state["mision_texto_area"],
        height=150,
        key="mision_texto_area"
    )

    # Guardamos lo que el usuario escriba manualmente
    st.session_state["mision_texto"] = mision_texto

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
@st.cache_data
def cargar_oei_excel(path_excel="Extraer_por_elemento_MEGL.xlsx", hoja="OEI"):
    """
    Carga la hoja OEI desde el archivo Excel.
    Se espera que la hoja tenga, como mínimo, estas columnas:
    - Código
    - Enunciado
    - Nombre del indicador
    """
    try:
        path_excel = Path(path_excel)
        df = pd.read_excel(path_excel, sheet_name=hoja, engine="openpyxl")

        # Normalizar nombres de columnas por si vienen con espacios
        df.columns = [str(c).strip() for c in df.columns]

        columnas_requeridas = ["Código", "Enunciado", "Nombre del indicador"]
        faltantes = [c for c in columnas_requeridas if c not in df.columns]

        if faltantes:
            st.error(
                f"La hoja '{hoja}' no contiene las columnas requeridas: {', '.join(faltantes)}"
            )
            return pd.DataFrame(columns=columnas_requeridas)

        # Limpiar filas vacías
        df = df[columnas_requeridas].copy()
        df = df.dropna(subset=["Código", "Enunciado"])
        df["Código"] = df["Código"].astype(str).str.strip()
        df["Enunciado"] = df["Enunciado"].astype(str).str.strip()
        df["Nombre del indicador"] = df["Nombre del indicador"].fillna("").astype(str).str.strip()

        # Eliminar duplicados exactos
        df = df.drop_duplicates().reset_index(drop=True)

        return df

    except FileNotFoundError:
        st.error(f"No se encontró el archivo Excel: {path_excel}")
        return pd.DataFrame(columns=["Código", "Enunciado", "Nombre del indicador"])
    except Exception as e:
        st.error(f"No se pudo cargar la hoja '{hoja}' del archivo Excel: {e}")
        return pd.DataFrame(columns=["Código", "Enunciado", "Nombre del indicador"])


def seccion_oei(path_excel="Extraer_por_elemento_MEGL.xlsx"):
    # st.markdown("### Objetivos Estratégicos Institucionales (OEI)")

    oei_data = cargar_oei_excel(path_excel=path_excel, hoja="OEI")

    if oei_data.empty:
        return pd.DataFrame(columns=["Código", "Enunciado", "Nombre del indicador"])

    # Base única de OEI para el primer selector
    oei_base = (
        oei_data[["Código", "Enunciado"]]
        .drop_duplicates()
        .sort_values(by="Código")
        .reset_index(drop=True)
    )

    oei_dict = {
        row["Código"]: f"{row['Código']} - {row['Enunciado']}"
        for _, row in oei_base.iterrows()
    }

    # Recuperar selección previa
    oei_previas = st.session_state.get("oei_json", pd.DataFrame())
    codigos_previos = []

    if isinstance(oei_previas, pd.DataFrame) and not oei_previas.empty and "Código" in oei_previas.columns:
        codigos_previos = (
            oei_previas["Código"]
            .dropna()
            .astype(str)
            .str.strip()
            .drop_duplicates()
            .tolist()
        )
        codigos_previos = [c for c in codigos_previos if c in oei_dict]

    # Paso 1: seleccionar uno o más OEI
    codigos_seleccionados = st.multiselect(
        "Selecciona uno o más OEI:",
        options=list(oei_dict.keys()),
        default=codigos_previos,
        format_func=lambda x: oei_dict[x]
    )

    if not codigos_seleccionados:
        return pd.DataFrame(columns=["Código", "Enunciado", "Nombre del indicador"])

    # Paso 2: para cada OEI, elegir el indicador si hay más de uno
    filas_resultado = []

    for codigo in codigos_seleccionados:
        subset = oei_data[oei_data["Código"] == codigo].copy()
        enunciado = subset["Enunciado"].iloc[0]

        indicadores = (
            subset["Nombre del indicador"]
            .dropna()
            .astype(str)
            .str.strip()
            .replace("", pd.NA)
            .dropna()
            .drop_duplicates()
            .tolist()
        )

        # Buscar selección previa del indicador
        indicador_previo = None
        if isinstance(oei_previas, pd.DataFrame) and not oei_previas.empty:
            prev = oei_previas[oei_previas["Código"].astype(str).str.strip() == codigo]
            if not prev.empty and "Nombre del indicador" in prev.columns:
                candidato = str(prev["Nombre del indicador"].iloc[0]).strip()
                if candidato in indicadores:
                    indicador_previo = candidato

        st.markdown(f"**{codigo} - {enunciado}**")

        if len(indicadores) > 1:
            indicador_elegido = st.selectbox(
                f"Selecciona el indicador para {codigo}:",
                options=indicadores,
                index=indicadores.index(indicador_previo) if indicador_previo in indicadores else 0,
                key=f"indicador_{codigo}"
            )
        elif len(indicadores) == 1:
            indicador_elegido = indicadores[0]
            st.caption(f"Indicador seleccionado automáticamente: {indicador_elegido}")
        else:
            indicador_elegido = ""
            st.warning(f"El OEI {codigo} no tiene indicador registrado en el Excel.")

        filas_resultado.append({
            "Código": codigo,
            "Enunciado": enunciado,
            "Nombre del indicador": indicador_elegido
        })

    df_sel = pd.DataFrame(filas_resultado)

    st.dataframe(
        df_sel.reset_index(drop=True),
        hide_index=True,
        use_container_width=True
    )

    # Guardar selección en session_state
    st.session_state["oei_json"] = df_sel

    return df_sel

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
