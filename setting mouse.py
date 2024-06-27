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
    global yellow_center, yellow_radius
    global green_center, green_radius, blue_center, blue_radius
    global lower_blue,upper_blue, lower_green, upper_green, lower_yellow, upper_yellow, i

    if event == cv2.EVENT_LBUTTONDBLCLK and i<3:
        i += 1
        with open('color.txt','a')as fa:
            if i == 1:
                bgr_color = frame[y, x]
                hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
                lower_yellow = np.array([int(hsv_color[0, 0, 0]) - 10, 100, 100])
                upper_yellow = np.array([int(hsv_color[0, 0, 0]) + 10, 255, 255])
                fa.write('left up:\n')
                fa.write(f"'[{lower_yellow[0]}, {lower_yellow[1]}, {lower_yellow[2]}]'\n")
                fa.write('left down:\n')
                fa.write(f"'[{upper_yellow[0]}, {upper_yellow[1]}, {upper_yellow[2]}]'\n")
            if i == 2:
                bgr_color = frame[y, x]
                hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
                lower_green = np.array([int(hsv_color[0, 0, 0]) - 10, 100, 100])
                upper_green = np.array([int(hsv_color[0, 0, 0]) + 10, 255, 255])
                fa.write('right up:\n')
                fa.write(f"'[{lower_green[0]}, {lower_green[1]}, {lower_green[2]}]'\n")
                fa.write('right dowm:\n')
                fa.write(f"'[{upper_green[0]}, {upper_green[1]}, {upper_green[2]}]'\n")
            if i == 3:
                bgr_color = frame[y, x]
                hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
                lower_blue = np.array([int(hsv_color[0, 0, 0]) - 10, 100, 100])
                upper_blue = np.array([int(hsv_color[0, 0, 0]) + 10, 255, 255])
                fa.write('move up:\n')
                fa.write(f"'[{lower_blue[0]}, {lower_blue[1]}, {lower_blue[2]}]'\n")
                fa.write('move down:\n')
                fa.write(f"'[{upper_blue[0]}, {upper_blue[1]}, {upper_blue[2]}]'\n")

def detect_and_track_colored_objects(frame, lower_yellow, upper_yellow):
    yellow_center = None
    yellow_radius = 0

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    kernel = np.ones((3, 3), np.uint8)
    mask_yellow = cv2.morphologyEx(mask_yellow, cv2.MORPH_OPEN, kernel, iterations=2)
    mask_yellow = cv2.morphologyEx(mask_yellow, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_yellow:
        if cv2.contourArea(contour) > 100:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > yellow_radius:
                yellow_center = (int(x), int(y))
                yellow_radius = int(radius)
    return yellow_center, yellow_radius


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
                yellow_center, yellow_radius = detect_and_track_colored_objects(frame, lower_yellow, upper_yellow)
                if yellow_center is not None:
                    cv2.circle(frame, yellow_center, yellow_radius, (0, 255, 255), 2)

            if i>=2:
                cv2.putText(frame, 'move', (300,50), text_font, text_scale, color, text_thickness)
                green_center, green_radius = detect_and_track_colored_objects(frame, lower_green, upper_green)
                if green_center is not None:
                    cv2.circle(frame, green_center, green_radius, (0, 255, 0), 2)

            if i>=3:
                blue_center, blue_radius = detect_and_track_colored_objects(frame, lower_blue, upper_blue)
                if blue_center is not None:
                    cv2.circle(frame, blue_center, blue_radius, (255, 0, 0), 2)

            cv2.imshow("setting mouse", frame)
            cv2.setMouseCallback("setting mouse", mouse_click)

            if cv2.waitKey(1) &  0xFF == ord('q') or i == 3:
                break

        cap.release()
        cv2.destroyAllWindows()
        timeout(2)
        subprocess.run(['python','start.py'])