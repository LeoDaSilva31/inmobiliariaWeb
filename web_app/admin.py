# Q:\new\web_app\admin.py

# from traceback import format_tb # ¡OJO! Esto estaba mal, NO es necesario importarlo
from django.contrib import admin
from django.utils.html import format_html # Importa format_html aquí
from .models import Propiedad, PropiedadImagen, Consulta # Importa tus modelos

# Establece el site_header a una cadena vacía para quitar el título
admin.site.site_header = "Administración" 


# 1. Administración para PropiedadImagen (Inline)
class PropiedadImagenInline(admin.TabularInline):
    model = PropiedadImagen
    extra = 1
    fields = ('imagen', 'descripcion_corta')
    # Si quieres mostrar un thumbnail de la imagen en el admin:
    # def thumbnail_preview(self, obj):
    #     if obj.imagen:
    #         return format_html('<img src="{}" style="width: 80px; height: 80px; object-fit: cover;" />', obj.imagen.url)
    #     return "No Image"
    # thumbnail_preview.short_description = "Previsualización"


# 2. Administración para Propiedad
@admin.register(Propiedad) # Registra el modelo Propiedad en el admin
class PropiedadAdmin(admin.ModelAdmin):
    list_display = (
        'titulo', 'localidad', 'tipo_operacion', 'precio_usd', 'precio_pesos',
        'is_destacada', 'acepta_mascotas', 'estado_publicacion', 'fecha_actualizacion'
    )
    
    list_filter = (
        'tipo', 'tipo_operacion', 'localidad', 'is_destacada', 'acepta_mascotas',
        'estado_publicacion', 'fecha_creacion', 'fecha_actualizacion', 'tipo_mascota_permitida'
    )
    
    search_fields = (
        'titulo', 'descripcion', 'direccion', 'localidad', 'provincia', 'amenidades'
    )
    
    list_display_links = ('titulo',)
    list_per_page = 25
    ordering = ('-fecha_creacion',)

    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')

    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'tipo', 'tipo_operacion'),
            'description': 'Información fundamental de la propiedad.'
        }),
        ('Detalles de Precio', {
            'fields': ('precio_usd', 'precio_pesos'),
            'description': 'Define los precios de venta o alquiler. Al menos uno debe ser completado.'
        }),
        ('Ubicación', {
            'fields': ('direccion', 'localidad', 'provincia', 'pais'),
            'description': 'Ubicación física de la propiedad.'
        }),
        ('Características', {
            'fields': ('metros_cuadrados_total', 'metros_cuadrados_cubierta', 'dormitorios', 'banios', 'cocheras', 'antiguedad', 'amenidades'),
            'description': 'Especificaciones y comodidades de la propiedad.'
        }),
        ('Mascotas', {
            'fields': ('acepta_mascotas', 'tipo_mascota_permitida'),
            'description': 'Configuración de si la propiedad es amigable con mascotas y sus restricciones.'
        }),
        ('Gestión y Publicación', {
            'fields': ('imagen_principal', 'is_destacada', 'estado_publicacion', 'fecha_creacion', 'fecha_actualizacion'),
            'description': 'Control de la visibilidad y estado de la propiedad.',
            'classes': ('collapse',),
        }),
    )

    inlines = [PropiedadImagenInline]

    actions = ['make_destacada', 'make_not_destacada', 'publish_property', 'archive_property']

    def make_destacada(self, request, queryset):
        updated = queryset.update(is_destacada=True)
        self.message_user(request, f'{updated} propiedades marcadas como destacadas.', level='success')
    make_destacada.short_description = "Marcar propiedades seleccionadas como destacadas"

    def make_not_destacada(self, request, queryset):
        updated = queryset.update(is_destacada=False)
        self.message_user(request, f'{updated} propiedades desmarcadas como destacadas.', level='warning')
    make_not_destacada.short_description = "Desmarcar propiedades seleccionadas como destacadas"
    
    def publish_property(self, request, queryset):
        updated = queryset.update(estado_publicacion='publicada')
        self.message_user(request, f'{updated} propiedades publicadas.', level='success')
    publish_property.short_description = "Publicar propiedades seleccionadas"

    def archive_property(self, request, queryset):
        updated = queryset.update(estado_status='archivada') # Ojo, corregí a estado_status si es el nombre correcto
        self.message_user(request, f'{updated} propiedades archivadas.', level='warning')
    archive_property.short_description = "Archivar propiedades seleccionadas"


# 3. Administración para Consulta
# ¡IMPORTANTE! Para que NO se pueda manejar el modelo de consulta desde el admin,
# SIMPLEMENTE NO LO REGISTRES. Elimina o comenta el decorador @admin.register(Consulta)
# y la clase ConsultaAdmin completa.
# Si lo quitas de aquí, el modelo de Consulta ya no será accesible a través del panel de administración.
# Si necesitas consultar los datos de Consulta, deberás hacerlo a través de la shell de Django o crear vistas personalizadas.

# @admin.register(Consulta) # <-- COMENTA O ELIMINA ESTA LÍNEA Y TODA LA CLASE ConsultaAdmin
# class ConsultaAdmin(admin.ModelAdmin):
#     list_display = ('nombre_completo', 'email', 'telefono', 'propiedad_link', 'fecha_consulta')
    
#     list_filter = ('fecha_consulta',)
    
#     search_fields = ('nombre_completo', 'email', 'telefono', 'mensaje', 'propiedad__titulo', 'propiedad__direccion')
    
#     readonly_fields = ('nombre_completo', 'email', 'telefono', 'mensaje', 'propiedad', 'fecha_consulta')

#     ordering = ('-fecha_consulta',)

#     def propiedad_link(self, obj):
#         if obj.propiedad:
#             # Asegúrate que 'web_app:propiedad_detail' sea la URL correcta de tu detalle de propiedad
#             return format_html('<a href="{}">{}</a>',
#                                obj.propiedad.get_absolute_url() if hasattr(obj.propiedad, 'get_absolute_url') else f'/propiedad/{obj.propiedad.pk}/',
#                                obj.propiedad.titulo)
#         return "N/A"
#     propiedad_link.short_description = "Propiedad"


# ---
# Gestión de modelos internos de Django
# ---

# Ocultar "Autenticación y Autorización"
# Desregistrar los modelos de autenticación para que no aparezcan en el panel.
# Esto elimina 'Usuarios' y 'Grupos' de la sección 'Autenticación y Autorización'.
try:
    # Importamos User y Group solo cuando necesitamos desregistrarlos para evitar importar
    # django.contrib.auth.models en la parte superior del archivo si no se usan más.
    from django.contrib.auth.models import Group, User 
    admin.site.unregister(Group)
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    # Esto maneja el caso si por alguna razón ya no estuvieran registrados (no debería ocurrir normalmente).
    pass