import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException, Request
import logging
from datetime import datetime, timezone 
from agent.sysadmin.attack_control import run_syn_scan_remote, run_icmp_flood_remote
from agent.config import AGENT_ID, PORT
from agent.sysadmin.packages import list_installed_packages
from agent.sysadmin.system_info import get_resources, get_mac_address
from agent.sysadmin.executor import shutdown # <-- IMPORTACIÓN DE LA FUNCIÓN DE APAGADO
from agent.sysadmin.executor import update_system
from pydantic import BaseModel

logger = logging.getLogger("agent.api")

# Crea la aplicación FastAPI y el router para organizar los endpoints
app = FastAPI(title="SB Agent API")
router = APIRouter()

# ======================================================================
# ENDPOINT PARA PAQUETES INSTALADOS
# ======================================================================
@router.get("/agent/packages", tags=["Scan"])
async def get_packages_for_analysis():
    
    packages_list = list_installed_packages()
    
    response = {
        "agentId": AGENT_ID, 
        "packages": packages_list 
    }
    
    logger.info(f"Returning {len(packages_list)} packages for analysis.")
    return response

# ======================================================================
# ENDPOINT PARA ESTADO (RAM/CPU/MAC/ETC.)
# ======================================================================
@router.get("/agent/status", tags=["Status"])
async def get_agent_status():
    """
    Endpoint llamado por el sb-core-orchestrator para obtener el estado 
    actual del sistema (CPU, RAM, MAC) y actualizar la interfaz de usuario.
    """
    logger.info("Received request for agent status.")
    
    # Obtener recursos (CPU, RAM, Disco)
    resources = get_resources()
    
    # 🚨 NUEVA FUNCIÓN: Obtener la MAC Address para WOL
    mac_address = get_mac_address()
    
    # Obtener la marca de tiempo actual en formato ISO 8601 (UTC)
    current_time = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    response = {
        "agentId": AGENT_ID,
        "online": True, 
        "cpuLoad": resources.get('cpu_percent', 0.0),
        "ramUsagePercent": resources.get('ram_percent', 0.0),
        "osName": resources.get('os_name', 'Unknown'),
        "lastSeenAt": current_time,
        "overallSeverity": "NONE",
        
        # 🚨 CAMPO CRÍTICO PARA WOL
        "macAddress": mac_address 
    }
    
    logger.info("Returning real-time status data.")
    return response

# ======================================================================
# NUEVO ENDPOINT PARA CONTROL DEL SISTEMA (SHUTDOWN)
# ======================================================================
@router.post("/sysadmin/shutdown", tags=["Control"]) 
def shutdown_agent_host(request: Request):
    """
    Endpoint llamado por el Orchestrator para apagar el sistema operativo host 
    mediante el comando 'shutdown now'. Requiere permisos SYS_ADMIN en Docker.
    """
    host_ip = request.client.host
    logger.critical(f"SHUTDOWN COMMAND RECEIVED from {host_ip}. Executing shutdown...")
    
    try:
        # Llama a la función 'shutdown()' definida en executor.py
        shutdown() 
        return {"status": "success", "message": "Host shutdown initiated."}
    except Exception as e:
        logger.error(f"Failed to execute shutdown command: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate host shutdown.")

# En tu api.py, añade este nuevo endpoint (ejemplo):


@router.post("/sysadmin/update", tags=["Control"])
def update_agent_host(request: Request):
    """Ejecuta apt update y apt upgrade en el host."""
    try:
        update_system()
        return {"status": "success", "message": "System update initiated."}
    except Exception as e:
        logger.error(f"Failed to execute update command: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate system update.")
    
# ======================================================================
# STANDARDIZED ENDPOINT FOR AGENT COMMANDS
# ======================================================================
class AgentCommandRequest(BaseModel):
    action: str
    params: dict = {}

@router.post("/agent/commands", tags=["Control"])
async def handle_agent_command(request: AgentCommandRequest):
    """
    Standardized endpoint for executing commands from the Core Orchestrator.
    Supports: POWER_OFF, SCAN, UPDATE
    """
    action = request.action.upper()
    logger.info(f"Received command: {action} with params: {request.params}")
    
    try:
        if action == "POWER_OFF":
            shutdown()
            return {"success": True, "message": "Shutdown initiated"}
        
        elif action == "SCAN":
            # For now, we reuse the packages listing as a "scan" demo or 
            # we could implement a more formal scan later.
            packages = list_installed_packages()
            return {"success": True, "details": {"packages_count": len(packages), "packages": packages}}
        
        elif action == "UPDATE":
            update_system()
            return {"success": True, "message": "Update initiated"}
        
        else:
            return {"success": False, "errorMessage": f"Unknown action: {action}"}
            
    except Exception as e:
        logger.error(f"Error executing {action}: {e}")
        return {"success": False, "errorMessage": str(e)}

# Incluye todas las rutas definidas en el router en la aplicación principal
app.include_router(router)

# Función principal para ejecutar el servidor
def run_api_server():
    """Inicia el servidor Uvicorn para la API."""
    logger.info(f"Starting API listener on port {PORT}...")
    uvicorn.run(
        app,
        host="0.0.0.0", 
        port=PORT
    )