# -*- coding: utf-8 -*-
"""FAR Panel registro datos_session_state

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Z2jP-a6DrF4Q01XTkq2-7HQxUbQIkTHY
"""

# 1. Importar librerías necesarias
import streamlit as st
import pandas as pd
from datetime import datetime
import os
from zoneinfo import ZoneInfo

# Inicializar session state
if "etapa" not in st.session_state:
    st.session_state.etapa = "CEE"

# Datos del proyecto
cees = ["Afanías", "Aprocor", "Artesa", "Envera", "Funcarma", "Juan XXIII", "Prodis", "Trefemo"]
lineas_por_cee = {
    "Afanías": ["Línea 1", "Línea 2"],
    "Aprocor": ["Línea 1", "Línea 2"],
    "Artesa": ["Línea 1", "Línea 2", "Línea 3"],
    "Envera": ["Línea 1", "Línea 2", "Línea 3", "Línea 4"],
    "Funcarma": ["Línea 1", "Línea 2", "Línea 3"],
    "Juan XXIII": ["Línea 1", "Línea 2", "Línea 3"],
    "Prodis": ["Línea 1", "Línea 2", "Línea 3"],
    "Trefemo": ["Línea 1", "Línea 2", "Línea 3", "Línea 4"]
}
estaciones_por_linea = {
    "Afanías-Línea 1": 2, "Afanías-Línea 2": 2,
    "Aprocor-Línea 1": 2, "Aprocor-Línea 2": 6,
    "Artesa-Línea 1": 3, "Artesa-Línea 2": 2, "Artesa-Línea 3": 2,
    "Envera-Línea 1": 3, "Envera-Línea 2": 3, "Envera-Línea 3": 2, "Envera-Línea 4": 3,
    "Funcarma-Línea 1": 4, "Funcarma-Línea 2": 3, "Funcarma-Línea 3": 3,
    "Juan XXIII-Línea 1": 3, "Juan XXIII-Línea 2": 3, "Juan XXIII-Línea 3": 3,
    "Prodis-Línea 1": 2, "Prodis-Línea 2": 2, "Prodis-Línea 3": 3,
    "Trefemo-Línea 1": 4, "Trefemo-Línea 2": 3, "Trefemo-Línea 3": 3, "Trefemo-Línea 4": 4
}



st.set_page_config(page_title="Registro Producción CEE", layout="centered")
st.title("📦 Registro de Producción - Centro Especial de Empleo")

# Etapas
if st.session_state.etapa == "CEE":
    cee = st.selectbox("Selecciona el CEE", cees)
    if st.button("Continuar"):
        st.session_state.cee = cee
        st.session_state.etapa = "linea"

        # Mover esto dentro del botón:
        st.session_state.csv_path = f"registro_produccion_{cee}.csv"
        try:
            df = pd.read_csv(st.session_state.csv_path, sep=';')
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=["FechaHora", "CEE", "Línea", "Estación", "Operario", "Turno", "Producto", "Unidades", "Observaciones"])
            df.to_csv(st.session_state.csv_path, index=False, sep=';')
        st.session_state.df = df


elif st.session_state.etapa == "linea":
    lineas = lineas_por_cee[st.session_state.cee]
    linea = st.selectbox(f"Selecciona la línea de {st.session_state.cee}", lineas)
    if st.button("Continuar"):
        st.session_state.linea = linea
        st.session_state.etapa = "estacion"

elif st.session_state.etapa == "estacion":
    key = f"{st.session_state.cee}-{st.session_state.linea}"
    n_estaciones = estaciones_por_linea.get(key, 0)
    estaciones = [f"Estación {i+1}" for i in range(n_estaciones)]
    estacion = st.selectbox("Selecciona la estación", estaciones)
    if st.button("Continuar"):
        st.session_state.estacion = estacion
        st.session_state.etapa = "registro"

elif st.session_state.etapa == "registro":
    st.subheader(f"Registro en {st.session_state.cee} / {st.session_state.linea} / {st.session_state.estacion}")

    # Botón para iniciar la producción
    if st.button("🟢 Iniciar Producción"):
        zona = ZoneInfo("Europe/Madrid")
        fila_inicio = {
            "FechaHora": datetime.now(zona).strftime("%Y-%m-%d %H:%M:%S"),
            "CEE": st.session_state.cee,
            "Línea": st.session_state.linea,
            "Estación": st.session_state.estacion,
            "Operario": "Inicio producción",
            "Turno": "",
            "Producto": "",
            "Unidades": 0,
            "Observaciones": "Inicio de la jornada de producción"
        }
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([fila_inicio])], ignore_index=True)
        st.session_state.df.to_csv(st.session_state.csv_path, index=False, sep=';')
        st.success("🟢 Producción iniciada correctamente.")

    # Botón para registrar parada por incidencia
    if st.button("⛔ Parada por incidencia"):
        zona = ZoneInfo("Europe/Madrid")
        fila_parada = {
            "FechaHora": datetime.now(zona).strftime("%Y-%m-%d %H:%M:%S"),
            "CEE": st.session_state.cee,
            "Línea": st.session_state.linea,
            "Estación": st.session_state.estacion,
            "Operario": "Parada producción",
            "Turno": "",
            "Producto": "",
            "Unidades": 0,
            "Observaciones": "Parada de la producción por incidencia"
        }
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([fila_parada])], ignore_index=True)
        st.session_state.df.to_csv(st.session_state.csv_path, index=False, sep=';')
        st.error("⛔ Parada registrada.")

    # Entradas para el registro de producción
    operario = st.text_input("👤 Operario")
    turno = st.radio("🕒 Turno", ["Mañana", "Tarde", "Noche"])
    producto = st.selectbox("🧱 Producto", ["Producto A", "Producto B", "Producto C"])
    unidades = st.number_input("🔢 Unidades producidas", min_value=1, step=1)
    observaciones = st.text_area("📝 Observaciones")

    if st.button("✅ Registrar producción"):
        zona = ZoneInfo("Europe/Madrid")
        nueva_fila = {
            "FechaHora": datetime.now(zona).strftime("%Y-%m-%d %H:%M:%S"),
            "CEE": st.session_state.cee,
            "Línea": st.session_state.linea,
            "Estación": st.session_state.estacion,
            "Operario": operario,
            "Turno": turno,
            "Producto": producto,
            "Unidades": unidades,
            "Observaciones": observaciones
        }
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([nueva_fila])], ignore_index=True)
        st.session_state.df.to_csv(st.session_state.csv_path, index=False, sep=';', encoding='utf-8-sig')
        st.success("✅ Registro guardado correctamente.")

    st.markdown("---")
    st.markdown("### Últimos registros")
    st.dataframe(st.session_state.df.tail(5), use_container_width=True)

    # Descargar CSV
    with open(st.session_state.csv_path, "rb") as f:
        st.download_button("⬇️ Descargar CSV", f, file_name=f"registro_produccion_{st.session_state.cee}.csv", mime="text/csv")

        # Eliminar archivo
    if st.button("🗑️ Eliminar archivo de producción"):
        os.remove(st.session_state.csv_path)
        st.warning(f"Archivo `{st.session_state.csv_path}` eliminado. Recarga la app para reiniciar.")

    if st.button("🔁 Volver al inicio"):
        st.session_state.etapa = "CEE"