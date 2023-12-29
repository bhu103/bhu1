import cv2
import numpy as np
from itertools import permutations

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class VertexPair:
    def __init__(self, vertex1, vertex2):
        self.vertex1 = vertex1
        self.vertex2 = vertex2

def create_white_circle(image_size, center, radius, intensity):
    image = np.zeros(image_size, dtype=np.uint8)
    color = int(intensity * 255)

    # Convert center to a tuple of integers
    center = (int(center[0]), int(center[1]))

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
            max_ratio_vertices = VertexPair(getattr(vertices, perm[0]), getattr(vertices, perm[2]))

    return max_ratio, max_ratio_vertices

def draw_line(image, vertex, vertices):
    point1 = (max_ratio_vertices.vertex1.x, max_ratio_vertices.vertex1.y)
    point2 = (max_ratio_vertices.vertex2.x, max_ratio_vertices.vertex2.y)
    color = (255, 0, 0)  # Blue color
    thickness = 2
    cv2.line(image, point1, point2, color, thickness)

def draw_white_circle(image, center, radius, intensity):
    white_circle = create_white_circle(image.shape, center, radius, intensity)
    image_with_circle = cv2.addWeighted(image, 1, white_circle, 0.7, 0)
    return image_with_circle

image_path = '1.png'
image, vertex = find_red_block_vertices(image_path)

vertex_o_x = float(input("Enter x position of vertex O: "))
vertex_o_y = float(input("Enter y position of vertex O: "))

if image is not None and vertex is not None:
    print("Vertices of the red block:")
    print("A.x:", vertex.A.x, "A.y:", vertex.A.y)
    print("B.x:", vertex.B.x, "B.y:", vertex.B.y)
    print("C.x:", vertex.C.x, "C.y:", vertex.C.y)
    print("D.x:", vertex.D.x, "D.y:", vertex.D.y)

    max_ratio, max_ratio_vertices = find_largest_ratio(vertex, vertex_o_x, vertex_o_y)
    print("Largest Ratio:", max_ratio)
    print(f"Vertices corresponding to the largest ratio: {max_ratio_vertices.vertex1.x},{max_ratio_vertices.vertex1.y} and {max_ratio_vertices.vertex2.x},{max_ratio_vertices.vertex2.y}")

    image_with_line = image.copy()
    draw_line(image_with_line, vertex, max_ratio_vertices)

    # Extend line from O towards the first vertex
    extended_point1 = (int(vertex_o_x) + 1000 * (int(max_ratio_vertices.vertex1.x) - int(vertex_o_x)),
                       int(vertex_o_y) + 1000 * (int(max_ratio_vertices.vertex1.y) - int(vertex_o_y)))
    cv2.line(image_with_line, (int(vertex_o_x), int(vertex_o_y)),
             extended_point1, (0, 255, 0), 2)

    # Extend line from O towards the second vertex
    extended_point2 = (int(vertex_o_x) + 1000 * (int(max_ratio_vertices.vertex2.x) - int(vertex_o_x)),
                       int(vertex_o_y) + 1000 * (int(max_ratio_vertices.vertex2.y) - int(vertex_o_y)))
    cv2.line(image_with_line, (int(vertex_o_x), int(vertex_o_y)),
             extended_point2, (0, 255, 0), 2)

    # Create a mask for the region between the two extended green lines
    mask_lines = np.zeros_like(image_with_line)
    roi_points_lines = np.array([extended_point1, extended_point2, (extended_point2[0], 0), (extended_point1[0], 0)])
    cv2.fillPoly(mask_lines, [roi_points_lines], (255, 255, 255))

    # Make everything inside the circle have a decreased intensity and set it to black
    circle_radius = 400
    max_intensity = 1.0

    while max_intensity >= 0:
        intensity = max_intensity
        image_with_line = draw_white_circle(image_with_line, (vertex_o_x, vertex_o_y), circle_radius, intensity)
        max_intensity -= 1.0
        circle_radius += 10

    # Create a mask for the region inside the circle
    mask_circle = create_white_circle(image_with_line.shape, (vertex_o_x, vertex_o_y), circle_radius, 1)
    mask_circle[mask_circle > 0] = 1

    # Decrease the intensity and set the pixels common between the circle and lines to black
    alpha = 0.5  # You can adjust this value as needed
    cv2.addWeighted(image_with_line, 1 - alpha, mask_circle, alpha, 0, image_with_line)
    cv2.addWeighted(image_with_line, 1, mask_lines, -255, 0, image_with_line)

    cv2.imshow('Image with Line and Circles', image_with_line)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("No red block found in the image.")

