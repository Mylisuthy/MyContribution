import os
import subprocess
import shlex

# ----------- POWER MANAGEMENT -------------
# Contenido de sysadmin/executor.py
import os
# ... (otras funciones)

# ----------- POWER MANAGEMENT -------------
# ----------- POWER MANAGEMENT -------------
def shutdown(args=None):
    print("[EXECUTOR] Shutting down system using 'sudo systemctl poweroff'...")
    # Usamos sudo para asegurar permisos si el agente no corre como root directamente.
    # En un daemon bien configurado, esto debería funcionar.
    try:
        subprocess.Popen(["sudo", "systemctl", "poweroff"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"[ERROR] Shutdown failed: {e}")
        # Fallback
        os.system("sudo shutdown -h now &")
    
    return True 

# ----------- SYSTEM UPDATES ----------------
def update_system(args=None):
    try:
        print("[EXECUTOR] Starting system update...")
        # Usamos sudo explícitamente para mayor claridad en el foco admin.
        cmd = "sudo apt-get update -y && sudo apt-get upgrade -y"
        subprocess.run(cmd, shell=True, check=True)
        print("[EXECUTOR] Update completed")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Update failed: {e}")

# ----------- MULTIMEDIA --------------------
def show_video(args):
    path = args.get("path")
    if not path or not os.path.exists(path):
        print(f"[ERROR] Video path not found: {path}")
        return

    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    
    # Intento básico de obtener XAUTHORITY (Mejorable)
    if "XAUTHORITY" not in env:
        uid = os.getuid()
        env["XAUTHORITY"] = f"/run/user/{uid}/gdm/Xauthority"

    try:
        # shlex.split no es necesario si pasamos lista, pero path debe ser un solo argumento
        print(f"[EXECUTOR] Opening video: {path}")
        subprocess.Popen(["xdg-open", path], env=env)
    except Exception as e:
        print(f"[ERROR] Could not open video: {e}")

def change_wallpaper(args):
    path = args.get("path")
    if not path: return
    
    # Ejemplo para GNOME. Para otros entornos (KDE, XFCE) el comando cambia.
    cmd = [
        "gsettings", "set", "org.gnome.desktop.background", 
        "picture-uri", f"file://{path}"
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"[EXECUTOR] Wallpaper changed to {path}")
    except Exception as e:
        print(f"[ERROR] Failed to set wallpaper: {e}")