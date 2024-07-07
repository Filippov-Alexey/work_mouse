import subprocess
import os
from read_file import *
if not os.path.exists("settings.txt"):
    subprocess.Popen(['python','infoprocess.py'])
else:
    subprocess.run(['python','work mouse.py'])

    lines=read_every_second_line("settings.txt")
    if os.path.exists('settings camere keyboard.txt'):
        line1=read_every_second_line('settings camere keyboard.txt')
        if lines[2]!=line1[0]:
            subprocess.run(['python','camere keyboard.py'])
