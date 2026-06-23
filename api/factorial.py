import requests
import os
from dotenv import load_dotenv

class Factorial:


    def __init__(self, ingest):
        self.ingest = ingest
        # Cargar variables desde config.env
        load_dotenv('config.env')
        self.url = os.getenv('apiURL') + os.getenv('apiVersion') + "/"
        self.apiKey = os.getenv('apikey')

 

    def getAllEmployees(self):        
        theData = self.obtener_todos_los_empleados()        
        self.ingest.insertar_empleado(theData)
        return theData
    

    def getAllEmployees100(self):
        theRequest = "resources/employees/employees"
        theData = self.consumir_api(theRequest)        
        self.ingest.insertar_empleado(theData)
        return theData
    
    


    def getTheEmployeeById(self, id=None):
        theRequest = f"resources/employees/employees/{id}"
        return self.consumir_api(theRequest)


    def getShiftsByEmployee(self, idEmpleado, fechaInicio, fechaFin):
        
        theRequest = (
                f"resources/attendance/shifts"
                f"?employee_ids[]={idEmpleado}"
                f"&start_on={fechaInicio}"
                f"&end_on={fechaFin}"
                f"&half_day=false"
                f"&sort_created_at_asc=false"
            )
        
      
    # "/resources/attendance/shifts?employee_ids[]=2716809&start_on=2026-04-29&end_on=2026-04-29&half_day=false&sort_created_at_asc=false"        
        return self.consumir_api(theRequest)
    
    

    def getAllShiftsInDay(self, fechaInicio):
        theRequest = (
                f"resources/attendance/shifts"
                f"?start_on={fechaInicio}"
                f"&half_day=false"
                f"&sort_created_at_asc=true"
            )
            
        # "/resources/attendance/shifts?start_on=2026-05-12&half_day=false&sort_created_at_asc=true"
        return self.consumir_api(theRequest)


    def consumir_api(self, theRequest):
        headers = {
            "x-api-key": self.apiKey,
            "Accept": "application/json"
        }

        myUrl = self.url + "" + theRequest

        print(f"Consumiendo API: {myUrl}")
        
        try:
            response = requests.get(myUrl, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error consumiendo la API: {e}")
            return None


    def obtener_todos_los_empleados(self):
        todos = []
        page = 1
        has_next_page = True

        headers = {
            "x-api-key": self.apiKey,
            "Accept": "application/json"
        }

        while has_next_page:
            params = {
                "per_page": 100,
                "page": page,
                "only_active": "false"
            }

            response = requests.get(
                f"{self.url}/resources/employees/employees",
                headers=headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            todos.extend(data.get("data", []))
            has_next_page = data.get("meta", {}).get("has_next_page", False)
            page += 1

        return todos


"""

curl --request GET \
     --url 'https://api.factorialhr.com/api/2025-04-01/resources/employees/employees?access_ids[]=3593572&only_active=false&only_managers=false' \
     --header 'accept: application/json' \
     --header 'x-api-key: eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NjAwMTc4OTEsImV4cCI6MjA3NTU4NzQxMSwianRpIjoiNjM5YzljZDAtN2RiYy00OGM1LWE1ZjAtZTYwOTI3MDY1NmYyIiwiY2VsbCI6ImF3cy1wcm9kLWV1Y2VudHJhbDEtZ2xvYjAxIiwiY29tcGFueV9pZCI6Mjk4ODk5fQ.Plu09fLr2HXEMYI8JRfyoVLkey5dZHRPqyKQ2zVO0sxDLOIm65KMBjPgLPLCXpMuoD0-RRLuHVWkvBcd6IeSYw'

curl --request GET \
     --url 'https://api.factorialhr.com/api/2025-04-01/resources/attendance/shifts?employee_ids[]=3150762&start_on=2026-04-28&end_on=2026-04-28&half_day=false&sort_created_at_asc=false' \
     --header 'accept: application/json' \
     --header 'x-api-key: eyJraWQiOiJmYWN0b3JpYWwtaWQiLCJhbGciOiJFUzI1NiJ9.eyJpYXQiOjE3NjAwMTc4OTEsImV4cCI6MjA3NTU4NzQxMSwianRpIjoiNjM5YzljZDAtN2RiYy00OGM1LWE1ZjAtZTYwOTI3MDY1NmYyIiwiY2VsbCI6ImF3cy1wcm9kLWV1Y2VudHJhbDEtZ2xvYjAxIiwiY29tcGFueV9pZCI6Mjk4ODk5fQ.Plu09fLr2HXEMYI8JRfyoVLkey5dZHRPqyKQ2zVO0sxDLOIm65KMBjPgLPLCXpMuoD0-RRLuHVWkvBcd6IeSYw'
"""

