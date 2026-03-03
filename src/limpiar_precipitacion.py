import pandas as pd
import os

def procesar_precipitacion(carpeta):
    listado_dfs = []
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".csv"):
            ruta = os.path.join(carpeta, archivo)
            # Cargamos el archivo histórico
            df_temp = pd.read_csv(ruta, encoding='latin1')
            
            # Estandarizamos nombres basándonos en tu archivo 'clima_nacional_limpio.csv'
            rename_dict = {
                'Fecha': 'fecha', 
                'Precip': 'precipitacion_mm', 
                'Estado': 'estado'
            }
            df_temp = df_temp.rename(columns=rename_dict)
            
            # Convertir a formato fecha real de Python
            df_temp['fecha'] = pd.to_datetime(df_temp['fecha'], errors='coerce')
            
            # Asegurar que exista la columna binaria para los modelos
            if 'lluvia_binaria' not in df_temp.columns:
                df_temp['lluvia_binaria'] = (df_temp['precipitacion_mm'] > 0).astype(int)
            
            # Seleccionamos solo lo necesario
            listado_dfs.append(df_temp[["fecha", "estado", "lluvia_binaria"]])
                
    if not listado_dfs:
        return pd.DataFrame()
        
    return pd.concat(listado_dfs, ignore_index=True).dropna(subset=['fecha'])