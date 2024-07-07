from cv2_enumerate_cameras import enumerate_cameras
import cv2
import tkinter as tk
from PIL import ImageTk, Image
from run import*

selected_camera = 0
flip_horizontally = False
flip_vertically = False
rotate_camera = 0
turn=0

def change_camera(x):
    global selected_camera, rotate_camera
    rotate_camera=0
    selected_camera = camera_indices[x]
    global cap
    cap.release()
    cap = cv2.VideoCapture(camera_indices[x])

def flip_horizontally_toggle():
    global flip_horizontally
    flip_horizontally = not flip_horizontally

def flip_vertically_toggle():
    global flip_vertically
    flip_vertically = not flip_vertically
 
def save_settings():
    with open('settings.txt', 'a') as f:
        f.write(f'Pause:\n{scale1.get()/100}\n')
        f.write(f'Speed:\n{scale.get()}\n')
        f.write(f'Camera:\n{selected_camera}\n')
        f.write(f'autorun:\n{flag_var.get()}\n')
        f.write(f'autorun key:\n{flag_var1.get()}\n')
        f.write(f'horizontally:\n{int(flip_horizontally)}\n')
        f.write(f'vertically:\n{int(flip_vertically)}\n')
        f.write(f'turn:\n{rotate_camera}\n')
        f.write(f'close:\n{flag_var2.get()}\n')
        f.write(f'camere to keyboard:\n{flag_var3.get()}\n')
        root.quit()
        cap.release()
        cv2.destroyAllWindows()
        exit

def openkey():
    run_key()

def rotate_camera_90():
    global rotate_camera
    rotate_camera = (rotate_camera + 90) % 360
    ret, frame = cap.read()
    w, h = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    if rotate_camera == 90:
        center_x = w // 2
        center_y = h // 2
        frame = cv2.resize(frame, (h, w), cv2.INTER_AREA)
    elif rotate_camera == 180:
        center_x = w // 2
        center_y = h // 2
    elif rotate_camera == 270:
        center_x = 240
        center_y = 0
        frame = cv2.resize(frame, (h, w), cv2.INTER_AREA)
    else:
        center_x = w // 2
        center_y = h // 2
    M = cv2.getRotationMatrix2D((center_x, center_y), rotate_camera, 1)

    frame = cv2.warpAffine(frame, M, (w, h))

def update_frame():
    ret, frame = cap.read()
    if ret:
        if flip_horizontally:
            frame = cv2.flip(frame, 1)
        if flip_vertically:
            frame = cv2.flip(frame, 0)
        if rotate_camera != 0:
            w, h = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            if rotate_camera == 90:
                center_x = 240
                center_y = 240
                frame = cv2.resize(frame, (h, w), cv2.INTER_AREA)
            elif rotate_camera == 180:
                center_x = w // 2
                center_y = h // 2
            elif rotate_camera == 270:
                center_x = 320
                center_y = 320
                frame = cv2.resize(frame, (h, w), cv2.INTER_AREA)
            else:
                center_x = w // 2
                center_y = h // 2
            M = cv2.getRotationMatrix2D((center_x, center_y), rotate_camera, 1)
            frame = cv2.warpAffine(frame, M, (w, h))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)
        canvas.itemconfig(image_holder, image=photo)
        canvas.image = photo
    root.after(15, update_frame)

root = tk.Tk()
camn=[]
for camera_info in enumerate_cameras(cv2.CAP_MSMF):
    camn.append(camera_info.index)
 
root.title("Camera and Settings")
camera_indices = list(camn)

camera_var = tk.StringVar(root)
camera_var.set(camera_indices[0])

text = tk.Label(root, text='Настройки')
text.pack(side='top')

camera_label = tk.Label(root, text="Выберите камеру для мыши:")
camera_label.pack(side='top')

camera_menu = tk.OptionMenu(root, camera_var, *camera_indices, command=change_camera)
camera_menu.pack(side='top')

canvas = tk.Canvas(root, width=640, height=480)
canvas.pack(side='left')

flag_var = tk.IntVar()
flag_var1 = tk.IntVar()
flag_var2 = tk.IntVar()
flag_var3 = tk.IntVar()

flag_checkbox = tk.Checkbutton(root, text="Автозапуск", variable=flag_var)
flag_checkbox.pack(side='top')

flag_checkbox1 = tk.Checkbutton(root, text="Запуск экранной клавиатуры", variable=flag_var1)
flag_checkbox1.pack(side='top')

button_frame1 = tk.Frame(root)
button_frame1.pack()
save_button = tk.Button(button_frame1, text="посмотреть клавиатуру", command=openkey)
save_button.pack(side='bottom')

close_checkbox = tk.Checkbutton(root, text="Закрывание окна", variable=flag_var2)
close_checkbox.pack(side='top')

button_frame = tk.Frame(root)
button_frame.pack(side='bottom')

save_button = tk.Button(button_frame, text="Сохранить", command=save_settings)
save_button.pack(side='bottom')

flip_horizontally_button = tk.Button(button_frame, text="Отразить горизонтально", command=flip_horizontally_toggle)
flip_horizontally_button.pack(side='left')

flip_vertically_button = tk.Button(button_frame, text="Отразить вертикально", command=flip_vertically_toggle)
flip_vertically_button.pack(side='left')

rotate_camera_button = tk.Button(button_frame, text="Повернуть камеру", command=rotate_camera_90)
rotate_camera_button.pack(side='left')

scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
scale.pack(side='bottom')

tl = tk.Label(root, text="Шаг перемещения:")
tl.pack(side='bottom')

scale1 = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
scale1.pack(side='bottom')

tl = tk.Label(root, text="Задержка:")
tl.pack(side='bottom')

camkey_checkbox = tk.Checkbutton(root, text="Использовать камеру для печатанья", variable=flag_var3)
camkey_checkbox.pack(side='top')

cap = None
for idx, camera_idx in enumerate(camera_indices):
    cap = cv2.VideoCapture(camera_idx)
    if cap.isOpened():
        break

image = Image.new("RGB", (640, 480))
photo = ImageTk.PhotoImage(image=image)
image_holder = canvas.create_image(0, 0, anchor=tk.NW, image=photo)

update_frame()

root.mainloop()
