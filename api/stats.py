from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, Query, Request
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text

class Stats:
    
    def __init__(self):
        self.conn = None
        self.cur = None


    def fichjesMediaHora(self, db : Session, fecha: Optional[str] = Query(None), horaDesde: Optional[str] = Query("07:00"), horaHasta: Optional[str] = Query("22:00")):
        
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
    



    def fichajesComedor(self, db : Session, fecha: Optional[str] = Query(None)):

        if not fecha:
            raise HTTPException(status_code=400, detail="El parámetro 'fecha' es obligatorio")
        

        query = text("""
        SELECT COUNT(*) AS personas_en_comedor
        FROM (
            SELECT dni, COUNT(*) AS num_fichajes
            FROM indice_texto_detalle
            WHERE codigo = '02'
            AND TO_TIMESTAMP(datetime, 'YYYY/MM/DD HH24:MI:SS')::date = CAST(:fecha AS date)
            GROUP BY dni
            HAVING COUNT(*) % 2 = 1
        ) en_comedor;
         """)
        
        result = db.execute(query, {
            "fecha": fecha,          
        })
        
        rows = result.mappings().all()

        return {            
            "personas": [row["personas_en_comedor"] for row in rows],
        }
    

        
    def totalizadorFichajesDia(self, db : Session, fecha: Optional[str] = Query(None)):

        if not fecha:
            raise HTTPException(status_code=400, detail="El parámetro 'fecha' es obligatorio")

        query = text(""" 
        WITH base AS (
            SELECT
                codigo,
                dni,
                to_timestamp(datetime, 'YYYY/MM/DD HH24:MI:SS') AS ts
            FROM public.indice_texto_detalle
            WHERE codigo IN ('01', '51', '02')
            AND to_timestamp(datetime, 'YYYY/MM/DD HH24:MI:SS')::date = CAST(:fecha AS date)
        ), acumulado AS (
            SELECT
                ts,
                SUM(
                    CASE 
                        WHEN codigo = '01' THEN 1
                        WHEN codigo = '51' THEN -1
                        ELSE 0
                    END
                ) OVER (
                    ORDER BY ts
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ) AS empleados_dentro
            FROM base
        )  
        SELECT
            -- Máximo de empleados simultáneamente dentro del edificio
            (SELECT MAX(empleados_dentro) FROM acumulado) AS max_empleados_dentro,
            -- Total fichajes entrada del día
            (SELECT COUNT(*) FROM base WHERE codigo = '01') AS total_fichajes_entrada,
            -- Total fichajes salida del día
            (SELECT COUNT(*) FROM base WHERE codigo = '51') AS total_fichajes_salida,
            -- Total fichajes comedor del día
            (SELECT COUNT(*)/2 FROM base WHERE codigo = '02') AS total_fichajes_comedor;
        """)

        result = db.execute(query, {
            "fecha": fecha,          
        })
        
        rows = result.mappings().all()

        return {            
            "dentro": [row["max_empleados_dentro"] for row in rows],
            "entrada": [row["total_fichajes_entrada"] for row in rows],
            "salida": [row["total_fichajes_salida"] for row in rows],
            "comedor": [row["total_fichajes_comedor"] for row in rows],

        }