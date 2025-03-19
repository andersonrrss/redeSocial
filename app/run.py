import subprocess
import os
import platform
import threading
from . import create_app

app, socketio = create_app()

def get_npx_tsc_commands():
    system = platform.system()
    
    if system == "Windows":
        # Caminhos para Windows (usando .cmd)
        npx_cmd = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', 'npm', 'npx.cmd')
        tsc_cmd = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', 'npm', 'tsc.cmd')
    else:
        # Caminhos para Linux/MacOS
        npx_cmd = "node_modules/.bin/npx"
        tsc_cmd = "node_modules/.bin/tsc"

    return npx_cmd, tsc_cmd

def compile_tailwind(npx_cmd):
    try:
        # Compila o Tailwind CSS
        subprocess.run(["npx", "tailwindcss", "-i", "app/static/css/src/input.css", "-o", "app/static/css/output.css"], check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"\n\n\nErro ao compilar o Tailwind: {e}\n\n\n")

def compile_typescript(tsc_cmd):
    try:
        # Compila o TypeScript
        subprocess.run([tsc_cmd], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n\n\n Errp ap compilar o Typescript: {e}\n\n\n")

if __name__ == "__main__":
    # Obtém os comandos de acordo com o sistema operacional
    npx_cmd, tsc_cmd = get_npx_tsc_commands()
    
    # Rodar processos em threads
    tailwind_thread = threading.Thread(target=compile_tailwind, args=(npx_cmd,))
    typescript_thread = threading.Thread(target=compile_typescript, args=(tsc_cmd,))
    
    # Iniciar os threads
    tailwind_thread.start()
    typescript_thread.start()

    # Rodar o servidor Flask com socket.io
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
