import cv2
import numpy as np
from itertools import permutations

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def create_white_circle(image_size, center, radius, intensity):
    image = np.zeros(image_size, dtype=np.uint8)
    color = int(intensity * 255)
    cv2.circle(image, center, radius, (color, color, color), -1)
    return image

def find_red_block_vertices(image_path):
    image = cv2.imread(image_path)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    vertex = Vertex(0, 0)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)

        if len(approx) == 4:
            vertices = [Vertex(point[0], point[1]) for point in approx.reshape(-1, 2)]

            vertex.A, vertex.B, vertex.C, vertex.D = vertices

            return image, vertex

    return None, None

def find_largest_ratio(vertices, light_source_x, light_source_y):
    max_ratio = 0
    max_ratio_vertices = None

    for perm in permutations(['A', 'B', 'C', 'D']):
        ratio = abs(
            (getattr(vertices, perm[2]).x - light_source_x) / (getattr(vertices, perm[2]).y - light_source_y) -
            (getattr(vertices, perm[0]).x - light_source_x) / (getattr(vertices, perm[0]).y - light_source_y)
        )

        if ratio > max_ratio:
            max_ratio = ratio
            max_ratio_vertices = (perm[0], perm[2])

    return max_ratio, max_ratio_vertices

def draw_line(image, vertex, vertices):
    point1 = (getattr(vertex, vertices[0]).x, getattr(vertex, vertices[0]).y)
    point2 = (getattr(vertex, vertices[1]).x, getattr(vertex, vertices[1]).y)
    color = (255, 0, 0)  # Blue color
    thickness = 2
    cv2.line(image, point1, point2, color, thickness)

def draw_white_circle(image, center, radius, intensity):
    white_circle = create_white_circle(image.shape, center, radius, intensity)
    image_with_circle = cv2.addWeighted(image, 1, white_circle, 0.7, 0)
    return image_with_circle

# Example usage
image_path = '1.png'
image, vertex = find_red_block_vertices(image_path)

light_source_x = 64
light_source_y = 1

if image is not None and vertex is not None:
    print("Vertices of the red block:")
    print("A.x:", vertex.A.x, "A.y:", vertex.A.y)
    print("B.x:", vertex.B.x, "B.y:", vertex.B.y)
    print("C.x:", vertex.C.x, "C.y:", vertex.C.y)
    print("D.x:", vertex.D.x, "D.y:", vertex.D.y)

    max_ratio, max_ratio_vertices = find_largest_ratio(vertex, light_source_x, light_source_y)
    print("Largest Ratio:", max_ratio)
    print(f"Vertices corresponding to the largest ratio: {max_ratio_vertices[0]} and {max_ratio_vertices[1]}")

    # Create a copy of the image to draw the line on
    image_with_line = image.copy()
    draw_line(image_with_line, vertex, max_ratio_vertices)

    # Draw white circles with increasing radius and decreasing intensity
    circle_radius = 20
    max_intensity = 1.0

    while max_intensity >= 0:
        intensity = max_intensity
        image_with_circles = draw_white_circle(image_with_line, (light_source_x, light_source_y), circle_radius, intensity)
        cv2.imshow('Image with Line and Circles', image_with_circles)
        cv2.waitKey(500)  # Add a delay to observe the circles
        max_intensity -= 0.1
        circle_radius += 10

    cv2.destroyAllWindows()

else:
    print("No red block found in the image.")

