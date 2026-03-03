import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os  # Necesario para crear la carpeta
from sklearn.metrics import confusion_matrix

# Configuración de estética "Pro"
plt.style.use('seaborn-v0_8-muted')
sns.set_theme(style="whitegrid")

def asegurar_carpeta():
    """Crea la carpeta images si no existe."""
    if not os.path.exists('images'):
        os.makedirs('images')

def graficar_importancia_features(features, importancias):
    """Crea una gráfica de barras horizontal de importancia de variables."""
    asegurar_carpeta()
    df_imp = pd.DataFrame({'Variable': features, 'Importancia': importancias})
    df_imp = df_imp.sort_values('Importancia', ascending=True)

    plt.figure(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0.3, 0.8, len(df_imp)))
    
    plt.barh(df_imp['Variable'], df_imp['Importancia'], color=colors)
    plt.title('Influencia de Variables en la Predicción de Lluvia', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Nivel de Importancia (Gini Importance)', fontsize=12)
    
    plt.tight_layout()
    plt.savefig("images/importancia_variables_pro.png", dpi=300)
    plt.close()
    print("📊 Gráfica de importancia guardada en images/importancia_variables_pro.png")

def graficar_metricas_comparativas(resultados):
    """Compara F1-Score y AUC-ROC de los modelos (Requerido por rúbrica)."""
    asegurar_carpeta()
    data = []
    for mod, met in resultados.items():
        data.append({"Modelo": mod.upper(), "Métrica": "F1-Score", "Valor": met.get('f1_score', 0)})
        data.append({"Modelo": mod.upper(), "Métrica": "AUC-ROC", "Valor": met.get('auc_roc', 0)})
    
    df_plot = pd.DataFrame(data)

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x="Valor", y="Modelo", hue="Métrica", data=df_plot, palette="magma")
    
    plt.title('Comparativa de Modelos: F1-Score vs AUC-ROC', fontsize=14, fontweight='bold', pad=15)
    plt.xlim(0, 1.1)
    
    # Añadir valores a las barras
    for i in ax.patches:
        width = i.get_width()
        if width > 0:
            ax.text(width + 0.01, i.get_y() + i.get_height()/2, f'{width:.2f}', va='center')

    plt.tight_layout()
    plt.savefig("images/comparativa_modelos_final.png", dpi=300)
    plt.close()
    print("📈 Gráfica comparativa guardada en images/comparativa_modelos_final.png")

def graficar_matriz_confusion(modelo_nombre, y_true, y_pred):
    """Genera un Heatmap elegante de la matriz de confusión."""
    asegurar_carpeta()
    cm = confusion_matrix(y_true, y_pred)
    clases = ["Seco (0)", "Lluvia (1)"]
    
    plt.figure(figsize=(7, 5))
    sns.heatmap(cm, annot=True, fmt='g', cmap='Blues', xticklabels=clases, yticklabels=clases, 
                annot_kws={"size": 14, "weight": "bold"})
    
    plt.title(f'Matriz de Confusión: {modelo_nombre.upper()}', fontsize=14, fontweight='bold', pad=15)
    plt.ylabel('Valor Real (CONAGUA)', fontsize=12)
    plt.xlabel('Predicción del Sistema', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f"images/matriz_confusion_{modelo_nombre}.png", dpi=300)
    plt.close()
    print(f"🖼️  Matriz de confusión guardada en images/matriz_confusion_{modelo_nombre}.png")