
import tkinter as tk
import pyautogui
import pygetwindow as gw
import time as tm

def key_press(event, key):
    global shift_pressed, alt_pressed, ctrl_pressed
    if key == 'Shift':
        tm.sleep(0.5)
        if not shift_pressed:
            print('Shift key pressed')
            shift_pressed = True
        else:
            print('Shift key released')
            shift_pressed = False

    if key=='Alt':
        tm.sleep(0.5)
        if not alt_pressed:
            pyautogui.keyDown('Alt')
            print('Alt key pressed')
            alt_pressed = True
        else:
            pyautogui.keyUp('Alt')
            print('Alt key released')
            alt_pressed = False

    if key=='Ctrl':
        tm.sleep(0.5)
        if not ctrl_pressed:
            pyautogui.keyDown('Ctrl')
            print('Ctrl key pressed')
            ctrl_pressed = True
        else:
            pyautogui.keyUp('Ctrl')
            print('Ctrl key released')
            ctrl_pressed = False

    
    windows = gw.getAllTitles()

    inactive_windows = [window for window in windows if not gw.getWindowsWithTitle(window)[0].isActive]
    if inactive_windows:
        window = gw.getWindowsWithTitle(inactive_windows[0])
        window[0].activate()

    tm.sleep(0.5)

    if shift_pressed:
        pyautogui.keyDown("Shift")
    else:
        pyautogui.keyUp('Shift')

    if ctrl_pressed:
        pyautogui.keyDown("Ctrl")
    else:
        pyautogui.keyUp('Ctrl')

    if alt_pressed:
        pyautogui.keyDown("Alt")
    else:
        pyautogui.keyUp('Alt')
    pyautogui.press(key)
window = tk.Tk()
window.attributes("-topmost", True) 
window.lift()
window.title('Экранная клавиатура')
window.resizable(width=False, height=False)
window.iconbitmap(default='key.ico')
shift_pressed = False
alt_pressed = False
ctrl_pressed = False
keys=['`','1','2','3','4','5','6','7','8','9','0','-','=']
k=['Backspace']
keys1=['Tab','q','w','e','r','t','y','u','i','o','p','[',']']
k1=['\\']
keys2=['CapsLock','a','s','d','f','g','h','j','k','l',';','\'']
k2=['Enter']
keys3=['Shift','z','x','c','v','b','n','m',',','.','/']
k3=['Shift']
keys4=['Ctrl','Alt','Space']
for key in keys:
    btn = tk.Button(window, text=key, command=lambda key=key: key_press(None, key), width=7)
    btn.grid(row=0, column=keys.index(key))
btn1 = tk.Button(window, text=k[0], command=lambda key=k[0]: key_press(None, key), width=7)
btn1.grid(row=0, column=len(keys))
for key in keys1:
    btn1 = tk.Button(window, text=key, command=lambda key=key: key_press(None, key), width=7)
    btn1.grid(row=1, column=keys1.index(key))
btn2 = tk.Button(window, text=k1[0], command=lambda key=k1[0]: key_press(None, key), width=7)
btn2.grid(row=1, column=len(keys1))
for key in keys2:
    btn2 = tk.Button(window, text=key, command=lambda key=key: key_press(None, key), width=7)
    btn2.grid(row=2, column=keys2.index(key))
btn3 = tk.Button(window, text='Enter', command=lambda: key_press(None, 'Enter'), width=7)
btn3.grid(row=2, column=len(keys2))
for key in keys3:
    btn3 = tk.Button(window, text=key, command=lambda key=key: key_press(None, key), width=7)
    btn3.grid(row=3, column=keys3.index(key))
btn3 = tk.Button(window, text=k3[0], command=lambda key=k3[0]: key_press(None, key), width=7)
btn3.grid(row=3, column=len(keys3))
for key in keys4:
    btn4 = tk.Button(window, text=key, command=lambda key=key: key_press(None, key), width=7)
    btn4.grid(row=4, column=keys4.index(key))
window.bind('<KeyPress>', lambda event: key_press(event, event.keysym))
window.mainloop()
