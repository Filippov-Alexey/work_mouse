import subprocess
import sys

# Путь к вашему Python-скрипту
script_path = "start.py"

try:
    if sys.platform.startswith("win"):
        subprocess.Popen(["python", script_path], creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        subprocess.Popen(["python3", script_path], start_new_session=True)
except Exception as e:
    print(f"Ошибка при запуске скрипта: {e}")
