import cv2
import numpy as np

def find_red_block_vertices(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the red color in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Threshold the image to get only red regions
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through the contours to find the rectangle around the red block
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        
        # If the contour has 4 vertices, it is likely a rectangle (assuming the red block is rectangular)
        if len(approx) == 4:
            return approx.reshape(-1, 2)  # Reshape to get the vertices as (x, y)

    return None  # Return None if no red block is found

def calculate_distances(vertices, point_A):
    distances = np.sqrt(np.sum((vertices - point_A)**2, axis=1))
    return distances

def calculate_angles(vertices, point_O):
    angles = []
    for i in range(len(vertices)):
        v1 = vertices[i] - point_O
        v2 = vertices[(i + 1) % len(vertices)] - point_O
        dot_product = np.dot(v1, v2)
        magnitude_product = np.linalg.norm(v1) * np.linalg.norm(v2)
        angle = np.arccos(dot_product / magnitude_product)
        angles.append(np.degrees(angle))
    return angles

# Example usage
image_path = '1.png'  # Replace with the actual path to your image
point_O = np.array([0, 0])  # Coordinates of point O

vertices = find_red_block_vertices(image_path)

if vertices is not None:
    print("Vertices of the red block:", vertices)

    distances = calculate_distances(vertices, point_O)
    print("Distances from point O:", distances)

    angles = calculate_angles(vertices, point_O)
    print("Angles:", angles)

    largest_angle_index = np.argmax(angles)
    largest_angle = angles[largest_angle_index]
    print("Largest angle:", largest_angle, "degrees")
else:
    print("No red block found in the image.")

