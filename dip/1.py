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

def calculate_distances(vertices, point_A):
    distances = np.sqrt(np.sum((vertices - point_A)**2, axis=1))
    return distances

image_path = '1.png'  
point_A = np.array([1, 1])

vertices = find_red_block_vertices(image_path)

if vertices is not None:
    print("Vertices of the red block: \n", vertices)

    distances = calculate_distances(vertices, point_A)
    print("Distances from point A:", distances)
else:
    print("Still working on all color images")

