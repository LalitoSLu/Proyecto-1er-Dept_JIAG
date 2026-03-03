import pandas as pd
import unicodedata

def normalizar_texto(texto):
    if not isinstance(texto, str): return texto
    # Quita acentos y pone en mayúsculas
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode("utf-8")
    return texto.upper().strip()

def integrar(prec, rad, cont):
    # Estandarizar nombres de estados
    prec['estado'] = prec['estado'].apply(normalizar_texto)
    rad['estado'] = rad['estado'].apply(normalizar_texto)
    cont['estado'] = cont['estado'].apply(normalizar_texto)

    print(f"      - Rango Lluvia: {prec['fecha'].min()} a {prec['fecha'].max()}")
    print(f"      - Rango Radiación: {rad['fecha'].min()} a {rad['fecha'].max()}")

    # 1. Unión Diaria por Fecha y Estado
    df = pd.merge(prec, rad, on=["fecha", "estado"], how="inner")

    # 2. Si el cruce por estado falla, cruzamos por fecha promedio nacional
    if df.empty:
        print("      ⚠️ No hubo coincidencia Estado+Fecha. Intentando unión general por Fecha...")
        rad_avg = rad.groupby('fecha')['radiacion'].mean().reset_index()
        df = pd.merge(prec, rad_avg, on="fecha", how="inner")

    if df.empty:
        return pd.DataFrame()

    # 3. Unión con Contaminantes
    df["anio"] = df["fecha"].dt.year
    df = pd.merge(df, cont, on=["anio", "estado"], how="left")
    
    # Rellenar datos de contaminantes faltantes con la media
    for col in ['pm10', 'pm2.5', 'so2', 'nox']:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mean())

    return df