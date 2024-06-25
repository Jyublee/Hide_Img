import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

def decode_message(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("The image could not be loaded.")
    
    flat_image = image.flatten()
    
    message_bits = []
    for pixel in flat_image:
        message_bits.append(pixel & 1)
    
    length_bits = message_bits[:16]
    length_str = ''.join(map(str, length_bits))
    message_length = int(length_str, 2) * 8
    
    message_bits = message_bits[16:16+message_length]
    
    message_bytes = []
    for i in range(0, len(message_bits), 8):
        byte = message_bits[i:i+8]
        if len(byte) == 8:
            byte_str = ''.join(map(str, byte))
            message_bytes.append(chr(int(byte_str, 2)))
    
    decoded_message = ''.join(message_bytes)
    return decoded_message

def decode_button_click():
    if not image_path:
        messagebox.showerror("Error", "Please select an image first.")
        return
    
    try:
        decoded_message = decode_message(image_path)
        messagebox.showinfo("Decoded Message", decoded_message)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def select_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    if image_path:
        image = Image.open(image_path)
        image.thumbnail((400, 400))  # Resize the image to fit in the UI
        image_tk = ImageTk.PhotoImage(image)
        
        image_label.configure(image=image_tk)
        image_label.image = image_tk

app = tk.Tk()
app.title("Steganographic Decoder")
app.geometry("500x600")  # Set default size for the window

frame = ttk.Frame(app, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

image_label = ttk.Label(frame)
image_label.grid(row=0, column=0, columnspan=2)

select_button = ttk.Button(frame, text="Select Image", command=select_image)
select_button.grid(row=1, column=0, pady=10)

decode_button = ttk.Button(frame, text="Decode Message", command=decode_button_click)
decode_button.grid(row=1, column=1, pady=10)

app.mainloop()
