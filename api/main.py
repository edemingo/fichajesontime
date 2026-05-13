from unittest import result

from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from starlette.responses import HTMLResponse 
from ingest import Ingest
from factorial import Factorial
from scheduler import Scheduler
from stats import Stats
from models import Base, FicherosExportados, IndiceTextoDetalle, engine, SessionLocal
from contextlib import asynccontextmanager
from sqlalchemy import text
from datetime import datetime

Base.metadata.create_all(bind=engine)
ingest = Ingest()
app = FastAPI()
fact = Factorial(ingest)

scheduler = Scheduler(ingest)
schedulerTime = 5 # minutos

stats = Stats()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # print("\n>>>>>> Scheduler para el refreso de hoy programado a cada " + str(schedulerTime) + " minutos <<<<<<\n")
    scheduler.start(schedulerTime)
    yield
    scheduler.stop()

app = FastAPI(lifespan=lifespan)

# --- Servir archivos estáticos (CSS, JS, etc.) ---
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# --- Plantillas HTML (Jinja2) ---
templates = Jinja2Templates(directory="web/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def web_index():
    # Sirve el HTML directamente desde templates como texto plano
    with open("web/templates/index.html", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)


@app.get("/empleados")
def web_index():
    # Sirve el HTML directamente desde templates como texto plano
    with open("web/templates/empleados.html", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)


@app.get("/ficheros")
def web_index():
    # Sirve el HTML directamente desde templates como texto plano
    with open("web/templates/ficheros.html", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)

@app.get("/informes")
def web_index():
    # Sirve el HTML directamente desde templates como texto plano
    with open("web/templates/informes.html", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)



@app.get("/api/ficheros", response_model=List[dict])
def listar_ficheros():

    ficheros = ingest.getFicherosDorlet()
    return [
        {            
            "nombre_fichero": f,
        }
        for f in ficheros
    ]



@app.post("/api/ficheros", status_code=201)
def crear_fichero(nombre: str, db: Session = Depends(get_db)):
    nuevo = FicherosExportados(nombre_fichero=nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {
        "id": nuevo.id,
        "nombre_fichero": nuevo.nombre_fichero,
        "fecha_exportacion": nuevo.fecha_exportacion,
    }


@app.get('/api/actualizarHoy')
def actualizarHoy(db: Session = Depends(get_db)):
    ingest.updateLastFile()


@app.get('/api/actualizarFromFile')
def actualizarFromFile(nombre_fichero: str, db: Session = Depends(get_db)):
    ingest.updateFromFile(nombre_fichero)


@app.get('/api/verFichero')
def verFichero(nombre_fichero: str):
    return ingest.getFicheroContent(nombre_fichero)



@app.get("/api/indice", response_model=List[dict])
def listar_indice(
    num_empleado: Optional[str] = Query(None, description="Filtrar por número de empleado"),
    dni: Optional[str] = Query(None, description="Filtrar por DNI"),
    fecha: Optional[str] = Query(None, description="Filtrar por fecha (campo datetime, formato texto)"),
    fecha_hasta: Optional[str] = Query(None, description="Filtrar por fecha hasta (campo datetime,  formato texto)"),
    db: Session = Depends(get_db),
):
    # Construir consulta SQL dinámica
    sql = "SELECT e.access_id, e.id as emp_id, e.first_name, e.last_name, i.* FROM indice_texto_detalle i LEFT JOIN empleados e ON i.dni = e.identifier WHERE 1=1"
    params = {}

    if num_empleado is not None:
        sql += " AND i.num_empleado = :num_empleado"
        params["num_empleado"] = num_empleado
    
    if dni is not None:
        sql += " AND i.dni = :dni"
        params["dni"] = dni

    if fecha is not None and fecha_hasta is None:
        sql += " AND to_date(split_part(i.datetime, ' ', 1), 'YYYY/MM/DD') = :fecha"
        params["fecha"] = f"%{fecha}%"    

    if fecha is None and fecha_hasta is not None:
        sql += " AND to_date(split_part(i.datetime, ' ', 1), 'YYYY/MM/DD') <= :fecha_hasta"
        params["fecha_hasta"] = fecha_hasta

    if fecha_hasta is not None and fecha is not None:
        sql += " AND to_date(split_part(i.datetime, ' ', 1), 'YYYY/MM/DD') BETWEEN DATE :fecha AND DATE :fecha_hasta"        
        params["fecha"] = fecha    
        params["fecha_hasta"] = fecha_hasta
    
    
    # Ordenar
    if num_empleado:
        sql += " ORDER BY i.num_empleado DESC, to_timestamp(datetime, 'YYYY/MM/DD HH24:MI:SS') ASC"
    elif fecha and not num_empleado:
        sql += " ORDER BY to_timestamp(datetime, 'YYYY/MM/DD HH24:MI:SS') DESC"
    else:
        sql += " ORDER BY to_timestamp(datetime, 'YYYY/MM/DD HH24:MI:SS')  DESC"
    
    result = db.execute(text(sql), params).fetchall()
    
    return [
        {
            "id": r.id,
            "Nombre": r.first_name,
            "Apellido": r.last_name,
            "Access_id": r.access_id,
            "emp_id": r.emp_id,
            "nombre_archivo": r.nombre_archivo,
            "num_linea": r.num_linea,
            "datetime": r.datetime,
            "dni": r.dni,
            "num_empleado": r.num_empleado,
            "maquina": r.maquina,
            "codigo": r.codigo,
            "codificado": r.codificado,
            "exportado": r.exportado,
        }
        for r in result
    ]



@app.get("/api/empleado", status_code=200)
def get_empleado(id: int):
    data = fact.getTheEmployeeById(id)
    return data


@app.get("/api/insertAllEmpleados", status_code=201)
def get_empleados():
    myData = fact.getAllEmployees()    
    return myData


@app.get("/api/empleados", status_code=200)
def get_empleadosList(
    id: int = Query(None, description="Filtrar por ID del empleado"),
    identifier : str = Query(None, description="Filtrar por DNI del empleado"),
    offset: int = Query(0, description="Offset para paginación"),
    limit: int = Query(10, description="Límite de registros"),
    num_empleado: Optional[str] = Query(None, description="Filtrar por número de empleado"),
    dni: Optional[str] = Query(None, description="Filtrar por DNI"),
    nombre: Optional[str] = Query(None, description="Filtrar por nombre"),
    email: Optional[str] = Query(None, description="Filtrar por email"),    
    status: Optional[str] = Query(None, description="Filtrar por estado (active/unactive)"),
    db: Session = Depends(get_db),
):
    sql = "WITH total AS (SELECT COUNT(*) AS total_count FROM empleados WHERE 1=1) "
    sql += "SELECT e.id, e.full_name, e.email, e.active, e.is_terminating, e.terminated_on, t.total_count "
    sql += "FROM empleados e CROSS JOIN total t WHERE 1=1"  
    params = {}


    if id is not None:
        sql += " AND e.id = :id"
        params["id"] = id

    if identifier is not None:
        sql += " AND e.identifier = :identifier"
        params["identifier"] = identifier

    if status is not None:
        if status == "active":
            sql += " AND active = true"
        elif status == "unactive":
            sql += " AND active = false"

    if num_empleado is not None:
        sql += " AND company_identifier = :num_empleado"
        params["num_empleado"] = num_empleado

    if dni is not None:
        sql += " AND identifier = :dni"
        params["dni"] = dni

    if nombre is not None:
        sql += " AND full_name ILIKE :nombre"
        params["nombre"] = f"%{nombre}%"

    if email is not None:
        sql += " AND email ILIKE :email"
        params["email"] = f"%{email}%"



    sql += " ORDER BY e.id OFFSET :offset LIMIT :limit"
    params["offset"] = offset
    params["limit"] = limit
    
    result = db.execute(text(sql), params).fetchall()
    
    data = [
        {
            "id": r.id,
            "full_name": r.full_name,
            "email": r.email,
            "active": r.active,
            "is_terminating": r.is_terminating,
            "terminated_on": r.terminated_on,
        }
        for r in result
    ]
    
    total = result[0].total_count if result else 0
    
    return {"data": data, "total": total}

@app.get("/api/empleadoShifts", status_code=200)
def get_empleadoShifts(idEmpleado: int, fechaInicio: str, fechaFin: str):  
    data = fact.getShiftsByEmployee(idEmpleado=idEmpleado, fechaInicio=fechaInicio, fechaFin=fechaFin)    
    return data

@app.get("/api/getAllShiftsInDay", status_code=200)
def get_allShiftsInDay(fechaInicio: str, db: Session = Depends(get_db)):  

    data = fact.getAllShiftsInDay(fechaInicio=fechaInicio)    
    ingest.insertShiftEmpleadoDia(obj=data, fecha=fechaInicio)

    return data


@app.post("/indice", status_code=201)
def crear_indice(
    nombre_archivo: str,
    num_linea: int,
    datetime: str,
    dni: str,
    num_empleado: str,
    maquina: str,
    codigo: str,
    codificado: str,
    exportado: int = 0,
    db: Session = Depends(get_db),
):
    sql = text("""
        INSERT INTO indice_texto_detalle 
        (nombre_archivo, num_linea, datetime, dni, num_empleado, maquina, codigo, codificado, exportado)
        VALUES (:nombre_archivo, :num_linea, :datetime, :dni, :num_empleado, :maquina, :codigo, :codificado, :exportado)
        RETURNING id
    """)
    result = db.execute(sql, {
        "nombre_archivo": nombre_archivo,
        "num_linea": num_linea,
        "datetime": datetime,
        "dni": dni,
        "num_empleado": num_empleado,
        "maquina": maquina,
        "codigo": codigo,
        "codificado": codificado,
        "exportado": exportado,
    }).fetchone()
    
    db.commit()
    return {"id": result.id}



@app.get("/api/fichajeshora", status_code=200)
def get_fichajeshora(fecha: Optional[str] = Query(None, description="Filtrar por fecha (campo datetime, formato texto)"),
    db: Session = Depends(get_db),):

        query = """
        WITH movimientos_hora AS (
            SELECT
                date_trunc('hour', to_timestamp(datetime, 'YYYY/MM/DD HH24:MI:SS')) AS hora,
                COUNT(*) FILTER (WHERE codigo = '01') AS entradas,
                COUNT(*) FILTER (WHERE codigo = '51') AS salidas
            FROM public.indice_texto_detalle
            WHERE codigo IN ('01', '51')
            AND to_timestamp(datetime, 'YYYY/MM/DD HH24:MI:SS')::date = %s
            GROUP BY hora
        )
        SELECT
            to_char(hora, 'HH24:00') AS hora,
            entradas,
            salidas,
            SUM(entradas - salidas) OVER (
                ORDER BY hora
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS personas_dentro
        FROM movimientos_hora
        ORDER BY hora;
        """
        result = db.execute(query)

        return {result.keys()[0]: [dict(row) for row in result]}
    

@app.get("/api/fichajesmediahora", status_code=200)
def get_fichajes_media_hora(
    fecha: Optional[str] = Query(None),
    horaDesde: Optional[str] = Query("06:00"),
    horaHasta: Optional[str] = Query("23:59"),
    db: Session = Depends(get_db),
):
    return stats.fichjesMediaHora(db=db,fecha=fecha,horaDesde=horaDesde,horaHasta=horaHasta)


@app.get("/api/fichajesComedor", status_code=200)
def get_fichajes_media_hora(
    fecha: Optional[str] = Query(None),    
    db: Session = Depends(get_db),
):
    return stats.fichajesComedor(db=db,fecha=fecha)


@app.get("/api/totalizadorFichajes", status_code=200)
def get_fichajes_media_hora(
    fecha: Optional[str] = Query(None),    
    db: Session = Depends(get_db),
):
    return stats.totalizadorFichajesDia(db=db,fecha=fecha)




@app.get("/api/fichajesmediahoraOld", status_code=200)
def get_fichajes_media_hora(
    fecha: Optional[str] = Query(None),
    horaDesde: Optional[str] = Query("06:00"),
    horaHasta: Optional[str] = Query("23:00"),
    db: Session = Depends(get_db),
):
    if not fecha:
        raise HTTPException(status_code=400, detail="El parámetro 'fecha' es obligatorio")

    fechadesde = f"{fecha} {horaDesde}:00"
    fechahasta = f"{fecha} {horaHasta}:00"

    query = text("""
        WITH intervalos AS (
            SELECT generate_series(
                CAST(:fechadesde AS timestamp),
                CAST(:fechahasta AS timestamp),
                INTERVAL '30 minutes'
            ) AS media_hora
        ),
        movimientos AS (
            SELECT
                date_trunc('hour', ts)
                + floor(date_part('minute', ts) / 30) * interval '30 minutes' AS media_hora,
                COUNT(*) FILTER (WHERE codigo = '01') AS entradas,
                COUNT(*) FILTER (WHERE codigo = '51') AS salidas
            FROM (
                SELECT
                    codigo,
                    to_timestamp(datetime, 'YYYY/MM/DD HH24:MI:SS') AS ts
                FROM public.indice_texto_detalle
                WHERE codigo IN ('01', '51')
                  AND to_timestamp(datetime, 'YYYY/MM/DD HH24:MI:SS')::date = CAST(:fecha AS date)
            ) t
            GROUP BY media_hora
        )
        SELECT
            to_char(i.media_hora, 'HH24:MI') AS hora,
            COALESCE(m.entradas, 0) AS entradas,
            COALESCE(m.salidas, 0) AS salidas,
            SUM(COALESCE(m.entradas, 0) - COALESCE(m.salidas, 0)) OVER (
                ORDER BY i.media_hora
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS personas_dentro
        FROM intervalos i
        LEFT JOIN movimientos m ON i.media_hora = m.media_hora
        ORDER BY i.media_hora;
    """)

    result = db.execute(query, {
        "fecha": fecha,
        "fechadesde": fechadesde,
        "fechahasta": fechahasta,
    })

    rows = result.mappings().all()

    return {
        "labels": [row["hora"] for row in rows],
        "entradas": [row["entradas"] for row in rows],
        "salidas": [row["salidas"] for row in rows],
        "personas_dentro": [row["personas_dentro"] for row in rows],
    }


