import os
import sys
import shutil

BASE_DIR = r"c:\Users\B1007\Documents\tienda"
sys.path.insert(0, os.path.join(BASE_DIR, "mi_proyecto"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mi_proyecto.settings")

import django
django.setup()

from django.test import Client

client = Client()
DOCS_DIR = os.path.join(BASE_DIR, "docs")

if os.path.exists(DOCS_DIR):
    shutil.rmtree(DOCS_DIR)
os.makedirs(DOCS_DIR, exist_ok=True)

# Copiar estáticos a docs/static
static_src = os.path.join(BASE_DIR, "mi_proyecto", "static")
static_dest = os.path.join(DOCS_DIR, "static")
shutil.copytree(static_src, static_dest, dirs_exist_ok=True)

routes = [
    ("/", os.path.join(DOCS_DIR, "index.html")),
    ("/productos/", os.path.join(DOCS_DIR, "productos", "index.html")),
    ("/locales/", os.path.join(DOCS_DIR, "locales", "index.html")),
    ("/locales/informacion/", os.path.join(DOCS_DIR, "locales", "informacion", "index.html")),
]

for i in range(1, 14):
    routes.append((f"/productos/{i}/", os.path.join(DOCS_DIR, "productos", str(i), "index.html")))

REPO_PREFIX = "/solariluxury"

for route, out_path in routes:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    response = client.get(route)
    if response.status_code == 200:
        html = response.content.decode("utf-8")
        
        # Adaptar para GitHub Pages
        html = html.replace('href="/static/', f'href="{REPO_PREFIX}/static/')
        html = html.replace('src="/static/', f'src="{REPO_PREFIX}/static/')
        html = html.replace("url('/static/", f"url('{REPO_PREFIX}/static/")
        html = html.replace('href="/productos/', f'href="{REPO_PREFIX}/productos/')
        html = html.replace('href="/locales/', f'href="{REPO_PREFIX}/locales/')
        html = html.replace('href="/"', f'href="{REPO_PREFIX}/"')
        html = html.replace("window.location.href='/productos/", f"window.location.href='{REPO_PREFIX}/productos/")
        html = html.replace("window.location.href = '/productos/'", f"window.location.href = '{REPO_PREFIX}/productos/'")
        html = html.replace("window.location.href='/productos/'", f"window.location.href='{REPO_PREFIX}/productos/'")
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Exportado: {route} -> {out_path}")
    else:
        print(f"Error {response.status_code} en {route}")

# Crear .nojekyll
with open(os.path.join(DOCS_DIR, ".nojekyll"), "w", encoding="utf-8") as f:
    f.write("")

print("Exportacion completa para GitHub Pages en docs/")
