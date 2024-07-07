from read_file import *
import cv2
import time
from detect import *
from data import *
from keyboard_layout import *

def update(line4):
    color_ranges = parse_color_ranges(line4)
    frame=camere_update(cap,turn,horizontally,vertically)
    lower_move, upper_move, lower_left, upper_left, lower_right, upper_right = color_ranges
    return frame,lower_move, upper_move, lower_left, upper_left, lower_right, upper_right
i=0
line4=read_every_second_line('color keyboard.txt')
lower_right, upper_right=None,None
line3=read_every_second_line('settings camere keyboard.txt')
horizontally=int(line3[1])
vertically=int(line3[2])
turn=int(line3[3])
sec= float(line3[0])
sm= int(line3[1])
camera= int(line3[0])
close= int(line3[4])
cap= cv2.VideoCapture(camera)

while True:
    time.sleep(0.2)

    frame, lower_move, upper_move, lower_left, upper_left, lower_right, upper_right = update(line4)

    move,left=detect_and_track_two_objects(frame, lower_move[i], upper_move[i], lower_left[i], upper_left[i])
       
    if i<=len(lower_left):
        i+=1
    if i>=len(lower_left):
        i=0
    
    if move and left:
        print(i)
        break

    if show_frame('test keyboard', frame, close):
        break

cap.release()
cv2.destroyAllWindows()