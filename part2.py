# Part 2: Finding a Given Object Within an Image

import cv2
import numpy as np

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

# Example usage
find_object("object.jpg", "scene.jpg", "output_object_detection.jpg")
