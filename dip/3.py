import cv2
import numpy as np

def find_red_block_vertices(image_path):
    image = cv2.imread(image_path)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        
        if len(approx) == 4:
            return approx.reshape(-1, 2)

    return None

image_path = '1.png'
vertices = find_red_block_vertices(image_path)

if vertices is not None:
    print("Vertices of the red block: \n", vertices)
else:
    print("No red block found in the image.")

