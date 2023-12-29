import cv2
import numpy as np
from itertools import permutations

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

            return vertex

    return None

def calculate_unique_ratios(vertices):
    unique_ratios = set()
    for perm in permutations(['A', 'B', 'C', 'D']):
        ratio = abs(getattr(getattr(vertices, perm[2]), 'x') / getattr(getattr(vertices, perm[2]), 'y') - getattr(getattr(vertices, perm[0]), 'x') / getattr(getattr(vertices, perm[0]), 'y'))
        unique_ratios.add(ratio)
    return unique_ratios

# Example usage
image_path = '1.png'
vertex = find_red_block_vertices(image_path)

if vertex is not None:
    print("Vertices of the red block:")
    print("A.x:", vertex.A.x, "A.y:", vertex.A.y)
    print("B.x:", vertex.B.x, "B.y:", vertex.B.y)
    print("C.x:", vertex.C.x, "C.y:", vertex.C.y)
    print("D.x:", vertex.D.x, "D.y:", vertex.D.y)

    unique_ratios = calculate_unique_ratios(vertex)
    print("Unique Ratios:")
    for i, ratio in enumerate(unique_ratios):
        print(f"Ratio {i+1}: {ratio}")

else:
    print("No red block found in the image.")

