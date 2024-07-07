import cv2
import numpy as np
import os
import win32com.client
from detect import *
from data import *
with open('settings.txt', 'r') as file:
    lines = file.readlines()

every_second_line = []
for index in range(1, len(lines), 2):
    every_second_line.append(lines[index])

for index in range(1, 10, 2):
    line = lines[index].strip()
    every_second_line.append(line)

if every_second_line[3] == "1":
    current_directory = os.getcwd()

    source_file = os.path.join(current_directory, 'start.exe')

    shortcut_name = 'start'

    startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut_file = os.path.join(startup_folder, f'{shortcut_name}.lnk')
    shortcut = shell.CreateShortcut(shortcut_file)
    shortcut.TargetPath = source_file
    shortcut.WorkingDirectory = os.path.dirname(source_file)
    shortcut.WindowStyle = 7
    shortcut.save()


var1 = every_second_line[0]
var2 = every_second_line[1]
var3 = int(every_second_line[2])
horizontally=int(every_second_line[5])
vertically=int(every_second_line[6])
turn=int(every_second_line[7])
close = int(every_second_line[8])

def mouse_click(event, x, y, flags, param):
    global rigth_center, rigth_radius, left_center, left_radius, move_center, move_radius
    global lower_move,upper_move, lower_left, upper_left, lower_rigth, upper_rigth, i

    if event == cv2.EVENT_LBUTTONDBLCLK:
        i += 1
        if i == 1:
            bgr_color = frame[y, x]
            hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
            lower_move = np.array([int(hsv_color[0, 0, 0]) - 10, 100, 100])
            upper_move = np.array([int(hsv_color[0, 0, 0]) + 10, 255, 255])
        if i == 2:
            bgr_color = frame[y, x]
            hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
            lower_left = np.array([int(hsv_color[0, 0, 0]) - 10, 100, 100])
            upper_left = np.array([int(hsv_color[0, 0, 0]) + 10, 255, 255])
        if i == 3:
            bgr_color = frame[y, x]
            hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
            lower_rigth = np.array([int(hsv_color[0, 0, 0]) - 10, 100, 100])
            upper_rigth = np.array([int(hsv_color[0, 0, 0]) + 10, 255, 255])
    if event==cv2.EVENT_RBUTTONDOWN and i>0:
        i-=1

cap = cv2.VideoCapture(var3)

if not cap.isOpened():
    print("Не удалось открыть видео файл")
    exit
else:
    while True:
        frame=camere_update(cap,turn,horizontally,vertically)

        cv2.putText(frame, 'move', (100,50), text_font, text_scale, color, text_thickness)

        if i>=1:
            cv2.putText(frame, 'left', (200,50), text_font, text_scale, color, text_thickness)
            move_center, move_radius = detect_and_track_colored_objects(frame, lower_move, upper_move)
            if move_center is not None:
                cv2.circle(frame, move_center, move_radius, (255, 0, 0), 2)

        if i>=2:
            cv2.putText(frame, 'right', (300,50), text_font, text_scale, color, text_thickness)
            left_center, left_radius = detect_and_track_colored_objects(frame, lower_left, upper_left)
            if left_center is not None:
                cv2.circle(frame, left_center, left_radius, (0, 255, 0), 2)
  
        if i>=3:
            rigth_center, rigth_radius = detect_and_track_colored_objects(frame, lower_rigth, upper_rigth)
            if rigth_center is not None:
                cv2.circle(frame, rigth_center, rigth_radius, (0, 255, 255), 2)

        cv2.imshow("setting mouse", frame)
        cv2.setMouseCallback("setting mouse", mouse_click)

        if cv2.waitKey(1) &  0xFF == ord('q') or i == 4:
            with open('color.txt','a')as fa:
                fa.write('move up:\n')
                fa.write(f"'[{lower_move[0]}, {lower_move[1]}, {lower_move[2]}]'\n")
                fa.write('move down:\n')
                fa.write(f"'[{upper_move[0]}, {upper_move[1]}, {upper_move[2]}]'\n")

                fa.write('left up:\n')
                fa.write(f"'[{lower_left[0]}, {lower_left[1]}, {lower_left[2]}]'\n")
                fa.write('left dowm:\n')
                fa.write(f"'[{upper_left[0]}, {upper_left[1]}, {upper_left[2]}]'\n")

                fa.write('right up:\n')
                fa.write(f"'[{lower_rigth[0]}, {lower_rigth[1]}, {lower_rigth[2]}]'\n")
                fa.write('right down:\n')
                fa.write(f"'[{upper_rigth[0]}, {upper_rigth[1]}, {upper_rigth[2]}]'\n")

            break

        if show_frame('setting mouse',frame, close):
            break

    cap.release()
    cv2.destroyAllWindows()