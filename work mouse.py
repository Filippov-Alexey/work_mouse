import cv2
import time
import numpy as np
import pyautogui
with open('settings.txt', 'r') as file:
    lines = file.readlines()

every_second_line = []
for index in range(1, len(lines), 2):
    every_second_line.append(lines[index])

with open('color.txt', 'r') as file:
    lines = file.readlines()

every_second_line2 = []
for index in range(1, len(lines), 2):
    every_second_line2.append(lines[index])


sec = every_second_line[0]
speed = every_second_line[1]
camera = int(every_second_line[2])
var5 = eval(every_second_line2[0])
var6 = eval(every_second_line2[1])
var7 = eval(every_second_line2[2])
var8 = eval(every_second_line2[3])
var9 = eval(every_second_line2[4])
var10 = eval(every_second_line2[5])


lower_yellow = []
upper_yellow = []
lower_green = []
upper_green = []
lower_blue = []
upper_blue = []

lower_yellow = np.array(eval(var5),dtype=np.uint8)
upper_yellow = np.array(eval(var6),dtype=np.uint8)
lower_green = np.array(eval(var7),dtype=np.uint8)
upper_green = np.array(eval(var8),dtype=np.uint8)
lower_blue = np.array(eval(var9),dtype=np.uint8)
upper_blue = np.array(eval(var10),dtype=np.uint8)

cap = cv2.VideoCapture(camera)
yellow_center = None
yellow_radius = 0
green_center = None
green_radius = 0
blue_center = None
blue_radius = 0
rect_width = int(cap.get(3) / 3)
rect_height = int(cap.get(4) / 3)

