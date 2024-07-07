import sys
import cv2
import numpy as np
from detect import *
from data import *
import os

def keyboard_click(event, x, y, flags, param):
    global move_center, move_radius
    global left_center, left_radius
    global lower_move,upper_move, lower_left, upper_left, i

    if event == cv2.EVENT_LBUTTONDBLCLK:
        i += 1
        with open('color keyboard.txt','a')as fa:
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
    if event==cv2.EVENT_RBUTTONDOWN and i>0:
        i-=1
if os.path.exists('settings camere keyboard.txt'):
    with open('settings camere keyboard.txt', 'r') as file:
        lines = file.readlines()

    every_second_line = []
    for index in range(1, len(lines), 2):
        every_second_line.append(lines[index])

    var3 = int(every_second_line[0])
    horizontally=int(every_second_line[1])
    vertically=int(every_second_line[2])
    turn=int(every_second_line[3])
    close = int(every_second_line[4])

    cap = cv2.VideoCapture(var3)


    if not cap.isOpened():
        print("Не удалось открыть видео файл")
        exit
    else:

        while True:
            frame=camere_update(cap,turn,horizontally,vertically)
            cv2.putText(frame, 'move', (100,50), text_font, text_scale, color, text_thickness)

            if i>=1:
                cv2.putText(frame, 'click', (200,50), text_font, text_scale, color, text_thickness)
                move_center, move_radius = detect_and_track_colored_objects(frame, lower_move, upper_move)
                if move_center is not None:
                    cv2.circle(frame, move_center, move_radius, (0, 255, 255), 2)
            if i>=2 :
                left_center, left_radius = detect_and_track_colored_objects(frame, lower_left, upper_left)
                if left_center is not None:
                    cv2.circle(frame, left_center, left_radius, (0, 255, 255), 2)

            cv2.imshow("setting keyboard", frame)
            cv2.setMouseCallback("setting keyboard",keyboard_click)

            if cv2.waitKey(1) &  0xFF == ord('q') or i == 3:
                with open('color keyboard.txt','a')as fa:
                    fa.write('move up:\n')
                    fa.write(f"'[{lower_move[0]}, {lower_move[1]}, {lower_move[2]}]'\n")
                    fa.write('move dowm:\n')
                    fa.write(f"'[{upper_move[0]}, {upper_move[1]}, {upper_move[2]}]'\n")
                    fa.write('left up:\n')
                    fa.write(f"'[{lower_left[0]}, {lower_left[1]}, {lower_left[2]}]'\n")
                    fa.write('left down:\n')
                    fa.write(f"'[{upper_left[0]}, {upper_left[1]}, {upper_left[2]}]'\n")
                break

            if show_frame('setting keyboard',frame, close):
                break

        cap.release()
        cv2.destroyAllWindows()
else:
    sys.exit()