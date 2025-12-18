# Guía de Uso y Configuración del Frontend (Dashboard)

Esta guía detalla cómo poner en marcha y utilizar el panel de control de "System Break" para la gestión de dispositivos y salas.

## 1. Configuración de Desarrollo

Si deseas ejecutar el frontend fuera de Docker o realizar modificaciones:

### Requisitos
- **Node.js**: v18 o superior.
- **npm**: v9 o superior.

### Instalación
1. Navega a la carpeta del frontend:
   ```bash
   cd sb-frontend
   ```
2. Instala las dependencias:
   ```bash
   npm install
   ```

### Configuración de la API
Edita el archivo `.env.local` (o créalo si no existe) para apuntar al API Gateway:
```env
NEXT_PUBLIC_API_URL=http://192.168.1.15:8080
```
*Reemplaza `192.168.1.15` por la IP de tu servidor principal.*

### Ejecución
Para iniciar el servidor de desarrollo:
```bash
npm run dev
```
La aplicación estará disponible en `http://localhost:3000`.

---

## 2. Navegación por el Dashboard

El frontend se divide en tres secciones principales accesibles desde el menú:

### A. Gestión de Dispositivos (Devices)
Es el centro de control principal.
- **Lista de Equipos**: Muestra todos los agentes registrados con su estado (Online/Offline) y telemetría real (CPU y RAM).
- **Acciones Masivas**:
  - **Seleccionar**: Puedes marcar varios equipos a la vez.
  - **Escanear**: Ejecuta un escaneo de seguridad remoto.
  - **Apagar**: Envía la señal de apagado inmediato.
  - **Actualizar**: Ejecuta `apt upgrade` en los equipos seleccionados.

### B. Salas de Laboratorio (Rooms)
Visualización macro del estado de la red.
- **Contadores Reales**: Verás cuántos equipos hay en total y cuántos están online en ese instante.
- **Organización**: Haz clic en una sala para ver los dispositivos asociados a ella.

### C. Chat IA
Interfaz de lenguaje natural para consultas rápidas.
- **Ejemplos de Preguntas**:
  - "¿Cuántos equipos están en línea?"
  - "¿Cuál es el estado del equipo AGENTE_01?"
  - "¿Hay algún equipo con problemas?"

---

## 3. Acceso desde otros Dispositivos

Una de las mayores ventajas es que el dashboard es responsivo y accesible desde móviles o tablets.

1. Asegúrate de que el servidor tenga el puerto `3000` abierto en su firewall.
2. Desde cualquier dispositivo en la **misma red Wi-Fi/Local**, abre el navegador.
3. Ingresa la IP del servidor: `http://192.168.1.15:3000`.
4. Inicia sesión y gestiona tus laboratorios desde cualquier lugar.

---

## 4. Notas de Personalización Estética
- El fondo utiliza **Spline** para una estética premium y dinámica.
- Los componentes de **Card** cambian de color según el estado del dispositivo (Brillo fucsia para online, gris para offline).
