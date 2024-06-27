import cv2
import time
import numpy as np
import pyautogui
from icecream import ic

ic.configureOutput(includeContext=True,prefix='ic:')

def read_every_second_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    every_second_line = []
    for index in range(1, len(lines), 2):
        every_second_line.append(lines[index])
    
    return every_second_line

def move_cursor(blue_center, square_left, square_right, square_top, square_bottom, sm):
    x, y = blue_center
    dx, dy = 0, 0

    if square_left <= x <= square_right and square_top <= y <= square_bottom:
        dx = -sm
        dy = -sm
    elif square_left < x <= 2 * square_right and square_top <= y <= square_bottom:
        dy = -sm
    elif square_left < x <= 3 * square_right and square_top <= y <= square_bottom:
        dx = sm
        dy = -sm
    elif square_top <= x <= square_right and square_top <= y <= 2 * square_bottom:
        dx = -sm
    elif square_top <= x <= 2 * square_right and square_top <= y <= 2 * square_bottom:
        pass
    elif square_top <= x <= 3 * square_right and square_top <= y <= 2 * square_bottom:
        dx = sm
    elif square_top <= x <= square_right and square_top <= y <= 3 * square_bottom:
        dx = -sm
        dy = sm
    elif square_top <= x <= 2 * square_right and square_top <= y <= 3 * square_bottom:
        dy = sm
    elif square_top <= x <= 3 * square_right and square_top <= y <= 3 * square_bottom:
        dx = sm
        dy = sm

    if dx or dy:
        screen_x, screen_y = pyautogui.position()
        new_x = screen_x + dx
        new_y = screen_y + dy
        pyautogui.moveTo(new_x, new_y)

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

def handle_mouse_center(frame, green_center, green_radius, sec, button, color):
    cv2.circle(frame, green_center, green_radius, color, 2)
    pyautogui.mouseDown(button=button)
    pyautogui.mouseUp(button=button)
    time.sleep(sec)

every_second_line = read_every_second_line('settings.txt')
every_second_line2 = read_every_second_line('color.txt')
horizontally=int(every_second_line[5])
vertically=int(every_second_line[6])
turn=int(every_second_line[7])
sec = float(every_second_line[0])
sm = int(every_second_line[1])
camera = int(every_second_line[2])
close = int(every_second_line[8])
lower_yellow = []
upper_yellow = []
lower_green = []
upper_green = []
lower_blue = []
upper_blue = []

lower_yellow = np.array(eval(eval(every_second_line2[0])),dtype=np.uint8)
upper_yellow = np.array(eval(eval(every_second_line2[1])),dtype=np.uint8)
lower_green = np.array(eval(eval(every_second_line2[2])),dtype=np.uint8)
upper_green = np.array(eval(eval(every_second_line2[3])),dtype=np.uint8)
lower_blue = np.array(eval(eval(every_second_line2[4])),dtype=np.uint8)
upper_blue = np.array(eval(eval(every_second_line2[5])),dtype=np.uint8)

cap = cv2.VideoCapture(camera)
text_font = cv2.FONT_HERSHEY_SIMPLEX
text_scale = 1
text_thickness = 2
pyautogui.FAILSAFE = False
screen_width,screen_height = pyautogui.size()
l=False
r=False

cell_width = int(cap.get(3) / 3)
cell_height = int(cap.get(4) / 3)
square_top = 0 
square_bottom = cell_height
square_left = 0
square_right = cell_width
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

    square_index = 0

    for i in range(3):
        for j in range(3):
            x = j * cell_width
            y = i * cell_height
            cv2.rectangle(frame, (x, y), (x + cell_width, y + cell_height), (0, 0, 0, 255), 2)
            cv2.putText(frame, str(square_index + 1), (x + cell_width // 2 - 10, y + cell_height // 2 + 10),
                        text_font, text_scale, (255, 192, 203), text_thickness)
            square_index += 1

    yellow_center, yellow_radius=detect_and_track_colored_objects(frame, lower_yellow, upper_yellow)
    green_center, green_radius=detect_and_track_colored_objects(frame, lower_green, upper_green)
    blue_center, blue_radius=detect_and_track_colored_objects(frame, lower_blue, upper_blue)

    if green_center is not None and blue_center is None and yellow_center is None:
        handle_mouse_center(frame,green_center,green_radius,sec,'right',(0, 255, 0))

    if yellow_center is not None and blue_center is None and green_center is None:
        handle_mouse_center(frame,yellow_center,yellow_radius,sec,'left',(0, 0, 255))

    if blue_center is not None and yellow_center is None and green_center is None:
        cv2.circle(frame, blue_center, blue_radius, (255, 0, 0), 2)
        move_cursor(blue_center, square_left, square_right, square_top, square_bottom, sm)

    if blue_center is not None and yellow_center is not None and green_center is None:
        cv2.circle(frame, blue_center, blue_radius, (255, 255, 0), 2)
        pyautogui.mouseDown(button='left')
        l=True
        move_cursor(blue_center, square_left, square_right, square_top, square_bottom, sm)

    if blue_center is not None and yellow_center is None and green_center is not None:
        cv2.circle(frame, green_center, green_radius, (0, 255, 100), 2)
        pyautogui.mouseDown(button='right')
        r=True
        move_cursor(blue_center, square_left, square_right, square_top, square_bottom, sm)

    if blue_center is None and yellow_center is None and green_center is None:
        if r:
            pyautogui.mouseUp(button='right')
            r=False
        if l:
            pyautogui.mouseUp(button='left')
            l=False
         
    cv2.imshow("Work mouse", frame)

    if cv2.waitKey(1) == ord('q'):
        break

    if close==1 and cv2.getWindowProperty('Work mouse', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()


