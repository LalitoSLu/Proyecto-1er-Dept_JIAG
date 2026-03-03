import pandas as pd
import os

def procesar_radiacion(carpeta):
    listado_dfs = []
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".csv"):
            ruta = os.path.join(carpeta, archivo)
            
            # Detectar fin de encabezado NASA POWER
            skip = 0
            try:
                with open(ruta, 'r', encoding='utf-8') as f:
                    for line in f:
                        skip += 1
                        if "-END HEADER-" in line: break
            except UnicodeDecodeError:
                with open(ruta, 'r', encoding='latin1') as f:
                    for line in f:
                        skip += 1
                        if "-END HEADER-" in line: break
            
            # Carga de datos sin el argumento 'errors'
            df_temp = pd.read_csv(ruta, skiprows=skip, encoding='utf-8', on_bad_lines='skip')
            
            # Extraer estado del nombre (ej: radiacion_Nayarit.csv -> NAYARIT)
            estado = archivo.replace("radiacion_", "").replace(".csv", "").upper()
            df_temp["estado"] = estado
            
            # Mapeo de YEAR, MO, DY a fecha
            if all(col in df_temp.columns for col in ['YEAR', 'MO', 'DY']):
                df_temp['fecha'] = pd.to_datetime(df_temp[['YEAR', 'MO', 'DY']].rename(
                    columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day'}))
            
            # Columna ALLSKY_SFC_SW_DWN
            col_rad = next((c for c in df_temp.columns if "ALLSKY" in c), None)
            if col_rad:
                df_temp = df_temp.rename(columns={col_rad: "radiacion"})
                listado_dfs.append(df_temp[["fecha", "estado", "radiacion"]])
                
    return pd.concat(listado_dfs, ignore_index=True).dropna()