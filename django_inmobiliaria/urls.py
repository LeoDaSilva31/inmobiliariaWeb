# Q:\new\django_inmobiliaria\urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Importa las configuraciones del proyecto
from django.conf.urls.static import static # Importa la función para servir archivos estáticos/media

urlpatterns = [
    path('admin/', admin.site.urls), # URL para el panel de administración de Django
    path('', include('web_app.urls')), # Incluye todas las URLs definidas en tu aplicación 'web_app'
]

# Configuración para servir archivos estáticos y de media SÓLO DURANTE EL DESARROLLO.
# En producción, un servidor web como Nginx o Apache se encargaría de esto.
if settings.DEBUG:
    # Sirve los archivos de media (imágenes subidas por usuarios/admin)
    # Ejemplo: /media/propiedades_imagenes/mi_casa.jpg apuntará a Q:/new/media/propiedades_imagenes/mi_casa.jpg
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Opcional: Sirve los archivos estáticos desde STATICFILES_DIRS en desarrollo.
    # Esto es útil si tienes archivos estáticos globales en /q/new/static/
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]) 
    # La parte [0] es porque STATICFILES_DIRS es una lista, y queremos el primer (y en tu caso, único) elemento.