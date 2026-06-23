from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
import logging
from datetime import datetime


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) 

class Scheduler:

    def __init__(self, ingest, dorlet_alive=None):
        self.ingest = ingest
        self.dorlet_alive = dorlet_alive
        self.scheduler = BackgroundScheduler()

    def start(self, schedulerTime):
        self.scheduler.add_job(self.tarea_programada, 'interval', minutes=schedulerTime, misfire_grace_time=10)
        self.scheduler.start()
        self.scheduler.print_jobs()
        logger.info("Scheduler iniciado")

    def stop(self):
        self.scheduler.shutdown()
        print("Scheduler detenido")
        logger.info("Scheduler detenido")

    def tarea_programada(self):
        logger.info(">>> Tarea programada INICIADA")
        print("Ejecutando tarea...")

        if self.dorlet_alive is not None:
            alive_result = self.dorlet_alive()
            logger.info(f"Estado del servidor Dorlet: {alive_result}")

        self.ingest.updateLastFile()
        logger.info(">>> Tarea programada COMPLETADA")


    def getJobs(self):
        print(self.scheduler.print_jobs())


    def tiempo_restante(self,job_id):
        # Buscamos la tarea en el scheduler por su ID
        tarea = self.get_job(job_id)
        
        if tarea and tarea.next_run_time:
            # Importante: next_run_time tiene zona horaria (timezone-aware)
            # Obtenemos la hora actual con la misma zona horaria de la tarea
            ahora = datetime.now(tarea.next_run_time.tzinfo)
            
            # Restamos las fechas para obtener el tiempo que queda
            tiempo_que_queda = tarea.next_run_time - ahora
            
            return tiempo_que_queda
        else:
            return None

    