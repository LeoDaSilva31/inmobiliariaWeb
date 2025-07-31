# Q:\new\web_app\models.py

from django.db import models
from django.utils import timezone
from django.urls import reverse # ¡Importante! Necesario para get_absolute_url

class Propiedad(models.Model):
    TIPO_PROPIEDAD_CHOICES = [
        ('casa', 'Casa'),
        ('apartamento', 'Apartamento'),
        ('terreno', 'Terreno'),
        ('local_comercial', 'Local Comercial'),
        ('oficina', 'Oficina'),
        ('galpon', 'Galpón'),
        ('deposito', 'Depósito'),
        ('otro', 'Otro'),
    ]

    TIPO_OPERACION_CHOICES = [
        ('venta', 'Venta'),
        ('alquiler', 'Alquiler'),
    ]

    # --- Nuevos Choices para Pet-Friendly ---
    TIPO_MASCOTA_CHOICES = [
        ('cualquiera', 'Cualquier tamaño'),
        ('pequena', 'Pequeña'),
        ('mediana', 'Mediana'),
        ('grande', 'Grande'),
        ('no_especificado', 'No especificado'), # Para cuando es pet_friendly pero no se detalla el tamaño
    ]
    # --- Fin Nuevos Choices ---

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50, choices=TIPO_PROPIEDAD_CHOICES)
    tipo_operacion = models.CharField(max_length=50, choices=TIPO_OPERACION_CHOICES)
    
    precio_usd = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    precio_pesos = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    direccion = models.CharField(max_length=255)
    localidad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    pais = models.CharField(max_length=100, default='Argentina')

    metros_cuadrados_total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    metros_cuadrados_cubierta = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    dormitorios = models.IntegerField(null=True, blank=True)
    banios = models.IntegerField(null=True, blank=True)
    cocheras = models.IntegerField(null=True, blank=True)

    antiguedad = models.IntegerField(null=True, blank=True, help_text="Años de antigüedad")
    
    amenidades = models.TextField(blank=True, help_text="Lista de amenidades separadas por comas")
    
    imagen_principal = models.ImageField(upload_to='web_app_imagenes/', null=True, blank=True)

    is_destacada = models.BooleanField(default=False)
    
    ESTADO_PUBLICACION_CHOICES = [
        ('borrador', 'Borrador'),
        ('publicada', 'Publicada'),
        ('archivada', 'Archivada'),
    ]
    estado_publicacion = models.CharField(max_length=20, choices=ESTADO_PUBLICACION_CHOICES, default='borrador')

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    # --- Nuevos Campos para Mascotas ---
    acepta_mascotas = models.BooleanField(
        default=False,
        verbose_name="Acepta Mascotas",
        help_text="Marcar si la propiedad permite mascotas."
    )
    tipo_mascota_permitida = models.CharField(
        max_length=20,
        choices=TIPO_MASCOTA_CHOICES,
        default='no_especificado',
        blank=True,
        null=True, # Puede ser nulo si no acepta mascotas o si no se especifica el tipo
        verbose_name="Tipo de Mascota Permitida",
        help_text="Si acepta mascotas, especificar el tamaño."
    )
    # --- Fin Nuevos Campos ---

    def __str__(self):
        return f"{self.titulo} - {self.direccion}"

    # Método para obtener la URL absoluta de una instancia de Propiedad
    # Utiliza el nombre de URL 'web_app:propiedad_detail' que definimos en web_app/urls.py
    def get_absolute_url(self):
        return reverse('web_app:propiedad_detail', args=[str(self.pk)])

    class Meta:
        verbose_name_plural = "Propiedades"


class PropiedadImagen(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='web_app_galeria/')
    descripcion_corta = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Imagen de {self.propiedad.titulo} ({self.id})"

class Consulta(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultas')
    nombre_completo = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    mensaje = models.TextField()
    fecha_consulta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consulta de {self.nombre_completo} sobre {self.propiedad.titulo if self.propiedad else 'N/A'}"

    class Meta:
        verbose_name_plural = "Consultas"