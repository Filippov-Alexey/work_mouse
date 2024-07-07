from read_file import *
import cv2
import time
from detect import *
from data import *
from keyboard_layout import *
 
def update(line4):
    color_ranges = parse_color_ranges(line4)
    frame=camere_update(cap,turn,horizontally,vertically)
    lower_move, upper_move, lower_left, upper_left, lower_rigth, upper_rigth = color_ranges
    return frame,lower_move, upper_move, lower_left, upper_left, lower_rigth, upper_rigth

i=0

line=read_every_second_line('settings.txt')
horizontally=int(line[5])
vertically=int(line[6])
turn=int(line[7])
sec = float(line[0])
sm = int(line[1])
camera = int(line[2])
close = int(line[8])
camtokey = int(line[9])

cap = cv2.VideoCapture(camera)
line4=read_every_second_line('color.txt')

while True:
    time.sleep(0.2)
    frame, lower_move, upper_move, lower_left, upper_left, lower_right, upper_right = update(line4)

    move,right,left=detect_and_track_objects(frame, lower_left[i], upper_left[i], lower_move[i], upper_move[i], lower_right[i], upper_right[i])

       
    if i<=len(lower_left):
        i+=1
    if i>=len(lower_left):
        i=0

    if move and right and left:
        print(i)
        break

    if show_frame('test mouse', frame, close):
        break

cap.release()
cv2.destroyAllWindows()