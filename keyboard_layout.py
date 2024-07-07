import cv2
import keyboard
from detect import *
from run import *
from data import *
from key import *
def keylay(cap,shift,frame,lower_left, upper_left, lower_move, upper_move):
    cell_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 7)
    cell_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 7)
    square_top = 0 
    square_bottom = cell_height
    square_left = 0
    square_right = cell_width
    square_index=0

    lay = run_command("python layout.py")

    if shift==False:
        for i in range(7):
            for j in range(7):
                x = j * cell_width
                y = i * cell_height
                cv2.rectangle(frame, (x, y), (x + cell_width, y + cell_height), (0, 0, 0, 255), 2)
                if lay=='ru':
                    cv2.putText(frame, str(keyru[square_index]), (x + cell_width // 2-30, y + cell_height // 2 + 10),
                                text_font, text_scale, (255, 192, 203), text_thickness)
                else:
                    cv2.putText(frame, str(keyen[square_index]), (x + cell_width // 2-30, y + cell_height // 2 + 10),
                                text_font, text_scale, (255, 192, 203), text_thickness)
                square_index += 1
    else:
        for i in range(7):
            for j in range(7):
                x = j * cell_width
                y = i * cell_height
                cv2.rectangle(frame, (x, y), (x + cell_width, y + cell_height), (0, 0, 0, 255), 2)
                if lay=='ru':
                    cv2.putText(frame, str(keyrushift[square_index]), (x + cell_width // 2-30, y + cell_height // 2 + 10),
                                text_font, text_scale, (255, 192, 203), text_thickness)
                else:
                    cv2.putText(frame, str(keyenshift[square_index]), (x + cell_width // 2-30, y + cell_height // 2 + 10),
                                text_font, text_scale, (255, 192, 203), text_thickness)
                square_index += 1
                    
    left_center, left_radius=detect_and_track_colored_objects(frame, lower_left, upper_left)
    move_center, move_radius=detect_and_track_colored_objects(frame, lower_move, upper_move)
    return left_center, left_radius,move_center, move_radius, square_top,square_bottom,square_left,square_right

def key(keys):
    global shift
    if keys=='shift':
        if shift==False:
            keyboard.press(keys)
            shift=True
        else:
            keyboard.release(keys)
            shift=False
    else:
        keyboard.press(keys)
        keyboard.release(keys)
