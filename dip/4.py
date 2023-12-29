import cv2
import numpy as np

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
            vertices = approx.reshape(-1, 2)
            
            vertex.A = Vertex(vertices[0][0], vertices[0][1])
            vertex.B = Vertex(vertices[1][0], vertices[1][1])
            vertex.C = Vertex(vertices[2][0], vertices[2][1])
            vertex.D = Vertex(vertices[3][0], vertices[3][1])
            
            return vertex

    return None

image_path = '1.png'
vertex = find_red_block_vertices(image_path)

if vertex is not None:
    print("Vertices of the red block:")
    print("A.x:", vertex.A.x, "A.y:", vertex.A.y)
    print("B.x:", vertex.B.x, "B.y:", vertex.B.y)
    print("C.x:", vertex.C.x, "C.y:", vertex.C.y)
    print("D.x:", vertex.D.x, "D.y:", vertex.D.y)
else:
    print("No red block found in the image.")
print("angle AOC -> ")
print((vertex.C.x / vertex.C.y) - (vertex.A.x / vertex.A.y))

