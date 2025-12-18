#!/bin/bash

# --- System Break Agent - One-Liner Installer ---
# Uso: curl -sSL https://raw.githubusercontent.com/Mylisuthy/MyContribution/main/install.sh | bash

echo "==============================================="
echo "   RECLUTAMIENTO DE AGENTE - SYSTEM BREAK    "
echo "==============================================="

# 1. Pedir Configuración
exec 3< /dev/tty
printf "[-] Ingrese el Nombre del Equipo (Ej: PC-LAB-01): "
read -u 3 AGENT_NAME
printf "[-] Ingrese el Código de Servidor (IP): "
read -u 3 SERVER_IP
exec 3<&-

if [[ -z "$SERVER_IP" || -z "$AGENT_NAME" ]]; then
    echo "[!] Error: El nombre y el código/IP no pueden estar vacíos."
    exit 1
fi

# 2. Clonar el repositorio
echo "[*] Descargando componentes del agente..."
TEMP_DIR=$(mktemp -d)
git clone https://github.com/Mylisuthy/MyContribution.git "$TEMP_DIR"

if [ $? -ne 0 ]; then
    echo "[!] Error al clonar el repositorio. Verifique su conexión."
    exit 1
fi

cd "$TEMP_DIR"
mkdir -p data
echo "$AGENT_NAME" > data/agent_name.lic

# 3. Configurar el Agente
echo "[*] Configurando vinculación con el servidor $SERVER_IP..."
# Reemplazar la IP en config.py
sed -i "s|SERVER_URL = .*|SERVER_URL = \"http://${SERVER_IP}:8080/core/endpoints/register\"|g" config.py

# 4. Ejecutar el instalador real
echo "[*] Iniciando instalación del sistema..."
sudo chmod +x setup.sh
sudo ./setup.sh

# 5. Limpieza (Opcional, pero mejor dejarlo instalado en una ruta fija si es daemon)
# El setup.sh actual crea el servicio usando el PWD actual. 
# Para un instalador real, deberíamos moverlo a /opt/sb-agent antes de setup.sh.

echo ""
echo "==============================================="
echo "   INSTALACIÓN FINALIZADA CORRECTAMENTE      "
echo "==============================================="
