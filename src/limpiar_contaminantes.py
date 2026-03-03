import pandas as pd

def cargar_contaminantes(ruta):
    # Leemos con latin1 por los acentos
    df = pd.read_csv(ruta, encoding='latin1')
    
    # LIMPIEZA EXTREMA DE COLUMNAS: quitamos espacios y pasamos a minúsculas
    df.columns = df.columns.str.strip().str.lower()
    
    # Buscamos la columna de estado (puede ser 'estado', 'entidad', o 'unnamed: 0')
    if 'estado' in df.columns:
        pass
    elif 'entidad' in df.columns:
        df = df.rename(columns={'entidad': 'estado'})
    else:
        # Si no detecta el nombre, renombramos la primera columna (donde suelen estar los nombres)
        df.rename(columns={df.columns[0]: 'estado'}, inplace=True)

    # Forzamos la creación del año si no existe
    if 'anio' not in df.columns:
        df['anio'] = 2016 # Año base del inventario

    # Limpiamos los datos numéricos (quitar comas de los números "1,200.50")
    for col in df.columns:
        if col not in ['estado', 'anio']:
            df[col] = df[col].astype(str).str.replace(',', '').str.replace('"', '').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Estandarizamos los nombres de los estados
    df['estado'] = df['estado'].astype(str).str.upper().str.strip()
    
    return df