from socket import timeout
import cv2
import numpy as np
import os
import win32com.client
import subprocess

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

def mouse_click(event, x, y, flags, param):
    global rigth_center, rigth_radius
    global left_center, left_radius, move_center, move_radius
    global lower_move,upper_move, lower_left, upper_left, lower_rigth, upper_rigth, i

    if event == cv2.EVENT_LBUTTONDBLCLK and i<3:
        i += 1
        with open('color.txt','a')as fa:
            if i == 1:
                bgr_color = frame[y, x]
                hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
                lower_rigth = np.array([int(hsv_color[0, 0, 0]) - 10, 100, 100])
                upper_rigth = np.array([int(hsv_color[0, 0, 0]) + 10, 255, 255])
                fa.write('left up:\n')
                fa.write(f"'[{lower_rigth[0]}, {lower_rigth[1]}, {lower_rigth[2]}]'\n")
                fa.write('left down:\n')
                fa.write(f"'[{upper_rigth[0]}, {upper_rigth[1]}, {upper_rigth[2]}]'\n")
            if i == 2:
                bgr_color = frame[y, x]
                hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
                lower_left = np.array([int(hsv_color[0, 0, 0]) - 10, 100, 100])
                upper_left = np.array([int(hsv_color[0, 0, 0]) + 10, 255, 255])
                fa.write('right up:\n')
                fa.write(f"'[{lower_left[0]}, {lower_left[1]}, {lower_left[2]}]'\n")
                fa.write('right dowm:\n')
                fa.write(f"'[{upper_left[0]}, {upper_left[1]}, {upper_left[2]}]'\n")
            if i == 3:
                bgr_color = frame[y, x]
                hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
                lower_move = np.array([int(hsv_color[0, 0, 0]) - 10, 100, 100])
                upper_move = np.array([int(hsv_color[0, 0, 0]) + 10, 255, 255])
                fa.write('move up:\n')
                fa.write(f"'[{lower_move[0]}, {lower_move[1]}, {lower_move[2]}]'\n")
                fa.write('move down:\n')
                fa.write(f"'[{upper_move[0]}, {upper_move[1]}, {upper_move[2]}]'\n")

def detect_and_track_colored_objects(frame, lower_rigth, upper_rigth):
    rigth_center = None
    rigth_radius = 0

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_rigth = cv2.inRange(hsv, lower_rigth, upper_rigth)

    kernel = np.ones((3, 3), np.uint8)
    mask_rigth = cv2.morphologyEx(mask_rigth, cv2.MORPH_OPEN, kernel, iterations=2)
    mask_rigth = cv2.morphologyEx(mask_rigth, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours_rigth, _ = cv2.findContours(mask_rigth, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_rigth:
        if cv2.contourArea(contour) > 100:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > rigth_radius:
                rigth_center = (int(x), int(y))
                rigth_radius = int(radius)
    return rigth_center, rigth_radius


cap = cv2.VideoCapture(var3)

i = 0
text_font = cv2.FONT_HERSHEY_SIMPLEX
text_scale = 1
text_thickness = 2
color=(255, 192, 203)


if not cap.isOpened():
    print("Не удалось открыть видео файл")
    exit
else:

    with open("color.txt", "a") as fa:

        while True:

            ret, frame = cap.read()
            w,h = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            if turn==90 or turn==270:
                center_x = 240
                center_y = 240
                frame=cv2.resize(frame, (h,w), cv2.INTER_AREA)
            else:
                center_y = w / 2
                center_x = h / 2
            M = cv2.getRotationMatrix2D((center_x, center_y), turn, 1)

            frame = cv2.warpAffine(frame, M, (w,h))

            if horizontally==1:
                frame=cv2.flip(frame,1)
            if vertically==1:
                frame=cv2.flip(frame,0)

            cv2.putText(frame, 'left', (100,50), text_font, text_scale, color, text_thickness)

            if i>=1:
                cv2.putText(frame, 'right', (200,50), text_font, text_scale, color, text_thickness)
                rigth_center, rigth_radius = detect_and_track_colored_objects(frame, lower_rigth, upper_rigth)
                if rigth_center is not None:
                    cv2.circle(frame, rigth_center, rigth_radius, (0, 255, 255), 2)

            if i>=2:
                cv2.putText(frame, 'move', (300,50), text_font, text_scale, color, text_thickness)
                left_center, left_radius = detect_and_track_colored_objects(frame, lower_left, upper_left)
                if left_center is not None:
                    cv2.circle(frame, left_center, left_radius, (0, 255, 0), 2)

            if i>=3:
                move_center, move_radius = detect_and_track_colored_objects(frame, lower_move, upper_move)
                if move_center is not None:
                    cv2.circle(frame, move_center, move_radius, (255, 0, 0), 2)

            cv2.imshow("setting mouse", frame)
            cv2.setMouseCallback("setting mouse", mouse_click)

            if cv2.waitKey(1) &  0xFF == ord('q') or i == 3:
                break

        cap.release()
        cv2.destroyAllWindows()
        timeout(2)
        subprocess.run(['python','start.py'])