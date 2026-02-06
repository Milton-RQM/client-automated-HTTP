from pathlib import Path
# Asegura que un directorio exista; si no, lo crea..
def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
