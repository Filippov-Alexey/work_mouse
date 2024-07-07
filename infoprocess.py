import tkinter as tk
import subprocess 
import threading
from read_file import *
i=0
def run_other_scripts():
    global i

    setting = subprocess.Popen(['python', 'setting.py'])
    setting.wait()

    i+=1

    mouse = subprocess.Popen(['python', 'setting mouse.py'])
    mouse.wait()

    i+=1

    line=read_every_second_line('settingsubprocess.txt')
    if line[9]=='1\n':
        cam = subprocess.Popen(['python', 'camere to keyboard settingsubprocess.py'])
        cam.wait()

        i+=1

        key=subprocess.Popen(['python','setting keyboard.py'])
        key.wait()

        i+=1
    else:
        i+=2
    print(i)

    if i==4:
        subprocess.Popen(['python', 'start.py'])
        t.destroy()

def main():
    global t
    t = tk.Tk()
    t.title('proc')
    
    step1 = tk.Label(t, text="Начнём настройку с первичных данных:")
    step1.pack(side='top')

    step2 = tk.Label(t, text='В первом окне выберите камеру по порядковому номеру подключения')
    step2.pack(side='top')

    step3 = tk.Label(t, text='Во втором окна надо выбрать цвета для перемещения, нажатия левой кнопки мыши, и для нажания правой кнопки мыши')
    step3.pack(side='top')

    step4 = tk.Label(t, text='В треьем окне настройте камеру для мыши')
    step4.pack(side='top')

    t.mainloop()

thread1 = threading.Thread(target=main)
thread1.start()
thread = threading.Thread(target=run_other_scripts)
thread.start()
thread.join()
thread1.join()

