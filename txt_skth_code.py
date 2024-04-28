import tkinter as tk 
import customtkinter as ctk 
from PIL import Image, ImageTk
from customtkinter import filedialog
import cv2
import numpy as np

def get_brightness_value(value):
    brightness_label.configure(text=f"{int(value)}")

def get_thickness_value(value):
    thickness_label.configure(text=f"{int(value)}")

def get_contrast_value(value):
    contrast_label.configure(text=f"{int(value)}")

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        # Load the image and display it using CTkImage
        load_image(file_path)

def load_image(file_path):
    global ctk_img, original_image
    original_image = Image.open(file_path)
    original_image.thumbnail((210, 210))  # Resize image to fit in the label
    ctk_img = ctk.CTkImage(light_image=original_image, dark_image=original_image, size=(210, 210))
    upimgbox.configure(image=ctk_img)
    upimgbox.image = ctk_img

def convert_to_sketch():
    global original_image
    if original_image:
        # Convert the image to a sketch
        img_array = np.array(original_image)
        gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        inverted_gray_img = 255 - gray_img
        blurred_img = cv2.GaussianBlur(inverted_gray_img, (21, 21), 0)
        inverted_blurred_img = 255 - blurred_img
        sketch_img = cv2.divide(gray_img, inverted_blurred_img, scale=256.0)
        sketch_img = Image.fromarray(sketch_img)

        # Display the sketch image
        ctk_sketch_img = ctk.CTkImage(light_image=sketch_img, dark_image=sketch_img, size=(210, 210))
        preimgbox.configure(image=ctk_sketch_img)
        preimgbox.image = ctk_sketch_img
    else:
        print("No image uploaded")

ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.geometry("700x700")
root.title("Image to Sketch Application")
frame = ctk.CTkFrame(master=root, width=610, height=500, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

prelab = ctk.CTkLabel(master=frame, text="Preview Image", fg_color="transparent", text_color="grey")
prelab.place(x=320, y=30)
uplab = ctk.CTkLabel(master=frame, text="Uploaded Image", fg_color="transparent", text_color="grey")
uplab.place(x=20, y=30)

headlabel = ctk.CTkLabel(master=frame, text="Image to Sketch", font=("Century Gothic", 25), text_color="gray")
headlabel.place(relx=0.5, y=15, anchor="center")

upframe = ctk.CTkFrame(master=frame, width=290, height=270, corner_radius=15)
upframe.place(x=10, y=60)
preframe = ctk.CTkFrame(master=frame, width=290, height=270, corner_radius=15)
preframe.place(x=310, y=60)

upimgbox = ctk.CTkLabel(master=upframe, text="", width=275, height=255, corner_radius=15)
upimgbox.place(x=5, y=5)
preimgbox = ctk.CTkLabel(master=preframe, text="", width=275, height=255, corner_radius=15)
preimgbox.place(x=5, y=5)

# Slider labels
bri_sli_lab = ctk.CTkLabel(master=frame, text="Brightness", text_color="grey")
bri_sli_lab.place(x=10, y=335)
thik_sli_lab = ctk.CTkLabel(master=frame, text="Line Thickness", text_color="grey")
thik_sli_lab.place(x=210, y=335)
cnst_sli_lab = ctk.CTkLabel(master=frame, text="Contrast", text_color="grey")
cnst_sli_lab.place(x=410, y=335)

# Create labels to display selected values
brightness_label = ctk.CTkLabel(frame, text="0", text_color="grey")
brightness_label.place(x=180, y=335)
thickness_label = ctk.CTkLabel(frame, text="0", text_color="grey")
thickness_label.place(x=380, y=335)
contrast_label = ctk.CTkLabel(frame, text="0", text_color="grey")
contrast_label.place(x=580, y=335)

brt_slid = ctk.CTkSlider(frame, from_=-100, to=100, number_of_steps=100, command=get_brightness_value, button_color="grey")
brt_slid.place(x=5, y=360)
thik_slid = ctk.CTkSlider(frame, from_=0, to=100, number_of_steps=200, command=get_thickness_value, button_color="grey")
thik_slid.place(x=205, y=360)
cnst_slid = ctk.CTkSlider(frame, from_=0, to=100, number_of_steps=100, command=get_contrast_value, button_color="grey")
cnst_slid.place(x=405, y=360)

# Create buttons
upload_button = ctk.CTkButton(frame, text='Upload', width=180, height=28, fg_color="grey", command=upload_image)
upload_button.place(x=10, y=400)
convert_button = ctk.CTkButton(frame, text='Convert', width=180, height=28, fg_color="grey", command=convert_to_sketch)
convert_button.place(x=210, y=400)
preview_button = ctk.CTkButton(frame, text='Preview', width=180, height=28, fg_color="grey")
preview_button.place(x=410, y=400)
save_button = ctk.CTkButton(frame, text='Save', width=180, height=35, fg_color="grey")
save_button.place(x=210, y=450)

root.mainloop()
