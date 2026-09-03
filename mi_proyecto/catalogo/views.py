import json
import os
from django.shortcuts import render, Http404
from django.conf import settings

def get_productos_data():
    json_path = os.path.join(settings.BASE_DIR, 'data', 'productos.json')
    with open(json_path, 'r', encoding='utf-8-sig') as file:
        productos = json.load(file)
    for prod in productos:
        prod['precio_formateado'] = f"${prod['precio']:,}".replace(',', '.')
    return productos

def inicio(request):
    """Pantalla Gateway / Entrada oficial con Logo GIF 3D, reloj en vivo y menú en español"""
    return render(request, 'catalogo/inicio.html')

def lista_productos(request):
    """Catálogo adaptativo estilo TRM Shopify con sidebar de categorías y productos reales"""
    productos = get_productos_data()
    categoria_seleccionada = request.GET.get('categoria', 'TODOS').upper()
    
    if categoria_seleccionada and categoria_seleccionada != 'TODOS':
        productos_filtrados = [p for p in productos if p.get('categoria', '').upper() == categoria_seleccionada]
    else:
        productos_filtrados = productos

    categorias = [
        'TODOS',
        'ZAPATILLAS (SNEAKERS)',
        'POLERONES (HOODIES)',
        'POLERAS',
        'PANTALONES FLARED',
        'PASAMONTAÑAS',
        'BOLSOS Y MORRALES',
        'ACCESORIOS'
    ]

    context = {
        'productos': productos_filtrados,
        'total_productos': len(productos_filtrados),
        'categorias': categorias,
        'categoria_actual': categoria_seleccionada,
    }
    return render(request, 'catalogo/productos.html', context)

def detalle_producto(request, producto_id):
    """Detalle del producto en español con galería de miniaturas, tallas interactivas y pasarela de pago"""
    productos = get_productos_data()
    producto = next((p for p in productos if p['id'] == producto_id), None)
    
    if not producto:
        raise Http404("Producto no encontrado")

    ids = [p['id'] for p in productos]
    curr_idx = ids.index(producto_id)
    prev_id = ids[curr_idx - 1] if curr_idx > 0 else ids[-1]
    next_id = ids[curr_idx + 1] if curr_idx < len(ids) - 1 else ids[0]

    context = {
        'prod': producto,
        'prev_id': prev_id,
        'next_id': next_id,
    }
    return render(request, 'catalogo/detalle_producto.html', context)
