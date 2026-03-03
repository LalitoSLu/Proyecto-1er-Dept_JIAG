from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
import numpy as np

def entrenar_modelos(X_train, y_train):
    modelos = {}
    
    # --- CALCULO DE PESOS ---
    # Calculamos la proporción entre días secos y lluviosos
    # En tu caso es aprox 451 / 61 = 7.4
    con_lluvia = np.sum(y_train == 1)
    sin_lluvia = np.sum(y_train == 0)
    ratio = sin_lluvia / con_lluvia if con_lluvia > 0 else 1
    
    print(f"      -> Aplicando factor de balanceo: {ratio:.2f}")

    # 1. Regresión Logística (Balanceada)
    modelos["logistica"] = LogisticRegression(
        max_iter=1000, 
        class_weight='balanced'
    ).fit(X_train, y_train)
    
    # 2. Random Forest (Balanceado)
    modelos["rf"] = RandomForestClassifier(
        n_estimators=100, 
        class_weight='balanced', 
        random_state=42
    ).fit(X_train, y_train)
    
    # 3. XGBoost (Balanceado con scale_pos_weight)
    modelos["xgb"] = XGBClassifier(
        eval_metric="logloss",
        scale_pos_weight=ratio # Da más peso a la clase positiva (lluvia)
    ).fit(X_train, y_train)
    
    # 4. Red Neuronal LSTM (Balanceada)
    # Reshape para LSTM: [muestras, pasos_de_tiempo, variables]
    X_train_lstm = np.reshape(X_train.values, (X_train.shape[0], 1, X_train.shape[1]))
    
    lstm = Sequential([
        Input(shape=(1, X_train.shape[1])),
        LSTM(64, activation='tanh', return_sequences=False), # Tanh es más estable para LSTM
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    
    lstm.compile(optimizer='adam', loss='binary_crossentropy', metrics=['Recall'])
    
    # Aplicamos class_weight en el fit de Keras
    pesos_clase = {0: 1.0, 1: ratio}
    
    lstm.fit(
        X_train_lstm, 
        y_train, 
        epochs=20, # Aumentamos un poco las épocas para que aprenda el balanceo
        batch_size=16, 
        class_weight=pesos_clase,
        verbose=0
    )
    
    modelos["lstm"] = lstm
    return modelos