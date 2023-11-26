# Part 1: Finding Differences Between Two Images

import cv2
import numpy as np

def find_differences(image1_path, image2_path, output_path):
    # Load images
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

# Example usage
find_differences("image1.jpg", "image2.jpg", "output_diff.jpg")
