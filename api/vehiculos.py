import requests


class FactorialVehicleAPI:

    # http://172.27.35.250:8081/DASS/Personal/Persons/02709392S

    def __init__(self, host, port):
        """Inicializa la configuración base del API de Dorlet."""
        self.host = "172.27.35.250"
        self.port = "8081"
        self.base64Key = "ZmFjdG9yaWFsOk9udGltZS4yMDI2Kg=="
        self.base_url = f"http://{self.host}:{self.port}/DASS/Vehicle Management"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.base64Key}"
        }

    def search_vehicles(self, filters=None, offset=None, limit=None):
        """Obtiene datos de vehículos aplicando filtros y paginación.

        URL: POST /DASS/Vehicle Management/VehiclesSearch 
        """
        url = f"{self.base_url}/VehiclesSearch"
        params = {}
        if offset is not None:
            params["offset"] = offset  # 
        if limit is not None:
            params["limit"] = limit  # [cite: 34]

        # VehicleFilters payload [cite: 34]
        payload = filters if filters else {}

        response = requests.post(
            url, headers=self.headers, params=params, json=payload
        )
        if response.status_code == 200:
            return response.json()  # Retorna List of Vehicle [cite: 34]
        else:
            response.raise_for_status()

    def get_vehicle(self, license_plate):
        """Obtiene los datos detallados de un vehículo específico por su matrícula[cite: 34].

        URL: GET /DASS/Vehicle Management/Vehicles/<LicensePlate> [cite: 34]
        """
        url = f"{self.base_url}/Vehicles/{license_plate}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()  # Retorna Vehicle [cite: 34]
        elif response.status_code == 404:
            return (
                None  # Vehículo no encontrado [cite: 34]
            )
        else:
            response.raise_for_status()

    def create_vehicle(self, vehicle_data):
        """Da de alta un nuevo vehículo en el sistema[cite: 38].

        URL: POST /DASS/Vehicle Management/Vehicles [cite: 36]
        """
        url = f"{self.base_url}/Vehicles"
        response = requests.post(
            url, headers=self.headers, json=vehicle_data
        )  # vehicle_data mapea a la estructura 'Vehicle' [cite: 36]
        if response.status_code == 201:
            return response.json()  # Retorna Vehicle creado [cite: 37]
        elif response.status_code == 409:
            raise Exception(
                "Conflict: El vehículo ya existe."
            )  # El vehículo ya existe [cite: 37]
        else:
            response.raise_for_status()

    def update_vehicle(self, license_plate, vehicle_data):
        """Modifica los datos de un vehículo existente[cite: 40].

        URL: POST /DASS/Vehicle Management/Vehicles/<LicensePlate> [cite: 39]
        """
        url = f"{self.base_url}/Vehicles/{license_plate}"
        response = requests.post(url, headers=self.headers, json=vehicle_data)
        if response.status_code == 200:
            return True  # Modificación correcta [cite: 40]
        elif response.status_code == 404:
            raise Exception("Not Found: El vehículo no existe.")  # [cite: 40]
        else:
            response.raise_for_status()

    def delete_vehicle(self, license_plate):
        """Elimina un vehículo del sistema por su matrícula[cite: 40].

        URL: DELETE /DASS/Vehicle Management/Vehicles/<LicensePlate> [cite: 40]
        """
        url = f"{self.base_url}/Vehicles/{license_plate}"
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 200:
            return True  # Vehículo eliminado con éxito [cite: 40]
        elif response.status_code == 404:
            raise Exception("Not Found: El vehículo no existe.")  # [cite: 40]
        else:
            response.raise_for_status()

    def get_drivers(self, license_plate):
        """Obtiene la lista de personas autorizadas a conducir el vehículo[cite: 40].

        URL: GET /DASS/Vehicle Management/Vehicles/<LicensePlate>/Drivers [cite: 40]
        """
        url = f"{self.base_url}/Vehicles/{license_plate}/Drivers"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()  # Retorna List of Person [cite: 40]
        elif response.status_code == 404:
            raise Exception("Not Found: El vehículo no existe.")  # [cite: 40]
        else:
            response.raise_for_status()

    def add_driver(self, license_plate, document_id):
        """Añade un conductor autorizado a un vehículo mediante su DNI o Pasaporte[cite: 41].

        URL: POST /DASS/Vehicle Management/Vehicles/<LicensePlate>/Drivers/<DocumentId> [cite: 40, 41]
        """
        url = f"{self.base_url}/Vehicles/{license_plate}/Drivers/{document_id}"
        response = requests.post(url, headers=self.headers)
        if response.status_code == 200:
            return True  # Conductor añadido con éxito [cite: 41]
        elif response.status_code == 404:
            raise Exception(
                "Not Found: El vehículo o la persona no existen."
            )  # [cite: 41]
        else:
            response.raise_for_status()

    def remove_driver(self, license_plate, document_id):
        """Desasocia un conductor específico de un vehículo[cite: 41].

        URL: DELETE /DASS/Vehicle Management/Vehicles/<LicensePlate>/Drivers/<DocumentId> [cite: 41]
        """
        url = f"{self.base_url}/Vehicles/{license_plate}/Drivers/{document_id}"
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 200:
            return True  # Conductor desasociado con éxito [cite: 41]
        elif response.status_code == 404:
            raise Exception(
                "Not Found: El vehículo o la persona no existen."
            )  # [cite: 41]
        else:
            response.raise_for_status()

    def remove_all_drivers(self, license_plate):
        """Desasocia todos los conductores asociados a un vehículo[cite: 42].

        URL: DELETE /DASS/Vehicle Management/Vehicles/<LicensePlate>/Drivers [cite: 42]
        """
        url = f"{self.base_url}/Vehicles/{license_plate}/Drivers"
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 200:
            return True  # Todos los conductores fueron desasociados [cite: 42]
        elif response.status_code == 404:
            raise Exception("Not Found: El vehículo no existe.")  # [cite: 42]
        else:
            response.raise_for_status()