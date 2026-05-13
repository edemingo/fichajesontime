from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Datos de tu PostgreSQL
DATABASE_URL = "postgresql://appuser:apppass@localhost:5432/appdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class FicherosExportados(Base):
    __tablename__ = "ficheros_exportados"

    id = Column(Integer, primary_key=True, index=True)
    nombre_fichero = Column(String, nullable=True)
    fecha_exportacion = Column(DateTime, nullable=False)

class IndiceTextoDetalle(Base):
    __tablename__ = "indice_texto_detalle"

    id = Column(Integer, primary_key=True, index=True)
    nombre_archivo = Column(String, nullable=True)
    num_linea = Column(Integer, nullable=True)
    datetime = Column(String, nullable=True)
    dni = Column(String, nullable=True)
    num_empleado = Column(String, nullable=True)
    maquina = Column(String, nullable=True)
    codigo = Column(String, nullable=True)
    codificado = Column(String, nullable=True) 
    exportado = Column(Integer, default=0, nullable=False)
