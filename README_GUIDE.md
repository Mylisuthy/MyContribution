# Guía de Gestión Multi-Dispositivo y Escalabilidad

Este documento explica cómo configurar el sistema para gestionar múltiples computadores y cómo organizarlos por "Salas/Aulas" de manera efectiva.

### Método A: Instalación Rápida (Recomendado)

Si tienes `curl` instalado, puedes usar este "one-liner" para descargar, configurar y desplegar el agente en un solo paso:
```bash
curl -sSL https://raw.githubusercontent.com/Mylisuthy/MyContribution/main/agent/install.sh | bash
```
*Este comando es interactivo y te pedirá el "Código de Servidor" (IP) durante la instalación.*

### Método B: Instalación Manual
1.  **Copiar la carpeta `agent/`** al dispositivo Linux (Ubuntu recomendado).
2.  **Configurar la conexión**: Edita `agent/config.py` y cambia `SERVER_URL` por la dirección IP real de tu servidor Orquestador (ej. `http://192.168.1.10:8000/report`).
3.  **Ejecutar el instalador**:
    ```bash
    sudo chmod +x setup.sh
    sudo ./setup.sh
    ```
4.  El agente se registrará automáticamente en el sistema con un ID único guardado en `data/agent_id.lic`.

## 2. Vinculación con Salas (Aulas)

Actualmente, el frontend utiliza una lista estática en `sb-frontend/src/config/inventory.ts`. Para una vinculación real:

### Estrategia Recomendada (Vinculación por ID)
Al registrarse el agente, este envía su `ENDPOINT_ID`. En una implementación de producción, el administrador asocia este ID a una sala en la base de datos del Orquestador.

### Configuración Rápida para el Frontend:
Si quieres que un nuevo dispositivo aparezca en una sala específica del dashboard hoy:
1.  Busca el `ENDPOINT_ID` del nuevo agente (puedes verlo en los logs o en la página de "Dispositivos").
2.  Añade el ID a la lista de dispositivos de la sala correspondiente en `sb-frontend/src/config/rooms.ts`:
    ```typescript
    { id: "SALA_01", name: "Laboratorio A", devices: ["ID_DEL_AGENTE_01", "ID_DEL_AGENTE_02"] }
    ```

## 3. Ejecución de Pruebas de Funcionamiento

He implementado pruebas unitarias para asegurar que los comandos remotos funcionen sin riesgos:

### Pruebas del Agente (Python)
Requiere `pytest` y `httpx`:
```bash
cd agent
pip install pytest httpx
pytest tests/
```
*Estas pruebas verifican que los comandos (Shutdown, Update, Scan) ejecuten las llamadas de sistema correctas usando mocks (simulaciones).*

### Pruebas del Orquestador (C#)
Requiere el SDK de .NET:
```bash
cd sb-core-orchestrator
dotnet test
```
*Estas pruebas verifican que el cliente de comunicación genere el JSON correcto para los agentes.*

---

## 4. Verificación de la Funcionalidad de Aulas
1.  Asegúrate de que el Orchestrator esté corriendo.
2.  Inicia varios agentes (pueden ser en la misma máquina cambiando el ID en `agent_id.lic` para pruebas).
3.  Ve a la página **"Salas de Laboratorio"** del Frontend.
4.  Deberías ver el contador de "Equipos Online" incrementarse en tiempo real sumando todos los agentes activos.
