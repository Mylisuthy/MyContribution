import os
import uuid

# Configuración de conexión
SERVER_URL = "http://10.0.120.2:8000/report" # IP de tu servidor C#
PORT = 9875                                    # Puerto de escucha del agente
HEARTBEAT_INTERVAL = 10                       # Segundos

# --- Persistencia del ID y Nombre ---
ID_FILE = "data/agent_id.lic"
NAME_FILE = "data/agent_name.lic"

def get_agent_id():
    os.makedirs("data", exist_ok=True)
    if os.path.exists(ID_FILE):
        with open(ID_FILE, "r") as f:
            return f.read().strip()
    else:
        new_id = str(uuid.uuid4())
        with open(ID_FILE, "w") as f:
            f.write(new_id)
        return new_id

def get_agent_name():
    if os.path.exists(NAME_FILE):
        with open(NAME_FILE, "r") as f:
            return f.read().strip()
    return "Unknown Agent"

AGENT_ID = get_agent_id()
AGENT_NAME = get_agent_name()
