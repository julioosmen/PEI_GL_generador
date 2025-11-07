# modules/db.py
import streamlit as st
from sqlalchemy import create_engine, text
from datetime import datetime
import json

# Leer URL desde los secretos de Streamlit
DATABASE_URL = st.secrets["DATABASE_URL"]

# Crear conexión
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def guardar_pei_en_bd(data: dict):
    """Guarda o actualiza un registro en la tabla pei_avance."""
    sql = text("""
    INSERT INTO pei_avance (
        codigo_pliego, mision, oei_json, aei_json, ruta_json, anexo_b2_json, anexos_json, fecha_actualizacion
    )
    VALUES (
        :codigo_pliego, :mision, :oei_json::jsonb, :aei_json::jsonb, :ruta_json::jsonb, 
        :anexo_b2_json::jsonb, :anexos_json::jsonb, :fecha
    )
    ON CONFLICT (codigo_pliego) DO UPDATE SET
        mision = EXCLUDED.mision,
        oei_json = EXCLUDED.oei_json,
        aei_json = EXCLUDED.aei_json,
        ruta_json = EXCLUDED.ruta_json,
        anexo_b2_json = EXCLUDED.anexo_b2_json,
        anexos_json = EXCLUDED.anexos_json,
        fecha_actualizacion = EXCLUDED.fecha_actualizacion;
    """)
    with engine.begin() as conn:
        conn.execute(sql, {
            "codigo_pliego": data["codigo_pliego"],
            "mision": data["mision"],
            "oei_json": json.dumps(data["oei_json"]),
            "aei_json": json.dumps(data["aei_json"]),
            "ruta_json": json.dumps(data["ruta_json"]),
            "anexo_b2_json": json.dumps(data["anexo_b2_json"]),
            "anexos_json": json.dumps(data["anexos_json"]),
            "fecha": datetime.utcnow()
        })

def cargar_pei_desde_bd(codigo_pliego: str):
    """Carga el avance guardado para un código de pliego."""
    sql = text("SELECT * FROM pei_avance WHERE codigo_pliego = :codigo_pliego;")
    with engine.begin() as conn:
        result = conn.execute(sql, {"codigo_pliego": codigo_pliego}).mappings().first()
        return dict(result) if result else None
