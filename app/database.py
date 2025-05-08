from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Obtenemos la ruta de la base de datos desde una variable de entorno o usamos una ruta por defecto
# Esto nos permite cambiar fácilmente la ubicación de la base de datos desde docker-compose.yaml
DB_PATH = os.environ.get("DB_PATH", "/app/data/notes.db")

# Creamos el directorio para la base de datos si no existe
# Esto evita errores al intentar crear la base de datos en un directorio que no existe
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Creamos la conexión a la base de datos SQLite
# El parámetro check_same_thread=False permite que SQLite funcione con FastAPI
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Configuramos la sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para definir los modelos de SQLAlchemy
Base = declarative_base()


# Definimos el modelo de datos para las notas
class Note(Base):
    """Modelo para almacenar notas en la base de datos
    
    Campos:
    - id: Identificador único para cada nota (se genera automáticamente)
    - title: Título de la nota
    - content: Contenido o cuerpo de la nota
    """
    __tablename__ = "notes"  # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # Creamos un índice para búsquedas rápidas por título
    content = Column(Text)  # Tipo Text para contenido largo


# Creamos todas las tablas en la base de datos
# se ejecuta al iniciar la aplicación y crea las tablas si no existen
Base.metadata.create_all(bind=engine)


# Función para obtener una conexión a la base de datos
# FastAPI usa esto como dependencia en los endpoints
def get_db():
    """Proporciona una sesión de base de datos para cada solicitud
    
    Esta función se usa como dependencia en FastAPI para que cada
    solicitud tenga su propia conexión a la base de datos y se
    cierre correctamente al finalizar.
    """
    db = SessionLocal()
    try:
        yield db  # Proporciona la sesión al endpoint
    finally:
        db.close()  # Asegura que la conexión se cierre incluso si hay errores
