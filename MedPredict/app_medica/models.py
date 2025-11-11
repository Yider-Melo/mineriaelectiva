from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, default='doctor')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PatientMedicalData(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    imc = models.DecimalField(max_digits=5, decimal_places=2)
    pressure_systolic = models.IntegerField()
    pressure_diastolic = models.IntegerField()
    glucose = models.IntegerField()
    cholesterol_total = models.IntegerField()
    cholesterol_ldl = models.IntegerField()
    cholesterol_hdl = models.IntegerField()
    triglycerides = models.IntegerField()
    hba1c = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Datos médicos de {self.patient.name}"



class Prediction(models.Model):
    medical_data = models.ForeignKey(PatientMedicalData, on_delete=models.CASCADE)
    enfermedad = models.CharField(max_length=50)
    resultado = models.BooleanField()
    probabilidad = models.DecimalField(max_digits=5, decimal_places=4)
    riesgo = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.enfermedad} - {self.medical_data.patient.name}"



