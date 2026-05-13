import psycopg2
from datetime import datetime

def consultar_con_filtros():
    conn = psycopg2.connect(
        dbname="appdb", user="appuser", password="apppass",
        host="localhost", port="5432"
    )
    
    cur = conn.cursor()
    
    # Filtros (opcionales)
    fecha_filtro = input("Fecha (YYYY-MM-DD) o Enter para todos: ").strip()
    dni_filtro = input("DNI o Enter para todos: ").strip()
    empleado_filtro = input("Número empleado o Enter para todos: ").strip()
    
    # Construir query dinámica
    query = """
        SELECT nombre_archivo, datetime, dni, num_empleado, maquina, codigo, codificado
        FROM indice_texto_detalle 
        WHERE 1=1
    """
    params = []
    
    if fecha_filtro:
        query += " AND DATE(datetime) = %s"
        params.append(fecha_filtro)
    
    if dni_filtro:
        query += " AND dni = %s"
        params.append(dni_filtro)
    
    if empleado_filtro:
        query += " AND num_empleado = %s"
        params.append(empleado_filtro)
    
    query += " ORDER BY datetime DESC LIMIT 100"
    
    try:
        print(f"\nEjecutando: {query}")
        print(f"Parámetros: {params}")
        
        cur.execute(query, params)
        registros = cur.fetchall()
        
        print("\n" + "="*120)
        print("RESULTADOS FILTRADOS")
        print("="*120)
        print(f"{'Archivo':<25} {'Fecha':<20} {'DNI':<12} {'Empleado':<10} {'Máquina':<30} {'Código':<6} {'Codificado'}")
        print("-"*120)
        
        if registros:
            for registro in registros:
                print(f"{registro[0]:<25} {registro[1]:<20} {registro[2]:<12} {registro[3]:<10} {registro[4]:<30} {registro[5]:<6} {registro[6]}")
            print(f"\nTotal encontrados: {len(registros)}")
        else:
            print("No se encontraron registros")
            
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    consultar_con_filtros()
