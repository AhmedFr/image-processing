# Image Processing GUI Applications
### Team 17 project, Chung Ang University 2023

This repository contains two Python applications built using Tkinter for image processing tasks.

## Part 1: Image Difference Finder (gui_difference.py)

### Overview
The Image Difference Finder is a Tkinter-based application that allows users to compare two images and visualize the differences between them. The program loads two images, highlights the varying regions, and generates an output image displaying the identified distinctions.

### Features
1. **Image Selection:** Users can select two images for comparison.
2. **Visualization:** The program visually represents the differences between the selected images by drawing rectangles around varying regions.
3. **Result Display:** The output image, showing the highlighted differences, is displayed in the application.
4. **Modern Interface:** The application uses themed Tkinter widgets (`ttk`) to provide a more modern and aesthetically pleasing appearance.

### How to Use
1. **Select Images:**
   - Click the "Browse" button for Image 1 to choose the first image.
   - Click the "Browse" button for Image 2 to select the second image.

2. **Run Comparison:**
   - Click the "Run" button to initiate the comparison process.

3. **View Results:**
   - The program will highlight differences in the output image.
   - The result image will be displayed in the application.

## Part 2: Object Detection (gui_object.py)

### Overview
The Object Detection application is designed for locating a given object within a scene image. Users can select an object image and a scene image, and the program uses the ORB (Oriented FAST and Rotated BRIEF) algorithm to detect keypoints and descriptors, finding matches between the two images.

### Features
1. **Object Image Selection:** Users can select an object image for detection.
2. **Scene Image Selection:** Users can choose a scene image where the object will be detected.
3. **Run Detection:** Clicking the "Run" button initiates the detection process, highlighting the matched keypoints in the scene image.
4. **Output Display:** The program shows the scene image with highlighted matches.

### How to Use
1. **Select Object Image:**
   - Click the "Browse" button to choose the object image.

2. **Select Scene Image:**
   - Click the "Browse" button to select the scene image where the object will be detected.

3. **Run Detection:**
   - Click the "Run" button to initiate the detection process.

4. **View Results:**
   - The program will highlight matching keypoints in the scene image.
   - The result image will be displayed in the application.

## Prerequisites
- Python 3.x
- Required Python libraries: `cv2`, `PIL`, `numpy`

## Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:AhmedFr/image-processing.git
   cd image-processing
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the desired application:
   ```bash
   python gui_difference.py  # For Image Difference Finder
   python gui_object.py  # For Object Detection
   ```

## Author
Ahmed Abouelleil