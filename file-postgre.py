from pathlib import Path
import psycopg2

directorio = Path("/home/edmingo/Movimientos")

conn = psycopg2.connect(
    dbname="appdb",
    user="appuser",
    password="apppass",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

archivos = [f for f in directorio.iterdir() if f.is_file()]

operacion = 1
total_insertados = 0


for archivo_mas_reciente in archivos:

    cur.execute(
        "DELETE FROM indice_texto_detalle WHERE nombre_archivo = %s",
        (archivo_mas_reciente.name,)
    )

    with open(archivo_mas_reciente, "r", encoding="utf-8") as f:
        for num_linea, linea in enumerate(f, start=1):
            linea = linea.strip()
            if linea:
                campos = linea.split("|")
                
                if len(campos) >= 6:
                    datetime_str, dni, num_empleado, maquina, codigo, codificado = campos[:6]
                    
                    cur.execute("""
                        INSERT INTO indice_texto_detalle (nombre_archivo, num_linea, datetime, dni, num_empleado, maquina, codigo, codificado)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        archivo_mas_reciente.name, 
                        num_linea, 
                        datetime_str, 
                        dni, 
                        num_empleado, 
                        maquina, 
                        codigo, 
                        codificado

                        ))
                    


    conn.commit()
    print(f"Total líneas insertadas: {total_insertados}")

cur.close()
conn.close()


"""
if archivos:
    archivo_mas_reciente = max(archivos, key=lambda f: f.stat().st_mtime)

    with open(archivo_mas_reciente, "r", encoding="utf-8") as f:
        for i, linea in enumerate(f, start=1):
            linea = linea.strip()
            if linea:
                cur.execute(
                    "" "
                    INSERT INTO indice_texto (nombre_archivo, num_linea, contenido)
                    VALUES (%s, %s, %s)
                    "" ",
                    (archivo_mas_reciente.name, i, linea)
                )

    conn.commit()

cur.close()
conn.close()
"""
