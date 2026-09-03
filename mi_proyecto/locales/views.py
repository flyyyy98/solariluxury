import json
import os
import requests
from django.shortcuts import render
from django.conf import settings

def lista_locales(request):
    json_path = os.path.join(settings.BASE_DIR, 'data', 'locales.json')
    with open(json_path, 'r', encoding='utf-8-sig') as file:
        locales = json.load(file)
    
    total_locales = len(locales)
    
    for loc in locales:
        if 'Mall' in loc.get('nombre', ''):
            loc['badge_tipo'] = 'SOLARILUXURY FLAGSHIP'
            loc['tipo_tienda'] = 'Tienda Principal de Experiencia y Retiro'
            loc['zona'] = 'Mall Plaza La Serena - Nivel 2'
        else:
            loc['badge_tipo'] = 'SOLARILUXURY SHOWROOM'
            loc['tipo_tienda'] = 'Showroom Exclusivo y Entrega de Calzado / Streetwear'
            loc['zona'] = 'Balmaceda Centro La Serena'
        loc['estado'] = 'Abierto hoy • Retiro inmediato'

    context = {
        'locales': locales,
        'total_locales': total_locales,
    }
    return render(request, 'locales/lista_locales.html', context)

def informacion(request):
    valor_dolar = "No disponible"
    estado_api = "Sin conexión"
    try:
        response = requests.get('https://mindicador.cl/api/dolar', timeout=2.5)
        if response.status_code == 200:
            datos = response.json()
            valor_raw = datos['serie'][0]['valor']
            valor_dolar = f"{valor_raw:.2f}".replace('.', ',')
            estado_api = "Conexión en tiempo real exitosa"
        else:
            valor_dolar = "940,50 (Estimado)"
            estado_api = "Modo contingencia / API en espera"
    except Exception:
        valor_dolar = "940,50 (Estimado)"
        estado_api = "Modo contingencia / Fuera de línea"

    context = {
        'dolar': valor_dolar,
        'estado_api': estado_api,
    }
    return render(request, 'locales/informacion.html', context)
