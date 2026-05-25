"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import pandas as pd
import os


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", index_col=0)

    # Normalizar columnas de texto: minúsculas y eliminar espacios
    for col in ["sexo", "tipo_de_emprendimiento", "idea_negocio", "línea_credito"]:
        df[col] = df[col].str.lower().str.strip()
    df["barrio"] = df["barrio"].str.lower()

    # Eliminar filas con valores faltantes
    df = df.dropna()

    # Reemplazar separadores (-/_) por espacios en columnas de texto categóricas
    for col in ["idea_negocio", "línea_credito"]:
        df[col] = df[col].str.replace(r"[-_]", " ", regex=True).str.strip()
    df["barrio"] = df["barrio"].str.replace(r"[-_]", " ", regex=True)

    # Normalizar monto_del_credito: eliminar $, comas y espacios; quitar .0+ al final; convertir a int
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .str.replace(r"[\$ ,]", "", regex=True)
        .str.replace(r"\.0+$", "", regex=True)
        .astype(int)
    )

    # Normalizar fecha_de_beneficio: parsear formatos AAAA/MM/DD y DD/MM/AAAA por separado
    # para evitar interpretación errónea de fechas con prefijo AAAA usando dayfirst
    yyyy_mask = df["fecha_de_beneficio"].str.match(r"^\d{4}/")
    parsed = pd.Series(index=df.index, dtype="datetime64[ns]")
    parsed[~yyyy_mask] = pd.to_datetime(
        df.loc[~yyyy_mask, "fecha_de_beneficio"], dayfirst=True
    )
    parsed[yyyy_mask] = pd.to_datetime(
        df.loc[yyyy_mask, "fecha_de_beneficio"], format="%Y/%m/%d"
    )
    df["fecha_de_beneficio"] = parsed.dt.strftime("%Y/%m/%d")

    # Normalizar comuna_ciudadano a entero (almacenado como flotante)
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)

    # Eliminar filas duplicadas
    df = df.drop_duplicates()

    os.makedirs("files/output", exist_ok = True)
    df.to_csv("files/output/solicitudes_de_credito.csv", sep = ";", index = False)