import subprocess
def run_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Ошибка: {result.stderr.strip()}"
    except subprocess.CalledProcessError as e:
        return f"Ошибка: {e}"
    

def run_command_wait(command,max_attempts=5):
    attempts = 0
    result = ""
    
    while result=="":
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Ошибка: {e.stderr.strip()}")
            attempts += 1
            if attempts >= max_attempts:
                return f"Превышено максимальное количество попыток ({max_attempts})."
    
    return result.stdout

def run_key():
    subprocess.Popen(['python','keyboard1.py'])
