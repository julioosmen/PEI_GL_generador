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
# 💾 Guardar avance del PEI
# ======================================================
def guardar_pei_en_bd(data: dict):
    """
    Inserta o actualiza el avance del PEI en la tabla pei_avance.
    """
    codigo = data.get("codigo_pliego")
    fecha = datetime.now().isoformat()

    # Verificar si ya existe registro
    existing = supabase.table("pei_avance").select("*").eq("codigo_pliego", codigo).execute()

    payload = {
        "codigo_pliego": codigo,
        "mision": data.get("mision", ""),
        "oei_json": json.dumps(data.get("oei_json", [])),
        "aei_json": json.dumps(data.get("aei_json", [])),
        "ruta_json": json.dumps(data.get("ruta_json", [])),
        "anexo_b2_json": json.dumps(data.get("anexo_b2_json", [])),
        "anexos_json": json.dumps(data.get("anexos_json", {})),
        "fecha_actualizacion": fecha,
    }

    if existing.data:
        # 🔄 Update existente
        supabase.table("pei_avance").update(payload).eq("codigo_pliego", codigo).execute()
    else:
        # 🆕 Insert nuevo
        supabase.table("pei_avance").insert(payload).execute()

# ======================================================
# 📂 Cargar avance del PEI
# ======================================================
def cargar_pei_desde_bd(codigo_pliego: str):
    """
    Recupera el avance guardado para un código de pliego.
    """
    res = supabase.table("pei_avance").select("*").eq("codigo_pliego", codigo_pliego).execute()
    if not res.data:
        return None

    registro = res.data[0]
    # Convertir JSON strings a estructuras Python
    for campo in ["oei_json", "aei_json", "ruta_json", "anexo_b2_json", "anexos_json"]:
        if isinstance(registro.get(campo), str):
            try:
                registro[campo] = json.loads(registro[campo])
            except json.JSONDecodeError:
                registro[campo] = []
    return registro
