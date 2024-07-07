import os
import cv2
import time
import numpy as np
import pyautogui
from key import *
from move import *
from detect import *
from data import *
from keyboard_layout import *
from read_file import *

def move_cursor_mouse(move_center, square_left, square_right, square_top, square_bottom, sm):
    x, y = move_center
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

    screen_x, screen_y = pyautogui.position()
    new_x = screen_x + dx
    new_y = screen_y + dy
    pyautogui.moveTo(new_x, new_y)

def handle_mouse_center(frame, left_center, left_radius, sec, button, color):
    cv2.circle(frame, left_center, left_radius, color, 2)
    pyautogui.mouseDown(button=button)
    pyautogui.mouseUp(button=button)
    time.sleep(sec)

def move_mouse():
    global ck,l,r
    square_index=0
    cell_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 3)
    cell_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 3)
    square_top = 0 
    square_bottom = cell_height
    square_left = 0
    square_right = cell_width
    for i in range(3):
        for j in range(3):
            x = j * cell_width
            y = i * cell_height
            cv2.rectangle(frame, (x, y), (x + cell_width, y + cell_height), (0, 0, 0, 255), 2)
            cv2.putText(frame, str(square_index + 1), (x + cell_width // 2 - 10, y + cell_height // 2 + 10),
                        text_font, text_scale, (255, 192, 203), text_thickness)
            square_index += 1

    rigth_center, rigth_radius=detect_and_track_colored_objects(frame, lower_rigth, upper_rigth)
    left_center, left_radius=detect_and_track_colored_objects(frame, lower_left, upper_left)
    move_center, move_radius=detect_and_track_colored_objects(frame, lower_move, upper_move)

    if left_center is not None and move_center is None and rigth_center is None:
        handle_mouse_center(frame,left_center,left_radius,sec,'right',(0, 255, 0))

    elif rigth_center is not None and move_center is None and left_center is None:
        handle_mouse_center(frame,rigth_center,rigth_radius,sec,'left',(0, 0, 255))

    elif move_center is not None and rigth_center is None and left_center is None:
        cv2.circle(frame, move_center, move_radius, (255, 0, 0), 2)
        move_cursor_mouse(move_center, square_left, square_right, square_top, square_bottom, sm)

    elif move_center is not None and rigth_center is not None and left_center is None:
        cv2.circle(frame, move_center, move_radius, (255, 255, 0), 2)
        pyautogui.mouseDown(button='left')
        l=True
        move_cursor_mouse(move_center, square_left, square_right, square_top, square_bottom, sm)

    elif move_center is not None and rigth_center is None and left_center is not None:
        cv2.circle(frame, left_center, left_radius, (0, 255, 100), 2)
        pyautogui.mouseDown(button='right')
        r=True
        move_cursor_mouse(move_center, square_left, square_right, square_top, square_bottom, sm)

    elif move_center is None and rigth_center is None and left_center is None:
        if r:
            pyautogui.mouseUp(button='right')
            r=False
        if l:
            pyautogui.mouseUp(button='left')
            l=False

    elif move_center is None and rigth_center is not None and left_center is not None:
        return True

every_second_line = read_every_second_line('settings.txt')
every_second_line2 = read_every_second_line('color.txt')
if os.path.exists('settings camere keyboard.txt'):
    every_second_line1 = read_every_second_line('settings camere keyboard.txt')
    cam=int(every_second_line1[0])
else:
    cam=''
horizontally=int(every_second_line[5])
vertically=int(every_second_line[6])
turn=int(every_second_line[7])
sec = float(every_second_line[0])
sm = int(every_second_line[1])
camera = int(every_second_line[2])
close = int(every_second_line[8]) 
camtokey = int(every_second_line[9])

index=run_command_wait('python "test mouse.py"')

lower_move = np.array(eval(eval(every_second_line2[0+1*int(index)])),dtype=np.uint8)
upper_move = np.array(eval(eval(every_second_line2[1+1*int(index)])),dtype=np.uint8)
lower_left = np.array(eval(eval(every_second_line2[2+1*int(index)])),dtype=np.uint8)
upper_left = np.array(eval(eval(every_second_line2[3+1*int(index)])),dtype=np.uint8)
lower_rigth = np.array(eval(eval(every_second_line2[4+1*int(index)])),dtype=np.uint8)
upper_rigth = np.array(eval(eval(every_second_line2[5+1*int(index)])),dtype=np.uint8)

cap = cv2.VideoCapture(camera)

ck=True
if cam==camera:
    camkey=False
else:
    camkey=True

while True:
    time.sleep(0.2)

    frame=camere_update(cap,turn,horizontally,vertically)
    if camkey==True:
        ck=move_mouse()
    elif camtokey==1:
        if ck==False or ck==None:
            ck=move_mouse()
        else:
            left_center, left_radius,move_center, move_radius, square_top,square_bottom,square_left,square_right=keylay(cap,shift,frame,lower_left, upper_left, lower_move, upper_move)
            rigth_center, rigth_radius=detect_and_track_colored_objects(frame, lower_rigth, upper_rigth)

            if move_center is not None and rigth_center is None and left_center is None:
                cv2.circle(frame, move_center, move_radius, (255, 0, 0), 2)
                l=False
                
            elif move_center is not None and rigth_center is not None and left_center is None:
                cv2.circle(frame, move_center, move_radius, (255, 255, 0), 2)
                if l==False:
                    sim,l=move_cursor(move_center, square_left, square_right, square_top, square_bottom, l)
                    key(sim)

            elif move_center is None and rigth_center is not None and left_center is not None and ck==True:
                ck=False
            
            if move_center is not None:
                cv2.circle(frame, move_center, move_radius-5, (0, 0, 0), 2)
            if rigth_center is not None:
                cv2.circle(frame, rigth_center, rigth_radius-5, (125, 85, 41), 2)
            if left_center is not None:
                cv2.circle(frame, left_center, left_radius-5, (258, 255, 256), 2)

    if show_frame('Work mouse',frame, close):
        break
cap.release()
cv2.destroyAllWindows()


