# Q:\new\web_app\apps.py

from django.apps import AppConfig

class WebAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_app'
    # ¡Agrega esta línea!
    verbose_name = "Administración"