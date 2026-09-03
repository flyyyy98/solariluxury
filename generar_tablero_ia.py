import os
from PIL import Image

BASE_DIR = r"c:\Users\B1007\Documents\tienda"
IMG_DIR = os.path.join(BASE_DIR, "evidencias_ia")

f1 = Image.open(os.path.join(IMG_DIR, "Evidencia_1_Arquitectura_Django_JSON.png"))
f2 = Image.open(os.path.join(IMG_DIR, "Evidencia_2_Libreria_Requests_API_Dolar.png"))
f3 = Image.open(os.path.join(IMG_DIR, "Evidencia_3_Frontend_TRM_Theme_3D.png"))
f4 = Image.open(os.path.join(IMG_DIR, "Evidencia_4_Catalogo_Detalle_Responsivo.png"))

W, H = f1.size
GRID_W = W * 2 + 40
GRID_H = H * 2 + 40

grid = Image.new("RGB", (GRID_W, GRID_H), (10, 12, 16))
grid.paste(f1, (15, 15))
grid.paste(f2, (W + 25, 15))
grid.paste(f3, (15, H + 25))
grid.paste(f4, (W + 25, H + 25))

out_board = os.path.join(BASE_DIR, "Evidencias_IA_Tablero_Completo.png")
grid.save(out_board, quality=92)
grid.save(os.path.join(IMG_DIR, "Evidencias_IA_Tablero_Completo.png"), quality=92)
print(f"Tablero consolidado 2x2 generado en: {out_board}")
