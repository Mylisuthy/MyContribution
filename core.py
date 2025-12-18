# agent/core.py

import time
import threading
import logging
import sys

# --- Importaciones de módulos del agente ---
from agent.config import HEARTBEAT_INTERVAL, SERVER_URL # Mantengo por si vuelven al push
from agent.comm.outbound import send_heartbeat, send_full_inventory # Ya no se usan
from agent.security.ids import start_ids_daemon 
from agent.api import run_api_server # ¡NUEVO! Importamos la función que inicia la API

logger = logging.getLogger("agent.core") 

# ====================================================================
# BUCLES DE EJECUCIÓN
# ====================================================================

def heartbeat_loop():
    """Bucle infinito para enviar el latido al orquestador."""
    logger.info(f"Heartbeat loop started (Interval: {HEARTBEAT_INTERVAL}s)")
    while True:
        try:
            send_heartbeat()
        except Exception as e:
            logger.error(f"Error in heartbeat loop: {e}")
        time.sleep(HEARTBEAT_INTERVAL)

# ====================================================================
# ARRANQUE
# ====================================================================

def start():
    """Inicia todos los módulos del agente."""
    
    logger.info("--- SB-AGENT STARTING (API MODE) ---")

    # 1. Iniciar IDS (Sniffer) en un hilo secundario
    try:
        threading.Thread(target=start_ids_daemon, daemon=True).start()
        logger.info("IDS Module initialized")
    except Exception as e:
        logger.error(f"Failed to start IDS module: {e}")

    # 2. Iniciar Heartbeat
    try:
        threading.Thread(target=heartbeat_loop, daemon=True).start()
        logger.info("Heartbeat loop initialized")
    except Exception as e:
        logger.error(f"Failed to start Heartbeat loop: {e}")

    # 3. Iniciar el Servidor API (Bloquea el hilo principal)
    # Esto es lo que mantiene vivo al contenedor y responde a las peticiones del Orquestador
    try:
        run_api_server()
    except Exception as e:
        logger.critical(f"Critical error starting API Server. Shutting down: {e}")
        sys.exit(1)