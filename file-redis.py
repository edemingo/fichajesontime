from pathlib import Path
import redis

directorio = Path("/home/edmingo/Movimientos")
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

archivos = [f for f in directorio.iterdir() if f.is_file()]

if archivos:
    archivo_mas_reciente = max(archivos, key=lambda f: f.stat().st_mtime)


with open(archivo_mas_reciente, "r", encoding="utf-8") as f:
    r.hset("indice:archivo", "nombre_archivo", archivo_mas_reciente.name)
    for i, linea in enumerate(f, start=1):
        linea = linea.strip()
        if linea:
            r.hset("indice:archivo", f"linea:{i}", linea)


"""

    with open(archivo_mas_reciente, "r", encoding="utf-8") as f:
        contenido = f.read()

    r.hset("indice:archivos", mapping={
        "nombre": archivo_mas_reciente.name,
        "ruta": str(archivo_mas_reciente),
        "contenido": contenido
    })
"""
