import cv2
import tkinter as tk
from PIL import ImageTk, Image
import subprocess
selected_camera = 0  # Первая доступная камера

def change_camera(x):
    global selected_camera
    selected_camera = camera_indices[x]
    global cap
    cap.release()
    cap = cv2.VideoCapture(camera_indices[x])

def save_settings():
    with open('settings.txt', 'a') as f:
        f.write(f'Pause:\n{scale1.get()/100}\n')
        f.write(f'Speed:\n{scale.get()}\n')
        f.write(f'Camera:\n{selected_camera}\n')
        f.write(f'autorun:\n{flag_var.get()}\n')
        f.write(f'autorun key:\n{flag_var1.get()}\n')
        root.quit()
        cap.release()
        cv2.destroyAllWindows()
        subprocess.Popen(['python','setting mouse.py'])
        exit

def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)
        canvas.itemconfig(image_holder, image=photo)
        canvas.image = photo
    root.after(15, update_frame)

root = tk.Tk()
root.title("Camera and Settings")
root.iconbitmap(default='camera.ico')
# Get list of available camera indices
camera_indices = list(range(10))

# Create dropdown menu
camera_var = tk.StringVar(root)
camera_var.set(camera_indices[0])

text=tk.Label(root,text='Настройки')
text.pack()

camera_label = tk.Label(root, text="Выберите камеру:")
camera_label.pack()

camera_menu = tk.OptionMenu(root, camera_var, *camera_indices, command=change_camera)
camera_menu.pack()

# Create canvas for camera frame
canvas = tk.Canvas(root, width=640, height=480)
canvas.pack(side='top')

# Создание флажка
flag_var = tk.IntVar()
flag_var1 = tk.IntVar()

flag_checkbox = tk.Checkbutton(root, text="Автозапуск", variable=flag_var)
flag_checkbox.pack(side='top')

flag_checkbox1 = tk.Checkbutton(root, text="Запуск экранной клавиатуры", variable=flag_var1)
flag_checkbox1.pack(side='top')

# Create buttons frame
button_frame = tk.Frame(root)
button_frame.pack(side='bottom')

# Create button to save settings
save_button = tk.Button(button_frame, text="Сохранить", command=save_settings)
save_button.pack(side='bottom')

scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
scale.pack(side='bottom')

tl=tk.Label(root,text="Шаг перемещения:")
tl.pack(side='bottom')

scale1 = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
scale1.pack(side='bottom')

tl=tk.Label(root,text="Задержка:")
tl.pack(side='bottom')

# Open first available camera by default
cap = None
for idx, camera_idx in enumerate(camera_indices):
    cap = cv2.VideoCapture(camera_idx)
    if cap.isOpened():
        break

# Check if camera is found
if cap is None or not cap.isOpened():
    print('No cameras found.')
    exit()

# Create image holder in canvas
image = Image.new("RGB", (640, 480))
photo = ImageTk.PhotoImage(image=image)
image_holder = canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# Start camera frame update
update_frame()

# Run Tkinter main loop
root.mainloop()








