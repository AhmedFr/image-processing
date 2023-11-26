# GUI for Part 2: Finding a Given Object Within an Image

import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

class ObjectDetectionGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Object Detection")

        # Create widgets
        self.label1 = tk.Label(master, text="Select Object Image:")
        self.label1.pack()

        self.button1 = tk.Button(master, text="Browse", command=self.browse_object_image)
        self.button1.pack()

        self.label2 = tk.Label(master, text="Select Scene Image:")
        self.label2.pack()

        self.button2 = tk.Button(master, text="Browse", command=self.browse_scene_image)
        self.button2.pack()

        self.run_button = tk.Button(master, text="Run", command=self.find_object)
        self.run_button.pack()

    def browse_object_image(self):
        file_path = filedialog.askopenfilename(title="Select Object Image", filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        self.object_image_path = file_path
        self.label1.config(text="Selected Object Image:")

    def browse_scene_image(self):
        file_path = filedialog.askopenfilename(title="Select Scene Image", filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        self.scene_image_path = file_path
        self.label2.config(text="Selected Scene Image:")

    def find_object(self):
        try:
            output_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            find_object(self.object_image_path, self.scene_image_path, output_path)
            tk.messagebox.showinfo("Success", "Object found and matches highlighted successfully!")
        except Exception as e:
            tk.messagebox.showerror("Error An error occurred: ", str(e))

def find_object(object_image_path, scene_image_path, output_path):
    # Load images
    object_image = cv2.imread(object_image_path)
    scene_image = cv2.imread(scene_image_path)

    # Convert images to grayscale
    object_gray = cv2.cvtColor(object_image, cv2.COLOR_BGR2GRAY)
    scene_gray = cv2.cvtColor(scene_image, cv2.COLOR_BGR2GRAY)

    # Use ORB (Oriented FAST and Rotated BRIEF) to detect keypoints and descriptors
    orb = cv2.ORB_create()
    keypoints1, descriptors1 = orb.detectAndCompute(object_gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(scene_gray, None)

    # Use BFMatcher to find the best matches between descriptors
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)

    # Sort the matches based on their distances
    matches = sorted(matches, key=lambda x: x.distance)

    # Draw the matches on the images
    img_matches = cv2.drawMatches(object_image, keypoints1, scene_image, keypoints2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # Save the output image
    cv2.imwrite(output_path, img_matches)

# Create the Tkinter window
root = tk.Tk()

# Create an instance of the GUI class
app = ObjectDetectionGUI(root)

# Run the Tkinter event loop
root.mainloop()
