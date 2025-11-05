import streamlit as st
import pandas as pd
from io import StringIO

def seccion_mision():
    mision = st.text_area("Misión (texto)", height=120, placeholder="Escribe la misión de la municipalidad...")
    return mision

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

def seccion_oei():
    st.info("Agrega tus Objetivos Estratégicos Institucionales. Cada fila corresponde a un OEI.")
    uploaded = st.file_uploader("Subir tabla OEI (Excel o CSV)", type=['xlsx','csv'], accept_multiple_files=False, key='u_oei')
    if uploaded is not None:
        try:
            if uploaded.name.lower().endswith('.csv'):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded, engine='openpyxl')
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
            df = pd.DataFrame(columns=["Código","Denominación","Observaciones"])
    else:
        # crear tabla manual
        st.write("Crear OEI manualmente (ejemplo simple)")
        cols = st.columns([1,4,2])
        codigo = cols[0].text_input("Código ejemplo", key='oei_codigo')
        denominacion = cols[1].text_input("Denominación ejemplo", key='oei_deno')
        observ = cols[2].text_input("Observaciones", key='oei_obs')
        if st.button("Agregar OEI", key='add_oei'):
            if 'oei_df' not in st.session_state:
                st.session_state['oei_df'] = []
            st.session_state['oei_df'].append({'Código': codigo, 'Denominación': denominacion, 'Observaciones': observ})
        df = pd.DataFrame(st.session_state.get('oei_df', []))
    st.dataframe(df)
    return df

def seccion_aei():
    st.info("Agrega tus Acciones Estratégicas Institucionales. Cada fila corresponde a una AEI.")
    uploaded = st.file_uploader("Subir tabla AEI (Excel o CSV)", type=['xlsx','csv'], accept_multiple_files=False, key='u_aei')
    if uploaded is not None:
        try:
            if uploaded.name.lower().endswith('.csv'):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded, engine='openpyxl')
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
            df = pd.DataFrame(columns=["Código","Acción","Indicador","Responsable"])
    else:
        st.write("Crear AEI manualmente (ejemplo simple)")
        cols = st.columns([1,4,2,2])
        codigo = cols[0].text_input("Código ejemplo AEI", key='aei_codigo')
        accion = cols[1].text_input("Acción", key='aei_accion')
        indicador = cols[2].text_input("Indicador", key='aei_ind')
        responsable = cols[3].text_input("Responsable", key='aei_resp')
        if st.button("Agregar AEI", key='add_aei'):
            if 'aei_df' not in st.session_state:
                st.session_state['aei_df'] = []
            st.session_state['aei_df'].append({'Código': codigo, 'Acción': accion, 'Indicador': indicador, 'Responsable': responsable})
        df = pd.DataFrame(st.session_state.get('aei_df', []))
    st.dataframe(df)
    return df

def seccion_ruta_estrategica():
    ruta = st.text_area("Ruta Estratégica (breve descripción)", height=120, placeholder="Describe la ruta estratégica...")
    return ruta

def seccion_anexos():
    st.write("Ingresa contenido para Anexo B-1, B-2 y B-3. Puedes dejar vacío si no aplica.")
    b1 = st.text_area("Anexo B-1", height=100, key='b1')
    b2 = st.text_area("Anexo B-2", height=100, key='b2')
    b3 = st.text_area("Anexo B-3", height=100, key='b3')
    return {'B-1': b1, 'B-2': b2, 'B-3': b3}
