# django_inmobiliaria/web_app/urls.py

from django.urls import path
from . import views

app_name = 'web_app'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('propiedades/', views.propiedad_list_view, name='propiedad_list'),
    path('propiedad/<int:pk>/', views.propiedad_detail_view, name='propiedad_detail'),
    path('contacto/', views.contacto_view, name='contacto'), # Tu vista general de contacto
    path('busqueda/', views.busqueda_propiedades_view, name='busqueda'),
    
    # ¡AÑADE ESTA LÍNEA para el formulario de contacto específico de una propiedad!
    path('propiedad/<int:pk>/contactar/', views.contactar_propiedad_view, name='contactar_propiedad'),
]