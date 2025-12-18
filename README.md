# System Break Agent - Reclutamiento de Dispositivos

Bienvenido al repositorio del Agente de **System Break**. Este componente permite el monitoreo y control remoto (Apagado, Escaneo, Actualización) de computadores Linux (Ubuntu) desde un servidor central.

## 🚀 Instalación Rápida (One-Liner)

Para registrar un nuevo equipo en tu laboratorio, simplemente abre una terminal y ejecuta el siguiente comando:

```bash
curl -sSL https://raw.githubusercontent.com/Mylisuthy/MyContribution/main/install.sh | bash
```

> [!IMPORTANT]
> El instalador te pedirá el **Código de Servidor** (la dirección IP de tu servidor principal) para vincular el equipo automáticamente.

---

## 📂 Documentación Detallada

Para configuraciones más avanzadas o resolución de problemas, consulta las siguientes guías:

1.  **[Guía de Despliegue y Red Local](README_GUIDE.md)**: Cómo configurar el servidor y los agentes en una red Wi-Fi/Local.
2.  **[Guía de Uso del Frontend](FRONTEND_GUIDE.md)**: Cómo utilizar el dashboard, gestionar salas y ejecutar comandos remotos.

## 🛠️ Requisitos del Sistema
- **Sistema Operativo**: Ubuntu 22.04 LTS o superior (recomendado).
- **Dependencias**: El instalador configurará automáticamente `python3`, `pip`, y el entorno virtual necesario.

---
*Desarrollado para la gestión eficiente de laboratorios de informática y sistemas de seguridad.*
