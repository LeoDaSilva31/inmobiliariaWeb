# inmobiliaria_project_new/web_app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from web_app.models import Propiedad, Consulta # Importa tus modelos
from .forms import ConsultaForm # Importa tu formulario
from django.db.models import Q # Importa Q para consultas OR complejas


def home_view(request):
    propiedades_destacadas = Propiedad.objects.filter(is_destacada=True, estado_publicacion='publicada')[:6]
    context = {
        'propiedades_destacadas': propiedades_destacadas,
        'page_title': 'Inmobiliaria - Inicio',
    }
    return render(request, 'web_app/home.html', context)

def propiedad_list_view(request):
    propiedades = Propiedad.objects.filter(estado_publicacion='publicada').order_by('-fecha_creacion')
    context = {
        'propiedades': propiedades,
        'page_title': 'Listado de Propiedades',
    }
    return render(request, 'web_app/propiedad_list.html', context)

def propiedad_detail_view(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.propiedad = propiedad
            consulta.save()
            return redirect('web_app:propiedad_detail', pk=propiedad.pk)
    else:
        form = ConsultaForm(initial={'propiedad': propiedad.pk})

    context = {
        'propiedad': propiedad,
        'form': form,
        'page_title': f'{propiedad.titulo} - Detalles',
    }
    return render(request, 'web_app/propiedad_detail.html', context)

#Tu vista general de contacto (ya existente)
from django.conf import settings

def contacto_view(request):
    # Recoger parámetros de la URL si existen
    propiedad_id = request.GET.get('propiedad_id')
    propiedad_titulo = request.GET.get('propiedad_titulo')
    propiedad_direccion = request.GET.get('propiedad_direccion')
    propiedad_localidad = request.GET.get('propiedad_localidad')

    initial_data = {}
    if propiedad_id and propiedad_titulo:
        mensaje_inicial = f"¡Hola! Me gustaría obtener más información sobre la propiedad \"{propiedad_titulo}\""
        if propiedad_direccion and propiedad_localidad:
            mensaje_inicial += f" ubicada en {propiedad_direccion}, {propiedad_localidad}."
        elif propiedad_localidad:
            mensaje_inicial += f" ubicada en {propiedad_localidad}."
        mensaje_inicial += " Por favor, contáctenme para conocer los detalles."
        initial_data['mensaje'] = mensaje_inicial

    form = ConsultaForm(initial=initial_data)

    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            # Si la consulta viene de una propiedad específica, asociala
            if propiedad_id:
                try:
                    propiedad_asociada = Propiedad.objects.get(pk=propiedad_id)
                    consulta.propiedad = propiedad_asociada
                except Propiedad.DoesNotExist:
                    # Opcional: Logear que la propiedad no existe o manejar el error
                    pass
            consulta.save()

            # Redirigir a una página de agradecimiento o a la misma página con un mensaje
            # Puedes redirigir a formsubmit_next si lo prefieres, o manejarlo aquí
            return redirect(settings.FORMSUBMIT_NEXT) # Usamos la URL configurada en settings
    
    context = {
        'form': form,
        'page_title': 'Contacto',
        'formsubmit_email': settings.FORMSUBMIT_EMAIL,
        'formsubmit_next': settings.FORMSUBMIT_NEXT, # Ya está en settings
    }
    return render(request, 'web_app/contacto.html', context)

    # La vista contactar_propiedad_view queda en desuso para este flujo específico
    # Si la necesitas para otra funcionalidad (ej. un mini-formulario de contacto directamente en la página de detalle),
    # la mantienes. Para este caso, el botón de "Más Información" lleva a la vista general de contacto.
    # def contactar_propiedad_view(request, pk):
    #     propiedad = get_object_or_404(Propiedad, pk=pk)
    #     if request.method == 'POST':
    #         form = ConsultaForm(request.POST)
    #         if form.is_valid():
    #             consulta = form.save(commit=False)
    #             consulta.propiedad = propiedad
    #             consulta.save()
    #             return redirect('web_app:propiedad_detail', pk=propiedad.pk)
    #     return redirect('web_app:propiedad_detail', pk=propiedad.pk)

# La vista `contactar_propiedad_view` puede ser redundante si `propiedad_detail_view` ya maneja el POST.
# Sin embargo, si la tienes definida y en uso, se comporta de manera similar a propiedad_detail_view.
# La dejaré como está, asumiendo que su propósito es guardar en DB, no enviar por EmailJS.

# ¡AÑADE ESTA NUEVA VISTA para manejar el formulario de consulta de una propiedad específica!
def contactar_propiedad_view(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.propiedad = propiedad
            consulta.save()
            return redirect('web_app:propiedad_detail', pk=propiedad.pk)
    # Si no es POST o el POST no es válido, redirigir a la página de detalle
    return redirect('web_app:propiedad_detail', pk=propiedad.pk)

# Q:\new\web_app\views.py



# --- NUEVA VISTA DE BÚSQUEDA ---
def busqueda_propiedades_view(request):
    # Obtener todos los parámetros de la URL
    query = request.GET.get('q')
    tipo_propiedad = request.GET.get('tipo_propiedad')
    tipo_operacion = request.GET.get('tipo_operacion')
    min_precio_usd = request.GET.get('min_precio_usd')
    max_precio_usd = request.GET.get('max_precio_usd')
    min_precio_pesos = request.GET.get('min_precio_pesos')
    max_precio_pesos = request.GET.get('max_precio_pesos')
    localidad = request.GET.get('localidad')
    dormitorios = request.GET.get('dormitorios')
    banios = request.GET.get('banios')
    cocheras = request.GET.get('cocheras')
    acepta_mascotas = request.GET.get('acepta_mascotas')
    tipo_mascota_permitida = request.GET.get('tipo_mascota_permitida')
    is_destacada = request.GET.get('is_destacada')

    propiedades = Propiedad.objects.filter(estado_publicacion='publicada')

    active_filters_display = []

    # Crear una copia mutable de request.GET para manipularla
    current_get_params = request.GET.copy()

    # Función auxiliar para generar la URL de eliminación para un parámetro dado
    def generate_remove_url(param_to_remove):
        temp_params = current_get_params.copy()
        if param_to_remove in temp_params:
            del temp_params[param_to_remove]
        # Si el filtro es un checkbox que al desmarcar no se envía (como 'acepta_mascotas' o 'is_destacada')
        # y no tiene un valor explícito en la URL cuando está 'off',
        # aseguramos que no aparezca en la URL de eliminación.
        # Por ejemplo, si quitas 'acepta_mascotas', su valor no debe estar en la URL.
        # No es estrictamente necesario para todos los filtros, pero bueno para checkboxes.

        # urlencode por defecto convierte una QueryDict a una cadena de consulta.
        return temp_params.urlencode()


    # Aplicar filtros y poblar active_filters_display
    if query:
        propiedades = propiedades.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(direccion__icontains=query) |
            Q(localidad__icontains=query) |
            Q(provincia__icontains=query) |
            Q(amenidades__icontains=query)
        )
        active_filters_display.append({
            'param_name': 'q',
            'display_text': f"Palabra Clave: {query}",
            'remove_url_params': generate_remove_url('q')
        })

    if tipo_propiedad:
        propiedades = propiedades.filter(tipo=tipo_propiedad)
        tipo_propiedad_label = dict(Propiedad.TIPO_PROPIEDAD_CHOICES).get(tipo_propiedad, tipo_propiedad)
        active_filters_display.append({
            'param_name': 'tipo_propiedad',
            'display_text': tipo_propiedad_label.upper(),
            'remove_url_params': generate_remove_url('tipo_propiedad')
        })
    
    if tipo_operacion:
        propiedades = propiedades.filter(tipo_operacion=tipo_operacion)
        tipo_operacion_label = dict(Propiedad.TIPO_OPERACION_CHOICES).get(tipo_operacion, tipo_operacion)
        active_filters_display.append({
            'param_name': 'tipo_operacion',
            'display_text': tipo_operacion_label.upper(),
            'remove_url_params': generate_remove_url('tipo_operacion')
        })

    if min_precio_usd:
        try:
            propiedades = propiedades.filter(precio_usd__gte=float(min_precio_usd))
            active_filters_display.append({
                'param_name': 'min_precio_usd',
                'display_text': f"Precio USD Desde: U$D {min_precio_usd}",
                'remove_url_params': generate_remove_url('min_precio_usd')
            })
        except ValueError:
            pass
    if max_precio_usd:
        try:
            propiedades = propiedades.filter(precio_usd__lte=float(max_precio_usd))
            active_filters_display.append({
                'param_name': 'max_precio_usd',
                'display_text': f"Precio USD Hasta: U$D {max_precio_usd}",
                'remove_url_params': generate_remove_url('max_precio_usd')
            })
        except ValueError:
            pass
    
    if min_precio_pesos:
        try:
            propiedades = propiedades.filter(precio_pesos__gte=float(min_precio_pesos))
            active_filters_display.append({
                'param_name': 'min_precio_pesos',
                'display_text': f"Precio Pesos Desde: $ {min_precio_pesos}",
                'remove_url_params': generate_remove_url('min_precio_pesos')
            })
        except ValueError:
            pass
    if max_precio_pesos:
        try:
            propiedades = propiedades.filter(precio_pesos__lte=float(max_precio_pesos))
            active_filters_display.append({
                'param_name': 'max_precio_pesos',
                'display_text': f"Precio Pesos Hasta: $ {max_precio_pesos}",
                'remove_url_params': generate_remove_url('max_precio_pesos')
            })
        except ValueError:
            pass

    if localidad:
        propiedades = propiedades.filter(localidad__icontains=localidad)
        active_filters_display.append({
            'param_name': 'localidad',
            'display_text': f"Localidad: {localidad}",
            'remove_url_params': generate_remove_url('localidad')
        })
    
    if dormitorios and dormitorios.isdigit():
        propiedades = propiedades.filter(dormitorios__gte=int(dormitorios))
        active_filters_display.append({
            'param_name': 'dormitorios',
            'display_text': f"Ambientes: {dormitorios}",
            'remove_url_params': generate_remove_url('dormitorios')
        })
    
    if banios and banios.isdigit():
        propiedades = propiedades.filter(banios__gte=int(banios))
        active_filters_display.append({
            'param_name': 'banios',
            'display_text': f"Baños: {banios}",
            'remove_url_params': generate_remove_url('banios')
        })
    
    if cocheras and cocheras.isdigit():
        propiedades = propiedades.filter(cocheras__gte=int(cocheras))
        active_filters_display.append({
            'param_name': 'cocheras',
            'display_text': f"Cocheras: {cocheras}",
            'remove_url_params': generate_remove_url('cocheras')
        })
    
    if acepta_mascotas == 'on' or acepta_mascotas == 'True':
        propiedades = propiedades.filter(acepta_mascotas=True)
        active_filters_display.append({
            'param_name': 'acepta_mascotas',
            'display_text': 'Acepta Mascotas',
            'remove_url_params': generate_remove_url('acepta_mascotas')
        })
        if tipo_mascota_permitida and tipo_mascota_permitida != 'no_especificado':
            tipo_mascota_label = dict(Propiedad.TIPO_MASCOTA_CHOICES).get(tipo_mascota_permitida, tipo_mascota_permitida)
            active_filters_display.append({
                'param_name': 'tipo_mascota_permitida',
                'display_text': f"Tipo Mascota: {tipo_mascota_label}",
                'remove_url_params': generate_remove_url('tipo_mascota_permitida')
            })
    
    if is_destacada == 'on' or is_destacada == 'True':
        propiedades = propiedades.filter(is_destacada=True)
        active_filters_display.append({
            'param_name': 'is_destacada',
            'display_text': 'Solo Destacadas',
            'remove_url_params': generate_remove_url('is_destacada')
        })

    propiedades = propiedades.order_by('-fecha_actualizacion')

    context = {
        'propiedades': propiedades,
        'page_title': 'Resultados de Búsqueda',
        # Pasamos los valores de los filtros de vuelta al template para que se mantengan
        'query': query,
        'tipo_propiedad_choices': Propiedad.TIPO_PROPIEDAD_CHOICES,
        'tipo_operacion_choices': Propiedad.TIPO_OPERACION_CHOICES,
        'tipo_mascota_choices': Propiedad.TIPO_MASCOTA_CHOICES,
        # Valores seleccionados para mantener el estado del formulario
        'selected_tipo_propiedad': tipo_propiedad,
        'selected_tipo_operacion': tipo_operacion,
        'selected_min_precio_usd': min_precio_usd,
        'selected_max_precio_usd': max_precio_usd,
        'selected_min_precio_pesos': min_precio_pesos,
        'selected_max_precio_pesos': max_precio_pesos,
        'selected_localidad': localidad,
        'selected_dormitorios': dormitorios,
        'selected_banios': banios,
        'selected_cocheras': cocheras,
        'selected_acepta_mascotas': 'True' if (acepta_mascotas == 'on' or acepta_mascotas == 'True') else None,
        'selected_tipo_mascota_permitida': tipo_mascota_permitida,
        'selected_is_destacada': 'True' if (is_destacada == 'on' or is_destacada == 'True') else None,
        'active_filters_display': active_filters_display,
        'request': request,
    }
    return render(request, 'web_app/busqueda.html', context)