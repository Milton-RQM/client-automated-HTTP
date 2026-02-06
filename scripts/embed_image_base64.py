import base64
from pathlib import Path

IMG_PATH = Path('04_etl_pentaho/diagramas/t_load_kpi.png')
README = Path('README.md')

MAX_BYTES = 200_000  # safety limit ~200 KB

if not IMG_PATH.exists():
    print(f"ERROR: imagen no encontrada: {IMG_PATH}")
    raise SystemExit(1)

size = IMG_PATH.stat().st_size
print(f"Imagen encontrada ({size} bytes)")
if size > MAX_BYTES:
    print(f"ERROR: Imagen demasiado grande para inlining ({size} > {MAX_BYTES} bytes).\nConsidera subir la imagen al repo y usar la ruta relativa o reducir su tamaño.")
    raise SystemExit(2)

b = IMG_PATH.read_bytes()
b64 = base64.b64encode(b).decode('ascii')
data_uri = f"data:image/png;base64,{b64}"

text = README.read_text(encoding='utf-8')
old = '![Transformación t_load_kpi](04_etl_pentaho/diagramas/t_load_kpi.png)'
if old not in text:
    print('ERROR: marcador original no encontrado en README.md')
    raise SystemExit(3)

new = f'![Transformación t_load_kpi]({data_uri})'
text = text.replace(old, new)
README.write_text(text, encoding='utf-8')
print('README actualizado con data-URI (base64).')