text_font = cv2.FONT_HERSHEY_SIMPLEX
text_scale = 1
text_thickness = 2
sm = int(speed)
ts = float(sec)
pyautogui.FAILSAFE = False
screen_width,screen_height = pyautogui.size()
l=False
r=False
while True:
    ret, frame = cap.read()
    cell_width = int(cap.get(3) / 3)
    cell_height = int(cap.get(4) / 3)

    square_index = 0

    for i in range(3):
        for j in range(3):
            x = j * cell_width
            y = i * cell_height
            cv2.rectangle(frame, (x, y), (x + cell_width, y + cell_height), (0, 0, 0, 255), 2)
            cv2.putText(frame, str(square_index + 1), (x + cell_width // 2 - 10, y + cell_height // 2 + 10),
                        text_font, text_scale, (255, 192, 203), text_thickness)
            square_index += 1

    yellow_center = None
    yellow_radius = 0
    green_center = None
    green_radius = 0
    blue_center = None
    blue_radius = 0

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    kernel = np.ones((3, 3), np.uint8)
    mask_yellow = cv2.morphologyEx(mask_yellow, cv2.MORPH_OPEN, kernel, iterations=2)
    mask_yellow = cv2.morphologyEx(mask_yellow, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel, iterations=2)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel, iterations=2)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_yellow:
        area = cv2.contourArea(contour)
        if area > 100:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > yellow_radius:
                yellow_center = (int(x), int(y))
                yellow_radius = int(radius)

    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_green:
        area = cv2.contourArea(contour)
        if area > 100:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > green_radius:
                green_center = (int(x), int(y))
                green_radius = int(radius)

    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_blue:
        area = cv2.contourArea(contour)
        if area > 100:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > blue_radius:
                blue_center = (int(x), int(y))
                blue_radius = int(radius)

    if green_center is not None and blue_center is None and yellow_center is None:
        cv2.circle(frame, green_center, green_radius, (0, 255, 0), 2)
        pyautogui.mouseDown(button='right')
        pyautogui.mouseUp(button='right')
        time.sleep(ts)

    if yellow_center is not None and blue_center is None and green_center is None:
        cv2.circle(frame, yellow_center, yellow_radius, (0, 255, 255), 2)
        pyautogui.mouseDown(button='left')
        pyautogui.mouseUp(button='left')
        time.sleep(ts)

    if blue_center is not None and yellow_center is None and green_center is None:
        cv2.circle(frame, blue_center, blue_radius, (255, 0, 0), 2)
        square_top = 0 * cell_height
        square_bottom = 1 * cell_height
        square_left = 0 * cell_width
        square_right = 1 * cell_width

        if square_left <= blue_center[0] <= square_right and square_top <= blue_center[1] <= square_bottom:
            cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
            screen_x, screen_y = pyautogui.position()
            new_x = screen_x - sm
            new_y = screen_y - sm
            pyautogui.moveTo(new_x, new_y)
        elif square_left < blue_center[0] <= 2 * square_right and square_top <= blue_center[1] <= square_bottom:
            cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
            screen_x, screen_y = pyautogui.position()
            new_x = screen_x
            new_y = screen_y - sm
            pyautogui.moveTo(new_x, new_y)
        elif square_left < blue_center[0] <= 3 * square_right and square_top <= blue_center[1] <= square_bottom:
            cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
            screen_x, screen_y = pyautogui.position()
            new_x = screen_x + sm
            new_y = screen_y - sm
            pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= square_right and square_top <= blue_center[1] <= 2 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x - sm
           new_y = screen_y
           pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= 2 * square_right and square_top <= blue_center[1] <= 2 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x
           new_y = screen_y
           pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= 3 * square_right and square_top <= blue_center[1] <= 2 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x + sm
           new_y = screen_y
           pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= square_right and square_top <= blue_center[1] <= 3 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x - sm
           new_y = screen_y + sm
           pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= 2 * square_right and square_top <= blue_center[1] <= 3 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x
           new_y = screen_y+sm
           pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= 3 * square_right and square_top <= blue_center[1] <= 3 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x + sm
           new_y = screen_y + sm
           pyautogui.moveTo(new_x, new_y)

    if blue_center is not None and yellow_center is not None and green_center is None:
        l=True
        pyautogui.mouseDown(button='left')
        square_top = 0 * cell_height
        square_bottom = 1 * cell_height
        square_left = 0 * cell_width
        square_right = 1 * cell_width

        if square_left <= blue_center[0] <= square_right and square_top <= blue_center[1] <= square_bottom:
            cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
            screen_x, screen_y = pyautogui.position()
            new_x = screen_x - sm
            new_y = screen_y - sm
            pyautogui.moveTo(new_x, new_y)
        elif square_left < blue_center[0] <= 2 * square_right and square_top <= blue_center[1] <= square_bottom:
            screen_x, screen_y = pyautogui.position()
            cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
            new_x = screen_x
            new_y = screen_y - sm
            pyautogui.moveTo(new_x, new_y)
        elif square_left < blue_center[0] <= 3 * square_right and square_top <= blue_center[1] <= square_bottom:
            cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
            screen_x, screen_y = pyautogui.position()
            new_x = screen_x + sm
            new_y = screen_y - sm
            pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= square_right and square_top <= blue_center[1] <= 2 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x - sm
           new_y = screen_y
           pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= 2 * square_right and square_top <= blue_center[1] <= 2 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x
           new_y = screen_y
           pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= 3 * square_right and square_top <= blue_center[1] <= 2 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x + sm
           new_y = screen_y
           pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= square_right and square_top <= blue_center[1] <= 3 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x - sm
           new_y = screen_y + sm
           pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= 2 * square_right and square_top <= blue_center[1] <= 3 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x
           new_y = screen_y+sm
           pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= 3 * square_right and square_top <= blue_center[1] <= 3 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x + sm
           new_y = screen_y + sm
           pyautogui.moveTo(new_x, new_y)

    if blue_center is not None and yellow_center is None and green_center is not None:
        cv2.circle(frame, blue_center, blue_radius, (255, 0, 0), 2)
        cv2.circle(frame, green_center, green_radius, (0, 255, 0), 2)
        pyautogui.mouseDown(button='right')
        r=True
        square_top = 0 * cell_height
        square_bottom = 1 * cell_height
        square_left = 0 * cell_width
        square_right = 1 * cell_width

        if square_left <= blue_center[0] <= square_right and square_top <= blue_center[1] <= square_bottom:
            cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
            screen_x, screen_y = pyautogui.position()
            new_x = screen_x - sm
            new_y = screen_y - sm
            pyautogui.moveTo(new_x, new_y)
        elif square_left < blue_center[0] <= 2 * square_right and square_top <= blue_center[1] <= square_bottom:
            screen_x, screen_y = pyautogui.position()
            cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
            new_x = screen_x
            new_y = screen_y - sm
            pyautogui.moveTo(new_x, new_y)
        elif square_left < blue_center[0] <= 3 * square_right and square_top <= blue_center[1] <= square_bottom:
            cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
            screen_x, screen_y = pyautogui.position()
            new_x = screen_x + sm
            new_y = screen_y - sm
            pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= square_right and square_top <= blue_center[1] <= 2 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x - sm
           new_y = screen_y
           pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= 2 * square_right and square_top <= blue_center[1] <= 2 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x
           new_y = screen_y
           pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= 3 * square_right and square_top <= blue_center[1] <= 2 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x + sm
           new_y = screen_y
           pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= square_right and square_top <= blue_center[1] <= 3 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x - sm
           new_y = screen_y + sm
           pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= 2 * square_right and square_top <= blue_center[1] <= 3 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x
           new_y = screen_y+sm
           pyautogui.moveTo(new_x, new_y)
        elif square_top <= blue_center[0] <= 3 * square_right and square_top <= blue_center[1] <= 3 * square_bottom:
           cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), 5, (0, 0, 255), -1)
           screen_x, screen_y = pyautogui.position()
           new_x = screen_x + sm
           new_y = screen_y + sm
           pyautogui.moveTo(new_x, new_y)

    cv2.imshow("Work mouse", frame)


    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


