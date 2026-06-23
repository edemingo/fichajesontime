from datetime import datetime
import requests


class DorletAPI:
    def __init__(self):

        """
        TORNOS MARCONI1 
        "DeviceId": 6903, "DeviceName": "M1 Torno 1 Salida Derecha"
        "DeviceId": 6803, "DeviceName": "M1 Torno 1 Entrada Derecha"
        "DeviceId": 7103, "DeviceName": "M1 Torno 2 Salida Izquierda"
        "DeviceId": 6903, "DeviceName": "M1 Torno 1 Salida Derecha"
        """

        self.dorlet_server_ip = '10.51.10.19'
        self.dorlet_server_proto = 'http'
        self.dorlet_server_port = 8081
        self.auth_user = 'factorial'
        self.auth_pass = 'Ontime.2026*'
        
        self.list_of_devices = [11]

        self.base_url = f"{self.dorlet_server_proto}://{self.dorlet_server_ip}:{self.dorlet_server_port}"
        self.api_key = None 

        self.alivePayload = {
                                "Id": "1254",
                                "PersonToVisitDocumentId": "00000000-T",
                                "AppointmentStatus": "Authorized",
                                "AppointmentExternalStatus": "Pending",
                                "StartDateFromFrom": "01010001/01/01/2020",
                                "StartDateTo": "02/01/2020"    
                            }
        
        self.aliveHeaders = {
                                "Content-Type": "application/json",
                                "Accept": "application/json"
                            }   



    def alive(self):
        url = f"{self.base_url}/DASS/Visits/Appointments/Search"

        try:    
            response = requests.post(url, json=self.alivePayload, headers=self.aliveHeaders, auth=(self.auth_user, self.auth_pass))
            response.raise_for_status()
             # print(f"Estado del servidor Dorlet: {response.status_code} - {response.reason}")            
            theMessage = f"{response.status_code}|{response.reason}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.write_log(theMessage)
            return response.status_code
        except requests.exceptions.RequestException as e:
            print(f"Error al verificar el estado del servidor Dorlet: {e}")
            return None
        

    def write_log(self, message):
        # Aquí puedes implementar la lógica para escribir en un archivo de log
        # Por ejemplo, usando el módulo logging o simplemente escribiendo en un archivo de texto
        with open("dorlet_api.log", "a") as log_file:
            log_file.write(f"{message}\n")