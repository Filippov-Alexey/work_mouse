import numpy as np
import cv2

def show_frame(name, frame, close):
    cv2.imshow(name, frame)

    if cv2.waitKey(1) == ord('q'):
        return True

    if close==1 and cv2.getWindowProperty(name, cv2.WND_PROP_VISIBLE) < 1:
        return True

    return False

def detect_and_track_colored_objects(frame, lower_rigth, upper_rigth):
    rigth_center = None
    rigth_radius = 0

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_rigth = cv2.inRange(hsv, lower_rigth, upper_rigth)

    kernel = np.ones((3, 3), np.uint8)
    mask_rigth = cv2.morphologyEx(mask_rigth, cv2.MORPH_OPEN, kernel, iterations=2)
    mask_rigth = cv2.morphologyEx(mask_rigth, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours_rigth, _ = cv2.findContours(mask_rigth, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_rigth:
        if cv2.contourArea(contour) > 100:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > rigth_radius:
                rigth_center = (int(x), int(y))
                rigth_radius = int(radius)
                if rigth_radius > 40:
                    rigth_radius = 40

    return rigth_center, rigth_radius

def detect_and_track_objects(frame, lower_left, upper_left, lower_move, upper_move, lower_right, upper_right):

    left, right, move = False, False, False

    left_center, left_radius = detect_and_track_colored_objects(frame, lower_left, upper_left)
    move_center, move_radius = detect_and_track_colored_objects(frame, lower_move, upper_move)
    right_center, right_radius = detect_and_track_colored_objects(frame, lower_right, upper_right)

    if move_center is not None:
        cv2.circle(frame, move_center, move_radius-5, (0, 0, 0), 2)
        move = True
    if right_center is not None:
        cv2.circle(frame, right_center, right_radius-5, (125, 85, 41), 2)
        right = True
    if left_center is not None:
        cv2.circle(frame, left_center, left_radius-5, (258, 255, 256), 2)
        left = True

    return left,move,right

def detect_and_track_two_objects(frame, lower_move, upper_move, lower_left, upper_left):

    left, move = False, False

    left_center, left_radius = detect_and_track_colored_objects(frame, lower_left, upper_left)
    move_center, move_radius = detect_and_track_colored_objects(frame, lower_move, upper_move)

    if move_center is not None:
        cv2.circle(frame, move_center, move_radius-5, (0, 0, 0), 2)
        move = True
    if left_center is not None:
        cv2.circle(frame, left_center, left_radius-5, (258, 255, 256), 2)
        left = True

    return left,move












