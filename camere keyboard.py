import cv2
import numpy as np
import time
from key import *
from move import * 
from detect import *
from keyboard_layout import *
from read_file import *
from data import *
from run import *
def update(l):
    frame=camere_update(cap,turn,horizontally,vertically)

    left_center, left_radius,move_center, move_radius, square_top,square_bottom,square_left,square_right=keylay(cap,shift,frame,lower_left, upper_left, lower_move, upper_move)

    if move_center is not None and left_center is None:
        cv2.circle(frame, move_center, move_radius, (255, 0, 0), 2)
        l=False
        
    if move_center is not None and left_center is not None:
        cv2.circle(frame, move_center, move_radius, (0, 255, 0), 2)
        cv2.circle(frame, left_center, left_radius, (255, 255, 0), 2)
        if l==False:
            sim,l=move_cursor(move_center, square_left, square_right, square_top, square_bottom, l)
            key(sim)

    return frame,l

lay='ru'    
every_second_line2 = read_every_second_line('color keyboard.txt')

every_second_line1 = read_every_second_line('settings camere keyboard.txt')
horizontally=int(every_second_line1[1])
vertically=int(every_second_line1[2])
turn=int(every_second_line1[3])
camera = int(every_second_line1[0])
close = int(every_second_line1[4])


index=run_command_wait('python "test keyboard.py"')

slower_move = np.array(eval(eval(every_second_line2[0+1*int(index)])),dtype=np.uint8)
upper_move = np.array(eval(eval(every_second_line2[1+1*int(index)])),dtype=np.uint8)
lower_left = np.array(eval(eval(every_second_line2[2+1*int(index)])),dtype=np.uint8)
upper_left = np.array(eval(eval(every_second_line2[3+1*int(index)])),dtype=np.uint8)

cap = cv2.VideoCapture(camera)

while True:
    time.sleep(0.2)
    frame,l=update(l)

    if show_frame('keyboard',frame, close):
        break

cap.release()
cv2.destroyAllWindows()


