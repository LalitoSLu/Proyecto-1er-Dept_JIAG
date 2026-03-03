# Proyecto-1er-Dept_JIAG
# 🌦️ Sistema de Predicción Climática Nacional - Ingeniería de Datos

Este proyecto integra datos de **CONAGUA, UNAM y SEMARNAT** para predecir eventos de lluvia en México utilizando Machine Learning y Deep Learning.

## 📊 Características del Proyecto
- **ETL:** Integración de clima, radiación solar y contaminantes (PM10, NOx).
- **Modelos:** Regresión Logística, Random Forest, XGBoost y Redes Neuronales LSTM.
- **Visualización:** Mapas interactivos con Folium y gráficas de importancia de variables.

## 🚀 Instalación
1. Clonar repositorio: `git clone https://github.com/TU_USUARIO/TU_REPO.git`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar: `python main.py`

## 📈 Resultados Principales
- El modelo **Random Forest** demostró ser el más robusto para la detección de lluvia.
- Se identificó que la **radiación acumulada de 3 días** es el predictor clave.
