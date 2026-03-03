import numpy as np
from sklearn.metrics import accuracy_score, recall_score, f1_score, roc_auc_score

def evaluar(modelos, X_test, y_test):
    """
    Evalúa los modelos incluyendo métricas de Accuracy, Recall, F1 y AUC-ROC.
    """
    resultados = {}
    
    for nombre, modelo in modelos.items():
        # --- UMBRALES PERSONALIZADOS ---
        if nombre in ["logistica", "lstm"]:
            UMBRAL = 0.70  
        else:
            UMBRAL = 0.25  

        # --- PROBABILIDADES ---
        if nombre == "lstm":
            X_test_lstm = np.reshape(X_test.values, (X_test.shape[0], 1, X_test.shape[1]))
            probabilidades = modelo.predict(X_test_lstm, verbose=0).flatten()
        else:
            probabilidades = modelo.predict_proba(X_test)[:, 1]

        # --- PREDICCIONES ---
        predicciones = (probabilidades >= UMBRAL).astype(int)

        # --- MÉTRICAS ---
        resultados[nombre] = {
            "accuracy": accuracy_score(y_test, predicciones),
            "recall": recall_score(y_test, predicciones, zero_division=0),
            "f1_score": f1_score(y_test, predicciones, zero_division=0),
            "auc_roc": roc_auc_score(y_test, probabilidades), # Requerido por rúbrica
            "umbral_usado": UMBRAL
        }
    
    return resultados