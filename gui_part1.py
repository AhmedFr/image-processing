import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

class ImageDifferenceGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Difference Finder")

        # Initialize image paths
        self.image1_path = None
        self.image2_path = None

        # Create widgets
        self.label1 = tk.Label(master, text="Select Image 1:")
        self.label1.pack()

        self.button1 = tk.Button(master, text="Browse", command=self.browse_image1)
        self.button1.pack()

        self.label2 = tk.Label(master, text="Select Image 2:")
        self.label2.pack()

        self.button2 = tk.Button(master, text="Browse", command=self.browse_image2)
        self.button2.pack()

        self.run_button = tk.Button(master, text="Run", command=self.find_differences)
        self.run_button.pack()

        # Add labels to display the selected image names
        self.image1_label = tk.Label(master, text="")
        self.image1_label.pack()

        self.image2_label = tk.Label(master, text="")
        self.image2_label.pack()

        # Add a label to display the result image
        self.result_label = tk.Label(master)
        self.result_label.pack()

        # Initialize PhotoImage variables
        self.image1_tk = None
        self.image2_tk = None
        self.result_image_tk = None

        #display example image
        self.example_image = ImageTk.PhotoImage(Image.open("example_image.jpg"))
        self.example_image_label = tk.Label(master, image=self.example_image, bg="blue")
        self.example_image_label.pack()

    def browse_image1(self):
        file_path = filedialog.askopenfilename(title="Select Image 1", filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        self.image1_path = file_path
        self.label1.config(text="Selected Image 1: {}".format(file_path))
        # display the image
        image = Image.open(file_path)
        image.thumbnail((400, 400), Image.LANCZOS)
        self.image1_tk = ImageTk.PhotoImage(image)
        self.image1_label.config(image=self.image1_tk)
        self.image1_label.image = self.image1_tk

    def browse_image2(self):
        file_path = filedialog.askopenfilename(title="Select Image 2", filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        self.image2_path = file_path
        self.label2.config(text="Selected Image 2: {}".format(file_path))
        # display the image
        image = Image.open(file_path)
        image.thumbnail((400, 400), Image.LANCZOS)
        self.image2_tk = ImageTk.PhotoImage(image)
        self.image2_label.config(image=self.image2_tk)
        self.image2_label.image = self.image2_tk

    def find_differences(self):
        if self.image1_path is None or self.image2_path is None:
            messagebox.showerror("Error", "Please select both images before running.")
            return

        try:
            output_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            self._find_differences(self.image1_path, self.image2_path, output_path)
            messagebox.showinfo("Success", "Differences found and saved successfully!")
            # Display the result image
            result_image = Image.open(output_path)
            result_image.thumbnail((400, 400), Image.LANCZOS)
            self.result_image_tk = ImageTk.PhotoImage(result_image)
            self.result_label.config(image=self.result_image_tk)
            self.result_label.image = self.result_image_tk
        except Exception as e:
            messagebox.showerror("Error: An error occurred:", str(e))

    @staticmethod
    def _find_differences(image1_path, image2_path, output_path):
        # The code for finding differences (same as before)
        img1 = cv2.imread(image1_path)
        img2 = cv2.imread(image2_path)

        # Ensure images have the same dimensions
        if img1.shape != img2.shape:
            raise ValueError("Images must have the same dimensions")

        # Find absolute difference between the two images
        diff = cv2.absdiff(img1, img2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # Threshold the difference image
        _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw rectangles around the differing regions
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Save the output image
        cv2.imwrite(output_path, img1)

# Create the Tkinter window
root = tk.Tk()

# Create an instance of the GUI class
app = ImageDifferenceGUI(root)

# Run the Tkinter event loop
root.mainloop()
