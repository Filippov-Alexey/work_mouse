import subprocess
import os

if not os.path.exists("settings.txt"):
    subprocess.run(['python','setting.py'])
else:
    subprocess.Popen(['python','Work mouse.py'])

    with open("settings.txt", 'r+') as f:
        lines = f.readlines()

    every_second_line = []  # Create an empty list to store every second line
    for index in range(1, 10, 2):
        line = lines[index].strip()
        every_second_line.append(line)

    if every_second_line[4]=='1':
        subprocess.run(['python','keyboard.py'])