from fastapi import FastAPI
from dotenv import load_dotenv
from openpyxl import Workbook
import csv
import os
import requests

load_dotenv()

app = FastAPI()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CSV_INPUT_PATH = os.getenv("CSV_INPUT_PATH")
EXCEL_OUTPUT_PATH = os.getenv("EXCEL_OUTPUT_PATH")


@app.get("/api/comparar-coordenadas")
def comparar_coordenadas():

    wb = Workbook()
    ws = wb.active
    ws.title = "Comparacion Coordenadas"

    headers = [
        "nombre_empresa",
        "direccion",
        "poblacion",
        "provincia",
        "codigo_postal",
        "latitud_fichero",
        "longitud_fichero",
        "direccion_google",        
        "estado_google",
        "resultado"
    ]

    ws.append(headers)

    with open(CSV_INPUT_PATH, newline='', encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        for row in reader:
                        
            direccion_completa = (
                f"{row['empresa']}, "
                f"{row['provincia']}, "
                f"{row['poblacion']}, "
                f"{row['codigo_postal']} "
                f"{row['direccion']}, "
                f"{row['latitud']} "
                f"{row['longitud']} " 
            )
        
            params = {
                "address": direccion_completa,
                "key": GOOGLE_API_KEY,
                "range" : "200",
                "client" : "legacy",
                "language" : "es",
                "country" : "ES",
                "forceGoogle" : "false"
            }

            headers = {
                   "Authorization": "AIzaSyClW8qIkU1wGS22O9ai3MwuS2UhjlwvziQ",
                    "Accept": "application/json"
            }

            response = requests.get(
                "https://aks.ontime.es/ws-calle-streetmap-api/api/v1/addresses?",
                params=params,
                headers=headers
            )

            print(response)

            """
            data = response.json()

            latitud_fichero = row.get("latitud", "").strip()
            longitud_fichero = row.get("longitud", "").strip()

            direccion_google = ""
            latitud_google = ""
            longitud_google = ""
            estado_google = data.get("status", "")
            resultado = "KO"

            if estado_google == "OK":

                result = data["results"][0]
                location = result["geometry"]["location"]

                direccion_google = result.get("formatted_address", "")
                latitud_google = location["lat"]
                longitud_google = location["lng"]

                try:
                    lat_file = round(float(latitud_fichero), 6)
                    lng_file = round(float(longitud_fichero), 6)

                    lat_google = round(float(latitud_google), 6)
                    lng_google = round(float(longitud_google), 6)

                    if lat_file == lat_google and lng_file == lng_google:
                        resultado = "OK"
                    else:
                        resultado = "KO"

                except:
                    resultado = "KO"

            print('--start---------------------------------------------------')
            print(direccion_google)
            print(resultado)
            print('--end---------------------------------------------------')

            ws.append([
                row.get("nombre_empresa", ""),
                row.get("direccion", ""),
                row.get("poblacion", ""),
                row.get("provincia", ""),
                row.get("codigo_postal", ""),
                latitud_fichero,
                longitud_fichero,
                direccion_google,
                latitud_google,
                longitud_google,
                estado_google,
                resultado
            ])
            """


    #os.makedirs(os.path.dirname(EXCEL_OUTPUT_PATH), exist_ok=True)
    #wb.save(EXCEL_OUTPUT_PATH)

    return {
        "status": "OK",
        "excel_generado": EXCEL_OUTPUT_PATH
    }
