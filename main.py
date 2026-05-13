from pathlib import Path
import psycopg2

directorio = Path("/home/edmingo/Movimientos")
archivos = []
cur = None
conn = None

def databaseConnect():
    conn = psycopg2.connect(
        dbname="appdb",
        user="appuser",
        password="apppass",
        host="localhost",
        port="5432"
    )
    return conn



def databaseDisconnect(conn):
    conn.close()




def getArchivos():
    archivos = [f for f in directorio.iterdir() if f.is_file()]
    return archivos

def procesarArchivos(conn, cur):
    resultado = 0
    archivos = getArchivos()
    total_insertados = 0

    for archivo_mas_reciente in archivos:

        insertRegistroImportados(conn,archivo_mas_reciente)

        with open(archivo_mas_reciente, "r", encoding="utf-8") as f:

            total_insertados = 0

            for num_linea, linea in enumerate(f, start=1):
                total_insertados = total_insertados + 1
                linea = linea.strip()

                insertArchivos(conn, cur, linea, archivo_mas_reciente, num_linea)

        print(f"Total líneas insertadas: {total_insertados}")

    return resultado

def insertRegistroImportados(conn, archivo_mas_reciente):
    curExports = conn.cursor()

    curExports.execute("""
                INSERT INTO ficheros_exportados (nombre_fichero)
                VALUES (%s)
                """, (
                    archivo_mas_reciente.name, 
                ))

    conn.commit()

    curExports.close()


def insertArchivos(conn, cur, linea, archivo_mas_reciente, num_linea):
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



def theMain():
    conn = databaseConnect()
    cur = conn.cursor()

    procesarArchivos(conn, cur)

    cur.close()
    conn.close()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    theMain()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
