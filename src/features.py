import pandas as pd
import numpy as np

def crear_features(df):
    """
    Genera variables avanzadas para detectar patrones meteorológicos
    que preceden a la lluvia.
    """
    # Aseguramos el orden cronológico por estado para que los cálculos sean correctos
    df = df.sort_values(['estado', 'fecha']).copy()
    
    # --- 1. INDICADORES DE RADIACIÓN (CAÍDAS Y PROMEDIOS) ---
    
    # Diferencia diaria: ¿Bajó la radiación respecto a ayer? (Clave para detectar nubes)
    df['rad_diff'] = df.groupby('estado')['radiacion'].diff()
    
    # Promedio móvil de 3 días: Captura nubarrones de corta duración
    df['rad_mean_3'] = df.groupby('estado')['radiacion'].transform(lambda x: x.rolling(window=3).mean())
    
    # Promedio móvil de 7 días: Captura periodos de mal clima persistente
    df['rad_mean_7'] = df.groupby('estado')['radiacion'].transform(lambda x: x.rolling(window=7).mean())
    
    # Lags (Valores de días anteriores)
    df['rad_lag1'] = df.groupby('estado')['radiacion'].shift(1)
    df['rad_lag3'] = df.groupby('estado')['radiacion'].shift(3)
    
    # --- 2. INDICADORES DE CONTAMINANTES ---
    
    # Relación NOx vs Radiación: 
    # Mucho contaminante con poca luz suele ser señal de inversión térmica o nubes bajas
    df['nox_rad_ratio'] = df['nox'] / (df['radiacion'] + 0.1)
    
    # Tendencia de PM10: ¿Están subiendo las partículas?
    df['pm10_diff'] = df.groupby('estado')['pm10'].diff()
    
    # --- 3. VARIABLES TEMPORALES ---
    
    # El mes es vital porque la lluvia en México es estacional (verano/otoño)
    df['mes'] = df['fecha'].dt.month
    
    # Marcamos si es fin de semana (opcional, pero a veces ayuda en ruido de datos)
    df['es_finde'] = df['fecha'].dt.dayofweek.isin([5, 6]).astype(int)

    # --- 4. LIMPIEZA FINAL ---
    
    # Al usar rolling(7) y shift(3), las primeras filas de cada estado tendrán NaNs.
    # Las eliminamos para que el modelo no reciba datos incompletos.
    df_limpio = df.dropna().copy()
    
    # Aseguramos que el año esté disponible para el main.py
    df_limpio['anio'] = df_limpio['fecha'].dt.year

    return df_limpio