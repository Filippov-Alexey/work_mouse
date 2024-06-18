from socket import timeout
import cv2
import numpy as np
import os
import pythoncom
import win32com.client
import subprocess

with open('settings.txt', 'r+') as f:
    lines = f.readlines()

every_second_line = []  # Create an empty list to store every second line
for index in range(1, 10, 2):
    line = lines[index].strip()
    every_second_line.append(line)

if every_second_line[3] == "1":
    current_directory = os.getcwd()
    
    # Path to the file for which you want to create the shortcut
    source_file = os.path.join(current_directory, 'start.exe')

    # Shortcut name
    shortcut_name = 'start'

    # Path to the startup folder
    startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

    # Create the shortcut object
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut_file = os.path.join(startup_folder, f'{shortcut_name}.lnk')
    shortcut = shell.CreateShortcut(shortcut_file)
    shortcut.TargetPath = source_file
    shortcut.WorkingDirectory = os.path.dirname(source_file)
    shortcut.WindowStyle = 7  # Hidden window style (7)
    shortcut.save()

# Сохраняем каждую вторую строку в отдельные переменные
var1 = every_second_line[0]#sec
var2 = every_second_line[1]#speer
var3 = int(every_second_line[2])#cam
# Функция для обработки кликов мыши
def mouse_click(event, x, y, flags, param):
    global hsv_lower, hsv_upper, yellow_center, yellow_radius 
    global green_center, green_radius, blue_center, blue_radius
    global lower_blue,upper_blue, lower_green, upper_green, lower_yellow, upper_yellow, i

    if event == cv2.EVENT_LBUTTONDBLCLK and i<3:
        i += 1
        with open('color.txt','a')as f:
            # Записать значения переменных hsv_lower и hsv_upper в файл settings.txt
            if i == 1:
                bgr_color = frame[y, x]
                # Установить нижнюю и верхнюю границы цветового диапазона
                hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
                lower_yellow = np.array([int(hsv_color[0, 0, 0]) - 10, 100, 100])
                upper_yellow = np.array([int(hsv_color[0, 0, 0]) + 10, 255, 255])
                fa.write('left up:\n')
                fa.write(f"'[{lower_yellow[0]}, {lower_yellow[1]}, {lower_yellow[2]}]'\n")
                fa.write('left down:\n')
                fa.write(f"'[{upper_yellow[0]}, {upper_yellow[1]}, {upper_yellow[2]}]'\n")
            if i == 2:
                bgr_color = frame[y, x]
                # Установить нижнюю и верхнюю границы цветового диапазона
                hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
                lower_green = np.array([int(hsv_color[0, 0, 0]) - 10, 100, 100])
                upper_green = np.array([int(hsv_color[0, 0, 0]) + 10, 255, 255])
                fa.write('right up:\n')
                fa.write(f"'[{lower_green[0]}, {lower_green[1]}, {lower_green[2]}]'\n")
                fa.write('right dowm:\n')
                fa.write(f"'[{upper_green[0]}, {upper_green[1]}, {upper_green[2]}]'\n")
            if i == 3:
                bgr_color = frame[y, x]
                # Установить нижнюю и верхнюю границы цветового диапазона
                hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
                lower_blue = np.array([int(hsv_color[0, 0, 0]) - 10, 100, 100])
                upper_blue = np.array([int(hsv_color[0, 0, 0]) + 10, 255, 255])
                fa.write('move up:\n')
                fa.write(f"'[{lower_blue[0]}, {lower_blue[1]}, {lower_blue[2]}]'\n")
                fa.write('move down:\n')
                fa.write(f"'[{upper_blue[0]}, {upper_blue[1]}, {upper_blue[2]}]'\n")
        
# Создать объект захвата видео
cap = cv2.VideoCapture(var3)

# Установить размеры кадра
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# Создать окно

# Установить обработчик события для двойного щелчка мыши
# Инициализация переменных

i = 0
hsv_lower = None
hsv_upper = None
yellow_center = None
yellow_radius = 0
green_center = None
green_radius = 0
blue_center = None
blue_radius = 0
lower_yellow = None
upper_yellow = None
lower_green = None
upper_green = None
lower_blue = None
upper_blue = None
text_font = cv2.FONT_HERSHEY_SIMPLEX
text_scale = 1
text_thickness = 2
color=(255, 192, 203)
    
# Проверка на успешную загрузку видео
if not cap.isOpened():
    print("Не удалось открыть видео файл")
    exit
else:
 
    with open("color.txt", "a") as fa:
        # Запуск цикла для чтения видеопотока
        while True:
            try:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Обработка кадров
                    
            except cv2.error as e:
                # Обработка ошибки
                print(f"Ошибка при захвате кадра: {e}")
                continue
            # Считать кадр
            ret, frame = cap.read()
            cv2.putText(frame, 'left', (100,50), text_font, text_scale, color, text_thickness)        # Проверить, был ли выбран цветовой диапазон
            if i>=1:
                cv2.putText(frame, 'right', (200,50), text_font, text_scale, color, text_thickness)        # Проверить, был ли выбран цветовой диапазон

                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                kernel = np.ones((3, 3), np.uint8)
                mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
                mask_yellow = cv2.morphologyEx(mask_yellow, cv2.MORPH_OPEN, kernel, iterations=2)
                mask_yellow = cv2.morphologyEx(mask_yellow, cv2.MORPH_CLOSE, kernel, iterations=2)
                contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours_yellow:
                    area = cv2.contourArea(contour)
                    if area > 100:
                        (x, y), radius = cv2.minEnclosingCircle(contour)
                        if radius > yellow_radius:
                            yellow_center = (int(x), int(y))
                            yellow_radius = int(radius)
            if yellow_center is not None:
                cv2.circle(frame, yellow_center, yellow_radius, (0, 255, 255), 2)
                
            if i>=2:
                cv2.putText(frame, 'move', (300,50), text_font, text_scale, color, text_thickness)        # Проверить, был ли выбран цветовой диапазон

                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask_green = cv2.inRange(hsv, lower_green, upper_green)
                kernel = np.ones((3, 3), np.uint8)
                mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel, iterations=2)
                mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel, iterations=2)
                contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
                for contour in contours_green:
                    area = cv2.contourArea(contour)
                    if area > 100:
                        (x, y), radius = cv2.minEnclosingCircle(contour)
                        if radius > green_radius:
                            green_center = (int(x), int(y))
                            green_radius = int(radius)
            if green_center is not None:
                cv2.circle(frame, green_center, green_radius, (0, 255, 0), 2)
                        
            if i>=3:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
                kernel = np.ones((3, 3), np.uint8)
                mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel, iterations=2)
                mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_CLOSE, kernel, iterations=2)
                contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours_blue:
                    area = cv2.contourArea(contour)
                    if area > 100:
                        (x, y), radius = cv2.minEnclosingCircle(contour)
                        if radius > blue_radius:
                            blue_center = (int(x), int(y))
                            blue_radius = int(radius)
            if blue_center is not None:
                cv2.circle(frame, blue_center, blue_radius, (255, 0, 0), 2)
                
            # Показать кадр
            cv2.imshow("setting mouse", frame)
            cv2.setMouseCallback("setting mouse", mouse_click)

            # Проверить нажатие клавиши "q" для выхода
            if cv2.waitKey(1) &  0xFF == ord('q') or i == 3:
                break
                

        # Освободить ресурсы
        cap.release()
        cv2.destroyAllWindows()
        timeout(2)
        subprocess.run(['start.exe'])
