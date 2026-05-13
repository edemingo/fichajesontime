from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) 

class Scheduler:
    

    def __init__(self, ingest):
        self.ingest = ingest
        self.scheduler = BackgroundScheduler()

    def start(self, schedulerTime):
        self.scheduler.add_job(self.tarea_programada, 'interval', minutes=schedulerTime)
        self.scheduler.start()
        print("Scheduler iniciado")
        logger.info("Scheduler iniciado")

    def stop(self):
        self.scheduler.shutdown()
        print("Scheduler detenido")
        logger.info("Scheduler detenido")

    def tarea_programada(self):
        logger.info(">>> Tarea programada INICIADA")
        print("Ejecutando tarea...")
        self.ingest.updateLastFile()
        logger.info(">>> Tarea programada COMPLETADA")