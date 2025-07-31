# inmobiliaria_project_new/web_app/forms.py

from django import forms
from web_app.models import Consulta 

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['nombre_completo', 'email', 'telefono', 'mensaje']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo', 'id': 'id_nombre_completo'}), # Puedes añadir el id explícitamente para mayor claridad
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu email', 'id': 'id_email'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu teléfono (opcional)', 'id': 'id_telefono'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tu mensaje', 'rows': 5, 'id': 'id_mensaje'}), # <-- CONFIRMADO: id_mensaje
        }
        labels = {
            'nombre_completo': 'Nombre Completo',
            'email': 'Email',
            'telefono': 'Teléfono',
            'mensaje': 'Mensaje',
        }