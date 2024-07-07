from key import *
def move_cursor(move_center, square_left, square_right, square_top, square_bottom, sm):
    sim = ''
    x, y = move_center

    if square_left <= x <= square_right and square_top <= y <= square_bottom:
        sim = keyen0[0]
        sm=not sm
    elif square_left < x <= 2 * square_right and square_top <= y <= square_bottom:
        sim = keyen0[1]
        sm=not sm
    elif square_left < x <= 3 * square_right and square_top <= y <= square_bottom:
        sim = keyen0[2]
        sm=not sm
    elif square_left < x <= 4 * square_right and square_top <= y <= square_bottom:
        sim = keyen0[3]
        sm=not sm
    elif square_left < x <= 5 * square_right and square_top <= y <= square_bottom:
        sim = keyen0[4]
        sm=not sm
    elif square_left < x <= 6 * square_right and square_top <= y <= square_bottom:
        sim = keyen0[5]
        sm=not sm
    elif square_left < x <= 7 * square_right and square_top <= y <= square_bottom:
        sim = keyen0[6]
        sm=not sm
    elif square_top <= x <= square_right and square_top <= y <= 2 * square_bottom:
        sim = keyen0[7]
        sm=not sm
    elif square_top <= x <= 2 * square_right and square_top <= y <= 2 * square_bottom:
        sim = keyen0[8]
        sm=not sm
    elif square_top <= x <= 3 * square_right and square_top <= y <= 2 * square_bottom:
        sim = keyen0[9]
        sm=not sm
    elif square_top <= x <= 4 * square_right and square_top <= y <= 2 * square_bottom:
        sim = keyen0[10]
        sm=not sm
    elif square_top <= x <= 5 * square_right and square_top <= y <= 2 * square_bottom:
        sim = keyen0[11]
        sm=not sm
    elif square_top <= x <= 6 * square_right and square_top <= y <= 2 * square_bottom:
        sim = keyen0[12]
        sm=not sm
    elif square_top <= x <= 7 * square_right and square_top <= y <= 2 * square_bottom:
        sim = keyen0[13]
        sm=not sm
    elif square_top <= x <= square_right and square_top <= y <= 3 * square_bottom:
        sim = keyen0[14]
        sm=not sm
    elif square_top <= x <= 2 * square_right and square_top <= y <= 3 * square_bottom:
        sim = keyen0[15]
        sm=not sm
    elif square_top <= x <= 3 * square_right and square_top <= y <= 3 * square_bottom:
        sim = keyen0[16]
        sm=not sm
    elif square_top <= x <= 4 * square_right and square_top <= y <= 3 * square_bottom:
        sim = keyen0[17]
        sm=not sm
    elif square_top <= x <= 5 * square_right and square_top <= y <= 3 * square_bottom:
        sim = keyen0[18]
        sm=not sm
    elif square_top <= x <= 6 * square_right and square_top <= y <= 3 * square_bottom:
        sim = keyen0[19]
        sm=not sm
    elif square_top <= x <= 7 * square_right and square_top <= y <= 3 * square_bottom:
        sim = keyen0[20]
        sm=not sm
    elif square_top <= x <= square_right and square_top <= y <= 4 * square_bottom:
        sim = keyen0[21]
        sm=not sm
    elif square_top <= x <= 2 * square_right and square_top <= y <= 4 * square_bottom:
        sim = keyen0[22]
        sm=not sm
    elif square_top <= x <= 3 * square_right and square_top <= y <= 4 * square_bottom:
        sim = keyen0[23]
        sm=not sm
    elif square_top <= x <= 4 * square_right and square_top <= y <= 4 * square_bottom:
        sim = keyen0[24]
        sm=not sm
    elif square_top <= x <= 5 * square_right and square_top <= y <= 4 * square_bottom:
        sim = keyen0[25]
        sm=not sm
    elif square_top <= x <= 6 * square_right and square_top <= y <= 4 * square_bottom:
        sim = keyen0[26]
        sm=not sm
    elif square_top <= x <= 7 * square_right and square_top <= y <= 4 * square_bottom:
        sim = keyen0[27]
        sm=not sm
    elif square_top <= x <= square_right and square_top <= y <= 5 * square_bottom:
        sim = keyen0[28]
        sm=not sm
    elif square_top <= x <= 2 * square_right and square_top <= y <= 5 * square_bottom:
        sim = keyen0[29]
        sm=not sm
    elif square_top <= x <= 3 * square_right and square_top <= y <= 5 * square_bottom:
        sim = keyen0[30]
        sm=not sm
    elif square_top <= x <= 4 * square_right and square_top <= y <= 5 * square_bottom:
        sim = keyen0[31]
        sm=not sm
    elif square_top <= x <= 5 * square_right and square_top <= y <= 5 * square_bottom:
        sim = keyen0[32]
        sm=not sm
    elif square_top <= x <= 6 * square_right and square_top <= y <= 5 * square_bottom:
        sim = keyen0[33]
        sm=not sm
    elif square_top <= x <= 7 * square_right and square_top <= y <= 5 * square_bottom:
        sim = keyen0[34]
        sm=not sm
    elif square_top <= x <= square_right and square_top <= y <= 6 * square_bottom:
        sim = keyen0[35]
        sm=not sm
    elif square_top <= x <= 2 * square_right and square_top <= y <= 6 * square_bottom:
        sim = keyen0[36]
        sm=not sm
    elif square_top <= x <= 3 * square_right and square_top <= y <= 6 * square_bottom:
        sim = keyen0[37]
        sm=not sm
    elif square_top <= x <= 4 * square_right and square_top <= y <= 6 * square_bottom:
        sim = keyen0[38]
        sm=not sm
    elif square_top <= x <= 5 * square_right and square_top <= y <= 6 * square_bottom:
        sim = keyen0[39]
        sm=not sm
    elif square_top <= x <= 6 * square_right and square_top <= y <= 6 * square_bottom:
        sim = keyen0[40]
        sm=not sm
    elif square_top <= x <= 7 * square_right and square_top <= y <= 6 * square_bottom:
        sim = keyen0[41]
        sm=not sm
    elif square_top <= x <= square_right and square_top <= y <= 7 * square_bottom:
        sim = keyen0[42]
        sm=not sm
    elif square_top <= x <= 2 * square_right and square_top <= y <= 7 * square_bottom:
        sim = keyen0[43]
        sm=not sm
    elif square_top <= x <= 3 * square_right and square_top <= y <= 7 * square_bottom:
        sim = keyen0[44]
        sm=not sm
    elif square_top <= x <= 4 * square_right and square_top <= y <= 7 * square_bottom:
        sim = keyen0[45]
        sm=not sm
    elif square_top <= x <= 5 * square_right and square_top <= y <= 7 * square_bottom:
        sim = keyen0[46]
        sm=not sm
    elif square_top <= x <= 6 * square_right and square_top <= y <= 7 * square_bottom:
        sim = keyen0[47]
        sm=not sm
    elif square_top <= x <= 7 * square_right and square_top <= y <= 7 * square_bottom:
        sim = keyen0[48]
        sm=not sm

    return sim,sm
