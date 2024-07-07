import cv2
from detect import *
import pyautogui

text_font = cv2.FONT_HERSHEY_COMPLEX
text_scale = 0.7
text_thickness = 2

pyautogui.FAILSAFE = False
screen_width,screen_height = pyautogui.size()
l=False
r=False
shift=False

i = 0
color=(255, 192, 203)

def camere_update(cap,turn,horizontally,vertically):
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
    return frame

def parse_color_ranges(data):
    low_mov, upp_mov, low_lef, upp_lef, low_rig, upp_rig = [], [], [], [], [], []
    if len(data)%4 == 0:
        for i in range(0, len(data), 4):
            low_mov.append(np.array(eval(eval(data[i])), dtype=np.uint8))
            upp_mov.append(np.array(eval(eval(data[i+1])), dtype=np.uint8))
            low_lef.append(np.array(eval(eval(data[i+2])), dtype=np.uint8))
            upp_lef.append(np.array(eval(eval(data[i+3])), dtype=np.uint8))
    elif len(data)%6 == 0:
        for i in range(0, len(data), 6):
            low_mov.append(np.array(eval(eval(data[i])), dtype=np.uint8))
            upp_mov.append(np.array(eval(eval(data[i+1])), dtype=np.uint8))
            low_lef.append(np.array(eval(eval(data[i+2])), dtype=np.uint8))
            upp_lef.append(np.array(eval(eval(data[i+3])), dtype=np.uint8))
            low_rig.append(np.array(eval(eval(data[i+4])), dtype=np.uint8))
            upp_rig.append(np.array(eval(eval(data[i+5])), dtype=np.uint8))
    return low_mov, upp_mov, low_lef, upp_lef, low_rig, upp_rig 


