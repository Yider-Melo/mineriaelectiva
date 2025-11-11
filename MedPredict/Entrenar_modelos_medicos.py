# =============================================
# ENTRENAMIENTO DE MODELOS MÉDICOS PREDICTIVOS
# =============================================

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sqlalchemy import create_engine

usuario = 'postgres'
contraseña = '000000'
host = 'localhost'
base_datos = 'Premedic'

engine = create_engine(f'postgresql://{usuario}:{contraseña}@{host}/{base_datos}')

# Cargamos los datos médicos de los pacientes
query = """
SELECT 
    imc,
    pressure_systolic,
    pressure_diastolic,
    glucose,
    cholesterol_total,
    cholesterol_ldl,
    cholesterol_hdl,
    triglycerides,
    hba1c
FROM patient_medical_data;
"""

df = pd.read_sql(query, engine)

print(f"✅ Datos cargados: {df.shape[0]} registros, {df.shape[1]} columnas")

# ---------------------------------------------
# 2. CREACIÓN DE ETIQUETAS (Y)
# ---------------------------------------------
# Reglas médicas básicas para simular diagnóstico
df["diabetes"] = ((df["glucose"] > 126) | (df["hba1c"] > 6.5)).astype(int)
df["hipertension"] = ((df["pressure_systolic"] > 140) | (df["pressure_diastolic"] > 90)).astype(int)
df["colesterol_alto"] = ((df["cholesterol_total"] > 240) | (df["cholesterol_ldl"] > 160)).astype(int)

# ---------------------------------------------
# 3. VARIABLES DE ENTRADA
# ---------------------------------------------
X = df[[
    "imc", "pressure_systolic", "pressure_diastolic",
    "glucose", "cholesterol_total", "cholesterol_ldl",
    "cholesterol_hdl", "triglycerides", "hba1c"
]].fillna(0)

# ---------------------------------------------
# 4. ENTRENAMIENTO DE MODELOS
# ---------------------------------------------
def entrenar_modelo(y_col, nombre):
    y = df[y_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        random_state=42
    )
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print(f"\n🧠 Modelo: {nombre.upper()}")
    print(f"Precisión: {acc:.3f}")
    print(classification_report(y_test, y_pred))

    # Guardamos el modelo en un archivo .pkl
    with open(f"modelo_{nombre}.pkl", "wb") as f:
        pickle.dump(modelo, f)
    print(f"✅ Modelo guardado como modelo_{nombre}.pkl")

# Entrenamos los tres modelos
entrenar_modelo("diabetes", "diabetes")
entrenar_modelo("hipertension", "hipertension")
entrenar_modelo("colesterol_alto", "colesterol")

print("\n🎉 Entrenamiento completado con éxito.")
