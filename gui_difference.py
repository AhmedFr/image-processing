import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

# Constants for grayscale conversion
RED_WEIGHT = 0.299
GREEN_WEIGHT = 0.587
BLUE_WEIGHT = 0.114
THRESHOLD = 40
MAX_COLOR_VALUE = 255

def split_channels(image):
    if len(image.shape) == 3:
        channels = np.dsplit(image, image.shape[2]) # Splits the image into its BGR components, each channel is a 2D array representing the intensity of that color
        return channels
    else:
        raise ValueError("Input image must be multi-channel (BGR or RGB)")
      
def absdiff(image1, image2):
    if image1.shape != image2.shape:
        raise ValueError("Input images must have the same shape")
    diff = np.abs(image1 - image2)
    return diff

def convert_to_grayscale(image):
    b, g, r = split_channels(image)
    gray = RED_WEIGHT * r + GREEN_WEIGHT * g + BLUE_WEIGHT * b
    return gray.astype(np.uint8)
  
def binary_threshold(image):
    # buffer
    thresholded_image = np.zeros(image.shape, dtype=np.uint8)

    rows = image.shape[0]
    cols = image.shape[1]
    for i in range(rows):
        for j in range(cols):
            if image[i, j] > THRESHOLD:
                thresholded_image[i, j] = 1
            else:
                thresholded_image[i, j] = 0

    return thresholded_image
  
def get_rect_infos(contour):
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')

    # Find the minimum and maximum x and y coordinates
    for point in contour:
        x, y = point[0], point[1]  # Fix here
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    width = max_x - min_x
    height = max_y - min_y
    return min_x, min_y, width, height
  
def find_contours(thresh):
    contours = []

    rows = thresh.shape[0]
    cols = thresh.shape[1]
    visited = np.zeros((rows, cols), dtype=np.uint8)

    for i in range(rows):
        for j in range(cols):
            if thresh[i, j] > 0 and visited[i, j] == 0:
                contour = []
                stack = [(i, j)]

                while stack:
                    current_i, current_j = stack.pop()
                    visited[current_i, current_j] = 1
                    contour.append((current_j, current_i))

                    neighbors = [(current_i + 1, current_j),
                                 (current_i - 1, current_j),
                                 (current_i, current_j + 1),
                                 (current_i, current_j - 1)]

                    for neighbor_i, neighbor_j in neighbors:
                        if 0 <= neighbor_i < rows and 0 <= neighbor_j < cols and thresh[neighbor_i, neighbor_j] > 0 and visited[neighbor_i, neighbor_j] == 0:
                            stack.append((neighbor_i, neighbor_j))

                contours.append(np.array(contour))

    return contours
  
def draw_rectangle(image, top_left, bottom_right, color=(0, 255, 0), thickness=2):
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))
    b, g, r = color
    for x in range(top_left[0], bottom_right[0] + 1):
        for t in range(thickness):
            image[top_left[1] + t, x] = [b, g, r]
            image[bottom_right[1] - t, x] = [b, g, r]
    for y in range(top_left[1], bottom_right[1] + 1):
        for t in range(thickness):
            image[y, top_left[0] + t] = [b, g, r]
            image[y, bottom_right[0] - t] = [b, g, r]


class ImageDifferenceGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Difference Finder")
        self.master.geometry("1400x1000")

        # Initialize image paths
        self.image1_path = None
        self.image2_path = None

        # Create description label
        description = "This program allows you to select two images and find the differences between them."
        self.description_label = tk.Label(master, text=description)
        self.description_label.pack()

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
        print("Finding differences...")
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
            print('error line', e)
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
        diff = absdiff(img1, img2)
        gray = convert_to_grayscale(diff)

        # Threshold the difference image
        thresh = binary_threshold(gray)

        # Find contours in the thresholded image
        contours = find_contours(thresh)

        # Draw rectangles around the differing regions
        for i in range(len(contours)):
            print("Processing contour:", i)
            x, y, w, h = get_rect_infos(contours[i])
            draw_rectangle(img1, (x, y), (x + w, y + h), color=(0, 0, 255))

        # Save the output image
        cv2.imwrite(output_path, img1)

# Create the Tkinter window
root = tk.Tk()

# Create an instance of the GUI class
app = ImageDifferenceGUI(root)

# Run the Tkinter event loop
root.mainloop()