from pathlib import Path
import json
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values, Json


class Ingest:
    

    def __init__(self):
        self.directorio = directorio = Path("/home/edmingo/Movimientos") 
        self.conn = None
        self.cur = None


    
    """
    Ingesta y actualización del último fichero
    """
    def updateLastFile(self):
        
        self.dbconnection()

        archivos = [f for f in self.directorio.iterdir() if f.is_file()]
        total_insertados = 0

        if archivos:
            archivo_mas_reciente = max(archivos, key=lambda f: f.stat().st_mtime)

        print('-------------------------------------------------')
        print('--- Ultimo archivo encontrado para actualizar -------')
        print(archivo_mas_reciente)
        print('-------------------------------------------------')

        self.cur.execute(
            "DELETE FROM indice_texto_detalle WHERE nombre_archivo = %s",
            (archivo_mas_reciente.name,)
        )

        with open(archivo_mas_reciente, "r", encoding="utf-8") as f:
            for num_linea, linea in enumerate(f, start=1):
                linea = linea.strip()
                if linea:
                    campos = linea.split("|")


                    total_insertados = total_insertados + 1 
                    
                    if len(campos) >= 6:
                        datetime_str, dni, num_empleado, maquina, codigo, codificado = campos[:6]
                       
                        
                        self.cur.execute("""
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

        self.conn.commit()        
        self.dbConnnectionClose()
        

    """
    Ingesta y actualización de un fichero
    """


    def updateFromFileByParams(self, theDay, theMonth, theYear):
        self.dbconnection()
        archivos = []
        theDay = int(theDay)
        theMonth = int(theMonth)
        theYear = int(theYear)

        
        
        #archivos = [f for f in self.directorio.iterdir() if f.is_file(): echa_mod = datetime.fromtimestamp(archivo.stat().st_mtime)]

        for archivo in self.directorio.iterdir():
            if archivo.is_file():
                
                # Obtenemos la fecha de última modificación
                fecha_mod = datetime.fromtimestamp(archivo.stat().st_mtime)
                """
                print(archivo)
                print(fecha_mod)
                print(fecha_mod.day)
                print(fecha_mod.month)
                print(fecha_mod.year)
                """
                # Comparamos si coincide con los parámetros
                if fecha_mod.day == theDay and fecha_mod.month == theMonth and fecha_mod.year == theYear:
                    archivos.append(archivo)
                    

        
        total_insertados = 0

        if archivos:
            archivo_mas_reciente = max(archivos, key=lambda f: f.stat().st_mtime)


        print(archivos)

        
        self.cur.execute(
            "DELETE FROM indice_texto_detalle WHERE nombre_archivo = %s", (archivo_mas_reciente.name,)
        )

        with open(archivo_mas_reciente, "r", encoding="utf-8") as f:
            for num_linea, linea in enumerate(f, start=1):
                linea = linea.strip()
                if linea:
                    campos = linea.split("|")
                    
                    if len(campos) >= 6:
                        datetime_str, dni, num_empleado, maquina, codigo, codificado = campos[:6]
                        
                        self.cur.execute("""
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
                        
                        total_insertados = total_insertados +1
                        
        self.conn.commit()        
        self.dbConnnectionClose()
                 



    def updateFromFile(self, nombre_fichero):
        
        self.dbconnection()
        
        archivos = [f for f in self.directorio.iterdir() if f.is_file() and f.name == nombre_fichero]
        total_insertados = 0
        

        if archivos:
            archivo_mas_reciente = max(archivos, key=lambda f: f.stat().st_mtime)
            
        self.cur.execute(
            "DELETE FROM indice_texto_detalle WHERE nombre_archivo = %s", (archivo_mas_reciente.name,)
        )

        with open(archivo_mas_reciente, "r", encoding="utf-8") as f:
            for num_linea, linea in enumerate(f, start=1):
                linea = linea.strip()
                if linea:
                    campos = linea.split("|")
                    
                    if len(campos) >= 6:
                        datetime_str, dni, num_empleado, maquina, codigo, codificado = campos[:6]
                        
                        self.cur.execute("""
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
                        
                        total_insertados = total_insertados +1
                        
        self.conn.commit()        
        self.dbConnnectionClose()

 

    """
    Listado de Ficheros
    """
    def getFicherosDorlet(self):
        archivos = sorted(
            self.directorio.iterdir(),
            key=lambda f: f.stat().st_mtime,
            reverse=True   # más reciente primero
        )
        
        return [f.name for f in archivos if f.is_file()]


    """
    Ingesta y actualización de un fichero
    """

    def updateFromSingleFileRun(self, theFileName):
        
        self.dbconnection()

        #archivos = [f for f in self.directorio.iterdir() if f.is_file()]
        archivos = [f for f in self.directorio.iterdir() if f.is_file() and f.name == theFileName]
        total_insertados = 0

        if archivos:

            archivo_mas_reciente = max(archivos, key=lambda f: f.stat().st_mtime)

        self.cur.execute(
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
                        
                        self.cur.execute("""
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

        self.conn.commit()        
        self.dbConnnectionClose()


    def getFicheroContent(self, nombre_fichero):
        archivos = [f for f in self.directorio.iterdir() if f.is_file() and f.name == nombre_fichero]

        if archivos:
            archivo_mas_reciente = max(archivos, key=lambda f: f.stat().st_mtime)

        contenido_fichero = ""

        with open(archivo_mas_reciente, "r", encoding="utf-8") as f:            
            for num_linea, linea in enumerate(f, start=1):
                    linea = linea.strip()
                    if linea:
                        contenido_fichero = contenido_fichero + linea + "&&"

        return contenido_fichero
        

    def parse_date(value):
        if not value:
            return None
        return datetime.strptime(value, "%Y-%m-%d").date()

    def parse_datetime(value):
        if not value:
            return None
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    def delete_before_insert(self):
        self.dbconnection()
        self.cur.execute("DELETE FROM empleados")
        self.conn.commit()
        self.dbConnnectionClose()    



    def delete_sifts_before_insert(self, fecha):
        self.dbconnection()
        self.cur.execute("DELETE FROM allshifts where to_timestamp(datetime, 'YYYY/MM/DD HH24:MI:SS')::date = CAST(:fecha AS date)")

        
        self.conn.commit()
        self.dbConnnectionClose()    
        

    def insertShiftEmpleadoDia(self, obj, fecha):

        self.delete_sifts_before_insert(fecha=fecha)
        
        """"""
        self.dbconnection()

        # Definición de la consulta
        query = """
        INSERT INTO allShifts (
            id, employee_id, date, reference_date, clock_in, clock_out,
            in_source, out_source, observations, location_type, half_day,
            in_location_latitude, in_location_longitude, in_location_accuracy,
            out_location_latitude, out_location_longitude, out_location_accuracy,
            workable, created_at, workplace_id, time_settings_break_configuration_id,
            company_id, updated_at, minutes, clock_in_with_seconds
        ) VALUES (
            %(id)s, %(employee_id)s, %(date)s, %(reference_date)s, %(clock_in)s, %(clock_out)s,
            %(in_source)s, %(out_source)s, %(observations)s, %(location_type)s, %(half_day)s,
            %(in_location_latitude)s, %(in_location_longitude)s, %(in_location_accuracy)s,
            %(out_location_latitude)s, %(out_location_longitude)s, %(out_location_accuracy)s,
            %(workable)s, %(created_at)s, %(workplace_id)s, %(time_settings_break_configuration_id)s,
            %(company_id)s, %(updated_at)s, %(minutes)s, %(clock_in_with_seconds)s
        ) ;
        """

        myObj = obj

        # La API de Factorial retorna {"data": [...], "metadata": {...}}
        # Extraer la lista de empleados
        if isinstance(myObj, dict) and 'data' in myObj:
            data_to_insert = myObj['data']
        elif isinstance(myObj, list):
            data_to_insert = myObj
        else:
            data_to_insert = [myObj]
        
        for item in data_to_insert:
            mapped_item = {
                'id': item.get('id'),
                'employee_id': item.get('employee_id'),
                'date': item.get('date'),
                'reference_date': item.get('reference_date'),
                'clock_in': item.get('clock_in'),
                'clock_out': item.get('clock_out'),
                'in_source': item.get('in_source'),
                'out_source': item.get('out_source'),
                'observations': item.get('observations'),
                'location_type': item.get('location_type'),
                'half_day': item.get('half_day'),
                'in_location_latitude': item.get('in_location_latitude'),
                'in_location_longitude': item.get('in_location_longitude'),
                'in_location_accuracy': item.get('in_location_accuracy'),
                'out_location_latitude': item.get('out_location_latitude'),
                'out_location_longitude': item.get('out_location_longitude'),
                'out_location_accuracy': item.get('out_location_accuracy'),
                'workable': item.get('workable'),
                'created_at': item.get('created_at'),
                'workplace_id': item.get('workplace_id'),
                'time_settings_break_configuration_id': item.get('time_settings_break_configuration_id'),
                'company_id': item.get('company_id'),
                'updated_at': item.get('updated_at'),
                'minutes': item.get('minutes'),
                'clock_in_with_seconds': item.get('clock_in_with_seconds'),            
            }
            self.cur.execute(query, mapped_item) 
            self.conn.commit()



    def insertar_empleado(self, obj):

        self.delete_before_insert()

        self.dbconnection()


        thisSql = """
        INSERT INTO empleados (
            id, access_id, first_name, last_name, full_name, preferred_name,
            birth_name, gender, identifier, identifier_type, email, login_email,
            birthday_on, nationality, address_line_1, address_line_2, postal_code,
            city, state, country, bank_number, swift_bic, bank_number_format,
            company_id, legal_entity_id, location_id, created_at, updated_at,
            social_security_number, is_terminating, terminated_on,
            termination_reason_type, termination_reason, termination_observations,
            manager_id, timeoff_manager_id, phone_number, company_identifier,
            age_number, termination_type_description, contact_name, contact_number,
            personal_email, seniority_calculation_date, pronouns, active,
            disability_percentage_cents, identifier_expiration_date, attendable,
            country_of_birth, birthplace, raw_json
        ) VALUES (
            %(id)s, %(access_id)s, %(first_name)s, %(last_name)s, %(full_name)s, %(preferred_name)s,
            %(birth_name)s, %(gender)s, %(identifier)s, %(identifier_type)s, %(email)s, %(login_email)s,
            %(birthday_on)s, %(nationality)s, %(address_line_1)s, %(address_line_2)s, %(postal_code)s,
            %(city)s, %(state)s, %(country)s, %(bank_number)s, %(swift_bic)s, %(bank_number_format)s,
            %(company_id)s, %(legal_entity_id)s, %(location_id)s, %(created_at)s, %(updated_at)s,
            %(social_security_number)s, %(is_terminating)s, %(terminated_on)s,
            %(termination_reason_type)s, %(termination_reason)s, %(termination_observations)s,
            %(manager_id)s, %(timeoff_manager_id)s, %(phone_number)s, %(company_identifier)s,
            %(age_number)s, %(termination_type_description)s, %(contact_name)s, %(contact_number)s,
            %(personal_email)s, %(seniority_calculation_date)s, %(pronouns)s, %(active)s,
            %(disability_percentage_cents)s, %(identifier_expiration_date)s, %(attendable)s,
            %(country_of_birth)s, %(birthplace)s, %(raw_json)s
        )
        ON CONFLICT (id) DO UPDATE SET
            updated_at = EXCLUDED.updated_at,
            raw_json = EXCLUDED.raw_json
        """

                
        myObj = obj
        
        # La API de Factorial retorna {"data": [...], "metadata": {...}}
        # Extraer la lista de empleados
        if isinstance(myObj, dict) and 'data' in myObj:
            data_to_insert = myObj['data']
        elif isinstance(myObj, list):
            data_to_insert = myObj
        else:
            data_to_insert = [myObj]
        
        for item in data_to_insert:
            # Mapear campos de la API a campos de la BD
            # La API puede tener nombres diferentes, normalizar aquí
            mapped_item = {
                'id': item.get('id'),
                'access_id': item.get('access_id'),
                'first_name': item.get('first_name'),
                'last_name': item.get('last_name'),
                'full_name': item.get('full_name'),
                'preferred_name': item.get('preferred_name'),
                'birth_name': item.get('birth_name'),
                'gender': item.get('gender'),
                'identifier': item.get('identifier'),
                'identifier_type': item.get('identifier_type'),
                'email': item.get('email'),
                'login_email': item.get('login_email'),
                'birthday_on': item.get('birthday_on'),
                'nationality': item.get('nationality'),
                'address_line_1': item.get('address_line_1'),
                'address_line_2': item.get('address_line_2'),
                'postal_code': item.get('postal_code'),
                'city': item.get('city'),
                'state': item.get('state'),
                'country': item.get('country'),
                'bank_number': item.get('bank_number'),
                'swift_bic': item.get('swift_bic'),
                'bank_number_format': item.get('bank_number_format'),
                'company_id': item.get('company_id'),
                'legal_entity_id': item.get('legal_entity_id'),
                'location_id': item.get('location_id'),
                'created_at': item.get('created_at'),
                'updated_at': item.get('updated_at'),
                'social_security_number': item.get('social_security_number'),
                'is_terminating': item.get('is_terminating'),
                'terminated_on': item.get('terminated_on'),
                'termination_reason_type': item.get('termination_reason_type'),
                'termination_reason': item.get('termination_reason'),
                'termination_observations': item.get('termination_observations'),
                'manager_id': item.get('manager_id'),
                'timeoff_manager_id': item.get('timeoff_manager_id'),
                'phone_number': item.get('phone_number'),
                'company_identifier': item.get('company_identifier'),
                'age_number': item.get('age_number'),
                'termination_type_description': item.get('termination_type_description'),
                'contact_name': item.get('contact_name'),
                'contact_number': item.get('contact_number'),
                'personal_email': item.get('personal_email'),
                'seniority_calculation_date': item.get('seniority_calculation_date'),
                'pronouns': item.get('pronouns'),
                'active': item.get('active'),
                'disability_percentage_cents': item.get('disability_percentage_cents'),
                'identifier_expiration_date': item.get('identifier_expiration_date'),
                'attendable': item.get('attendable'),
                'country_of_birth': item.get('country_of_birth'),
                'birthplace': item.get('birthplace'),
                'raw_json': json.dumps(item)  # Guardar JSON completo
            }
            self.cur.execute(thisSql, mapped_item) 
            self.conn.commit()



        def cargar_empleados_desde_json(self, ruta_json):
            path = Path(ruta_json)
            registros = []

            self.dbconnection()

            with path.open("r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue

                    obj = json.loads(linea)

                    registros.append((
                        obj.get("id"),
                        obj.get("access_id"),
                        obj.get("first_name"),
                        obj.get("last_name"),
                        obj.get("full_name"),
                        obj.get("preferred_name"),
                        obj.get("birth_name"),
                        obj.get("gender"),
                        obj.get("identifier"),
                        obj.get("identifier_type"),
                        obj.get("email"),
                        obj.get("login_email"),
                        parse_date(obj.get("birthday_on")),
                        obj.get("nationality"),
                        obj.get("address_line_1"),
                        obj.get("address_line_2"),
                        obj.get("postal_code"),
                        obj.get("city"),
                        obj.get("state"),
                        obj.get("country"),
                        obj.get("bank_number"),
                        obj.get("swift_bic"),
                        obj.get("bank_number_format"),
                        obj.get("company_id"),
                        obj.get("legal_entity_id"),
                        obj.get("location_id"),
                        parse_datetime(obj.get("created_at")),
                        parse_datetime(obj.get("updated_at")),
                        obj.get("social_security_number"),
                        obj.get("is_terminating"),
                        parse_date(obj.get("terminated_on")),
                        obj.get("termination_reason_type"),
                        obj.get("termination_reason"),
                        obj.get("termination_observations"),
                        obj.get("manager_id"),
                        obj.get("timeoff_manager_id"),
                        obj.get("phone_number"),
                        obj.get("company_identifier"),
                        obj.get("age_number"),
                        obj.get("termination_type_description"),
                        obj.get("contact_name"),
                        obj.get("contact_number"),
                        obj.get("personal_email"),
                        parse_date(obj.get("seniority_calculation_date")),
                        obj.get("pronouns"),
                        obj.get("active"),
                        obj.get("disability_percentage_cents"),
                        parse_date(obj.get("identifier_expiration_date")),
                        obj.get("attendable"),
                        obj.get("country_of_birth"),
                        obj.get("birthplace"),
                        Json(obj)
                    ))

            sql = """
            INSERT INTO empleados (
                id, access_id, first_name, last_name, full_name, preferred_name, birth_name,
                gender, identifier, identifier_type, email, login_email, birthday_on,
                nationality, address_line_1, address_line_2, postal_code, city, state, country,
                bank_number, swift_bic, bank_number_format, company_id, legal_entity_id,
                location_id, created_at, updated_at, social_security_number, is_terminating,
                terminated_on, termination_reason_type, termination_reason, termination_observations,
                manager_id, timeoff_manager_id, phone_number, company_identifier, age_number,
                termination_type_description, contact_name, contact_number, personal_email,
                seniority_calculation_date, pronouns, active, disability_percentage_cents,
                identifier_expiration_date, attendable, country_of_birth, birthplace, raw_json
            ) VALUES %s
            ON CONFLICT (id) DO UPDATE SET
                updated_at = EXCLUDED.updated_at,
                raw_json = EXCLUDED.raw_json
            """

            with self.conn.cursor() as cur:
                execute_values(self.cur, sql, registros)
            self.conn.commit()


    def dbconnection(self):
        self.conn = psycopg2.connect(dbname="appdb", user="appuser", password="apppass", host="localhost", port="5432")
        self.cur = self.conn.cursor()

        
    def dbConnnectionClose(self):        
        self.cur.close()
        self.conn.close()

