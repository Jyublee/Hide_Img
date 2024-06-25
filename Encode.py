import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

def encode_message(image_path, message):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("The image could not be loaded.")
    
    message_bits = ''.join([format(ord(char), '08b') for char in message])
    message_length = len(message_bits)
    length_bits = format(len(message), '016b')  # 16 bits for message length

    max_capacity = image.size * 3
    if (len(length_bits) + message_length) > max_capacity:
        raise ValueError("Message is too long to be encoded in the given image.")
    
    combined_bits = length_bits + message_bits

    flat_image = image.flatten()
    
    for i in range(len(combined_bits)):
        flat_image[i] = (flat_image[i] & ~1) | int(combined_bits[i])
    
    encoded_image = flat_image.reshape(image.shape)
    return encoded_image

def save_encoded_image(image):
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        cv2.imwrite(save_path, image)
        messagebox.showinfo("Success", f"Image saved successfully at {save_path}")

def encode_button_click():
    if not image_path:
        messagebox.showerror("Error", "Please select an image first.")
        return
    
    message = message_entry.get("1.0", tk.END).strip()
    if not message:
        messagebox.showerror("Error", "Please enter a message to encode.")
        return
    
    try:
        encoded_image = encode_message(image_path, message)
        save_encoded_image(encoded_image)
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
app.title("Steganographic Encoder")

# Calculate center position of the screen
window_width = 500
window_height = 600
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)
app.geometry(f"{window_width}x{window_height}+{x}+{y}")

frame = ttk.Frame(app, padding="10")
frame.pack(expand=True, fill=tk.BOTH)

image_label = ttk.Label(frame)
image_label.pack(pady=10)

select_button = ttk.Button(frame, text="Select Image", command=select_image)
select_button.pack(side=tk.LEFT, padx=10, pady=10)

confirm_button = ttk.Button(frame, text="Confirm and Encode", command=encode_button_click)
confirm_button.pack(side=tk.RIGHT, padx=10, pady=10)

message_label = ttk.Label(frame, text="Enter the message to encode:")
message_label.pack(pady=5)

message_entry = tk.Text(frame, height=5, width=50)  # Reduced the height of the text box
message_entry.pack(pady=5)

app.mainloop()
