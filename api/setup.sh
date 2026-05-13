python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install fastapi uvicorn

# Lanzar
uvicorn main:app --reload
