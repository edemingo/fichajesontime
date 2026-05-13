#!/usr/bin/env python3
"""
Script de prueba para verificar la carga de variables de entorno desde config.env
"""

import os
from dotenv import load_dotenv

def test_config_loading():
    """Prueba la carga de variables desde config.env"""

    print("🔍 Probando carga de variables desde config.env...")

    # Cargar variables desde config.env
    load_dotenv('config.env')

    # Obtener variables
    api_key = os.getenv('apikey')
    api_url = os.getenv('apiURL')

    print(f"✅ API Key cargada: {'Sí' if api_key else 'No'}")
    print(f"✅ API URL cargada: {'Sí' if api_url else 'No'}")

    if api_key:
        print(f"📝 API Key (primeros 20 caracteres): {api_key[:20]}...")
    else:
        print("❌ API Key no encontrada")

    if api_url:
        print(f"🌐 API URL: {api_url}")
    else:
        print("❌ API URL no encontrada")

    # Verificar que las variables sean válidas
    if api_key and api_url:
        print("✅ Configuración completa y válida")
        return True
    else:
        print("❌ Configuración incompleta")
        return False

if __name__ == "__main__":
    test_config_loading()