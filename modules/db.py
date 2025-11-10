from supabase import create_client, Client
import streamlit as st

# ======================================================
# 🔗 Conexión a Supabase (vía REST API oficial)
# ======================================================
# Debes tener estas claves en tu archivo de secretos:
# SUPABASE_URL = "https://jvvjdirsdlcnpgdtwlog.supabase.co"
# SUPABASE_KEY = "tu_clave_api_anon"

url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# ======================================================
# 💾 Funciones de guardar y cargar avances PEI
# ======================================================
def guardar_pei_en_bd(data: dict):
    """Inserta o actualiza un registro de avance del PEI en Supabase."""
    codigo = data.get("codigo_pliego")
    # Verificar si ya existe registro
    result = supabase.table("pei_avance").select("codigo_pliego").eq("codigo_pliego", codigo).execute()

    if result.data:
        # Actualiza el registro existente
        response = supabase.table("pei_avance").update(data).eq("codigo_pliego", codigo).execute()
    else:
        # Inserta un nuevo registro
        response = supabase.table("pei_avance").insert(data).execute()

    return response


def cargar_pei_desde_bd(codigo_pliego: str):
    """Obtiene el registro de avance del PEI para un código de pliego."""
    result = supabase.table("pei_avance").select("*").eq("codigo_pliego", codigo_pliego).execute()
    if result.data:
        return result.data[0]
    return None
