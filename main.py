import pandas as pd
import numpy as np
import os
from src.limpiar_radiacion import procesar_radiacion
from src.limpiar_precipitacion import procesar_precipitacion
from src.limpiar_contaminantes import cargar_contaminantes
from src.integrar_datasets import integrar
from src.features import crear_features
from src.modelos import entrenar_modelos
from src.evaluar import evaluar
from src.mapa import generar_mapa_lluvia
# Importamos las funciones actualizadas para la carpeta /images
from src.visualizacion import (
    graficar_metricas_comparativas, 
    graficar_matriz_confusion, 
    graficar_importancia_features
)

def ejecutar_proyecto():
    print("\n" + "="*60)
    print("   SISTEMA DE PREDICCIÓN CLIMÁTICA (INGENIERÍA DE DATOS)   ")
    print("="*60 + "\n")

    # 1. Carga de datos
    rad = procesar_radiacion("datos/crudos/radiacion")
    prec = procesar_precipitacion("datos/crudos/precipitacion")
    cont = cargar_contaminantes("datos/crudos/contaminantes/3. Emisiones por Estado.csv")

    # 2. Integración
    df = integrar(prec, rad, cont)
    
    if df is None or df.empty:
        print("❌ Error: No se pudieron integrar los datos.")
        return

    # 3. Ingeniería de Variables (Features Avanzadas)
    print("[3/5] Generando indicadores de tendencia, caídas de radiación y estacionalidad...")
    df = crear_features(df)

    # 4. División de datos (70/30 cronológico)
    df = df.sort_values("fecha")
    
    train_size = int(len(df) * 0.7)
    train = df.iloc[:train_size].copy()
    test  = df.iloc[train_size:].copy()

    # --- LISTA COMPLETA DE VARIABLES ---
    features = [
        "radiacion", "rad_diff", "rad_mean_3", "rad_mean_7", 
        "rad_lag1", "pm10", "nox", "so2", "nox_rad_ratio", "mes"
    ]
    target = "lluvia_binaria" 

    X_train, y_train = train[features].fillna(0), train[target]
    X_test, y_test   = test[features].fillna(0), test[target]

    print(f"📊 Entrenamiento: {len(X_train)} días | Prueba: {len(X_test)} días")
    print(f"📊 Distribución lluvia en Train: {int(y_train.sum())} de {len(y_train)}")
    print(f"📊 Distribución lluvia en Test:  {int(y_test.sum())} de {len(y_test)}")

    # 5. Entrenamiento
    print(f"\nEntrenando modelos con balanceo de clase y nuevas variables...")
    modelos = entrenar_modelos(X_train, y_train)

    # 6. Evaluación
    print("\n" + "*"*50)
    print("             RESULTADOS DE PREDICCIÓN")
    print("*"*50)
    
    # En la parte de evaluación de main.py
    try:
        resultados = evaluar(modelos, X_test, y_test)
        
        # MEJORA: Asegurar que la carpeta existe antes de guardar el CSV
        if not os.path.exists('images'):
            os.makedirs('images')
            
        pd.DataFrame(resultados).T.to_csv("images/reporte_metricas_final.csv")
        print("📄 Reporte de métricas guardado en 'images/reporte_metricas_final.csv'")
        
        for mod, met in resultados.items():
            print(f"\n>>> {mod.upper()}:")
            print(f"    - Accuracy: {met.get('accuracy', 0):.4f}")
            print(f"    - Recall:   {met.get('recall', 0):.4f} (Detección de lluvia)")
            print(f"    - F1-Score: {met.get('f1_score', 0):.4f}")
            print(f"    - AUC-ROC:  {met.get('auc_roc', 0):.4f}")
    except Exception as e:
        print(f"❌ Error en evaluación: {e}")

    # 7. Análisis de Importancia
    print("\n" + "-"*50)
    print("ANÁLISIS DE IMPORTANCIA (Random Forest)")
    print("-"*50)
    importancia = modelos["rf"].feature_importances_
    for i, v in enumerate(features):
        print(f"Variable: {v:15} | Importancia: {importancia[i]:.4f}")

    # 8. Generación de Visuales
    print("\n[Generando archivos visuales elegantes en carpeta /images...]")
    
    # Mapa de Folium
    generar_mapa_lluvia(df)
    
    # Importancia de variables
    graficar_importancia_features(features, importancia)
    
    # Comparativa F1 vs AUC-ROC
    graficar_metricas_comparativas(resultados)
    
    # Heatmap Matriz de Confusión
    prob_rf = modelos["rf"].predict_proba(X_test)[:, 1]
    pred_rf = (prob_rf >= 0.25).astype(int)
    graficar_matriz_confusion("random_forest", y_test, pred_rf)

    print("\n✅ Proceso finalizado correctamente. Revisa la carpeta '/images'.")

if __name__ == "__main__":
    ejecutar_proyecto()