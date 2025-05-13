import os
import tkinter as tk
from tkinter import PhotoImage, Canvas, Button, messagebox

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
gui_cache_dir = os.path.join(script_dir, "GUI_cache")
working_func_dir = os.path.join(script_dir, "Working_Func")

# Ensure GUI_cache directory exists
if not os.path.exists(gui_cache_dir):
    messagebox.showerror("Error", f"GUI_cache directory not found: {gui_cache_dir}")
    exit()

# Function to run external scripts
def run_script(script_name):
    script_path = os.path.join(working_func_dir, script_name)
    if os.path.exists(script_path):
        print(f"Running {script_name}...")
        os.system(f'"{sys.executable}" "{script_path}"')
    else:
        messagebox.showerror("Error", f"Script not found: {script_name}")

# Button commands
def speech():
    run_script("Jarvis.py")

def btn_mouse():
    run_script("Mouse_Control.py")

def btn_volume():
    run_script("Volume_Control.py")

# Function to load images safely
def load_image(filename):
    path = os.path.join(gui_cache_dir, filename)
    if not os.path.exists(path):
        messagebox.showerror("Error", f"Image not found: {filename}")
        return None
    try:
        return PhotoImage(file=path)
    except tk.TclError as e:
        messagebox.showerror("Error", f"Failed to load image: {filename}\n{e}")
        return None

# Initialize Window
window = tk.Tk()
window.geometry("450x400")
window.configure(bg="#ffffff")
window.title("Hand Gesture Controlling")
window.resizable(False, False)

# Create Canvas
canvas = Canvas(window, height=400, width=450, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

# Load and Display Images
background_img = load_image("background.png")
if background_img:
    canvas.create_image(225.0, 200.0, image=background_img)

img0 = load_image("img0.png")
if img0:
    b0 = Button(window, image=img0, borderwidth=0, highlightthickness=0, command=speech, relief="flat")
    b0.place(x=76, y=65, width=135, height=135)

img1 = load_image("img1.png")
if img1:
    b1 = Button(window, image=img1, borderwidth=0, highlightthickness=0, command=btn_volume, relief="flat")
    b1.place(x=238, y=65, width=135, height=135)

img2 = load_image("img2.png")
if img2:
    b2 = Button(window, image=img2, borderwidth=0, highlightthickness=0, command=btn_mouse, relief="flat")
    b2.place(x=76, y=227, width=135, height=135)

canvas.create_text(225.0, 47.5, text="Control it with just a Hand", fill="#001739", font=("BeVietnamPro-Bold", 24))

photo = load_image("img4.png")
if photo:
    canvas2 = Canvas(window, width=56, height=67, relief="ridge")
    canvas2.create_image(30, 37, image=photo, anchor=tk.CENTER)
    canvas2.place(x=194.2, y=179)

# Exit on Escape Key
window.bind('<Escape>', lambda e: window.destroy())

# Run the GUI
window.mainloop()
