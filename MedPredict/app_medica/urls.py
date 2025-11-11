from django.urls import path
from .views import inicio_view, prediccion_view,dashboard_view

urlpatterns = [
    path('', inicio_view, name='inicio'),
    path('prediccion/', prediccion_view, name='prediccion'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
