import os
import pickle
import numpy as np
from django.shortcuts import render
from .forms import PredictionForm
from .models import Patient, PatientMedicalData, Prediction

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml_models")

def cargar_modelo(enfermedad):
    rutas = {
        'diabetes': os.path.join(MODEL_PATH, "modelo_diabetes.pkl"),
        'hipertension': os.path.join(MODEL_PATH, "modelo_hipertension.pkl"),
        'colesterol': os.path.join(MODEL_PATH, "modelo_colesterol.pkl"),
    }
    with open(rutas[enfermedad], 'rb') as f:
        modelo = pickle.load(f)
    return modelo


def prediccion_view(request):
    resultado = None

    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            enfermedad = form.cleaned_data['enfermedad']

            # Aquí podrías obtener o crear un paciente temporal
            paciente, _ = Patient.objects.get_or_create(
                name="Paciente Anónimo",
                age=40,
                gender="M"
            )

            # Guardamos los datos médicos
            datos_medicos = PatientMedicalData.objects.create(
                patient=paciente,
                imc=form.cleaned_data['imc'],
                pressure_systolic=form.cleaned_data['pressure_systolic'],
                pressure_diastolic=form.cleaned_data['pressure_diastolic'],
                glucose=form.cleaned_data['glucose'],
                cholesterol_total=form.cleaned_data['cholesterol_total'],
                cholesterol_ldl=form.cleaned_data['cholesterol_ldl'],
                cholesterol_hdl=form.cleaned_data['cholesterol_hdl'],
                triglycerides=form.cleaned_data['triglycerides'],
                hba1c=form.cleaned_data.get('hba1c') or 0
            )

            # Preparar los datos para el modelo
            datos = np.array([[
                form.cleaned_data['imc'],
                form.cleaned_data['pressure_systolic'],
                form.cleaned_data['pressure_diastolic'],
                form.cleaned_data['glucose'],
                form.cleaned_data['cholesterol_total'],
                form.cleaned_data['cholesterol_ldl'],
                form.cleaned_data['cholesterol_hdl'],
                form.cleaned_data['triglycerides'],
                form.cleaned_data.get('hba1c') or 0
            ]])

            modelo = cargar_modelo(enfermedad)
            pred = modelo.predict(datos)
            prob = modelo.predict_proba(datos)[0][1]
            riesgo = "Alto" if prob > 0.7 else "Moderado" if prob > 0.4 else "Bajo"

            # Guardar la predicción
            Prediction.objects.create(
                medical_data=datos_medicos,
                enfermedad=enfermedad,
                resultado=bool(pred[0]),
                probabilidad=prob,
                riesgo=riesgo
            )

            # Mostrar resultado en pantalla
            resultado = {
                'enfermedad': enfermedad.capitalize(),
                'prediccion': 'Positivo' if pred[0] == 1 else 'Negativo',
                'probabilidad': f"{prob*100:.2f}%",
                'riesgo': riesgo
            }

    else:
        form = PredictionForm()

    return render(request, 'prediccion.html', {'form': form, 'resultado': resultado})


from django.shortcuts import render
from django.utils import timezone

def inicio_view(request):
    return render(request, 'inicio.html', {'now': timezone.now()})

from django.shortcuts import render
from django.db import connection
from django.utils import timezone

def dashboard_view(request):
    # Conteos generales
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM patients;")
        total_pacientes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM predictions;")
        total_predicciones = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM predictions WHERE diabetes_risk_level='high' OR hypertension_risk_level='high' OR cardiovascular_risk_level='high';")
        total_riesgo_alto = cursor.fetchone()[0]

        # Distribución de enfermedades
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN diabetes_prediction THEN 1 ELSE 0 END) AS diabetes,
                SUM(CASE WHEN hypertension_prediction THEN 1 ELSE 0 END) AS hipertension,
                SUM(CASE WHEN cardiovascular_prediction THEN 1 ELSE 0 END) AS cardiovascular
            FROM predictions;
        """)
        data = cursor.fetchone()

    enfermedades_labels = ['Diabetes', 'Hipertensión', 'Cardiovascular']
    enfermedades_data = [data[0] or 0, data[1] or 0, data[2] or 0]

    context = {
        'total_pacientes': total_pacientes,
        'total_predicciones': total_predicciones,
        'total_riesgo_alto': total_riesgo_alto,
        'enfermedades_labels': enfermedades_labels,
        'enfermedades_data': enfermedades_data,
        'now': timezone.now()
    }

    return render(request, 'dashboard.html', context)







