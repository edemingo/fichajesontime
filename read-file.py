import os
from pathlib import Path


directorio = Path("/home/edmingo/Movimientos")

archivos = [f for f in directorio.iterdir() if f.is_file()]


archivos = [f for f in directorio.iterdir() if f.is_file()]


if not archivos:
    print("No hay archivos en el directorio")
else:
    archivo_mas_reciente = max(archivos, key=lambda f: f.stat().st_mtime)
    print("Archivo más reciente:", archivo_mas_reciente.name)

    with open(archivo_mas_reciente, "r", encoding="utf-8") as f:
        contenido = f.read()

    print(contenido)


