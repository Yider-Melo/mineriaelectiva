from django import forms

class PredictionForm(forms.Form):
    DISEASE_CHOICES = [
        ('diabetes', 'Diabetes'),
        ('hipertension', 'Hipertensión'),
        ('colesterol', 'Colesterol alto'),
    ]

    enfermedad = forms.ChoiceField(choices=DISEASE_CHOICES, label="Enfermedad a predecir")
    imc = forms.FloatField(label="Índice de masa corporal (IMC)")
    pressure_systolic = forms.IntegerField(label="Presión sistólica")
    pressure_diastolic = forms.IntegerField(label="Presión diastólica")
    glucose = forms.IntegerField(label="Glucosa (mg/dL)")
    cholesterol_total = forms.IntegerField(label="Colesterol total (mg/dL)")
    cholesterol_ldl = forms.IntegerField(label="Colesterol LDL (mg/dL)")
    cholesterol_hdl = forms.IntegerField(label="Colesterol HDL (mg/dL)")
    triglycerides = forms.IntegerField(label="Triglicéridos (mg/dL)")
    hba1c = forms.FloatField(label="HbA1c (%)", required=False)
