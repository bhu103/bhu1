#include <opencv2/opencv.hpp>
#include <cmath>

using namespace cv;

double calculateDistance(const Point& point1, const Point& point2) {
    return sqrt(pow(point2.x - point1.x, 2) + pow(point2.y - point1.y, 2));
}

double calculateAngle(const Point& vertex1, const Point& vertex2, const Point& vertex3) {
    double side1 = calculateDistance(vertex1, vertex2);
    double side2 = calculateDistance(vertex2, vertex3);
    double side3 = calculateDistance(vertex3, vertex1);

    return acos((pow(side1, 2) + pow(side3, 2) - pow(side2, 2)) / (2 * side1 * side3));
}

int main() {
    Mat image = imread("1.png");

    if (image.empty()) {
        std::cerr << "Error: Unable to load image!" << std::endl;
        return -1;
    }

    Mat hsvImage;
    cvtColor(image, hsvImage, COLOR_BGR2HSV);

    Mat redBlockMask;
    inRange(hsvImage, Scalar(0, 100, 100), Scalar(10, 255, 255), redBlockMask);

    std::vector<std::vector<Point>> contours;
    findContours(redBlockMask, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

    // Assuming there is only one contour (red rectangle)
    if (!contours.empty()) {
        // Approximate the contour to get vertices
        std::vector<Point> redBlockVertices;
        approxPolyDP(contours[0], redBlockVertices, 1.0, true);

        // Print the coordinates of the red block vertices
        for (const Point& point : redBlockVertices) {
            std::cout << "Vertex: (" << point.x << ", " << point.y << ")" << std::endl;
        }

        double angleAOB = calculateAngle(redBlockVertices[0], redBlockVertices[1], redBlockVertices[3]);
        double angleBOC = calculateAngle(redBlockVertices[1], redBlockVertices[2], redBlockVertices[0]);
        double angleCOD = calculateAngle(redBlockVertices[2], redBlockVertices[3], redBlockVertices[1]);
        double angleDOA = calculateAngle(redBlockVertices[3], redBlockVertices[0], redBlockVertices[2]);

        double angleAOC = calculateAngle(redBlockVertices[0], redBlockVertices[2], redBlockVertices[1]);
        double angleBOD = calculateAngle(redBlockVertices[1], redBlockVertices[3], redBlockVertices[2]);

        std::cout << "Angle AOB: " << angleAOB * (180.0 / CV_PI) << " degrees" << std::endl;
        std::cout << "Angle BOC: " << angleBOC * (180.0 / CV_PI) << " degrees" << std::endl;
        std::cout << "Angle COD: " << angleCOD * (180.0 / CV_PI) << " degrees" << std::endl;
        std::cout << "Angle DOA: " << angleDOA * (180.0 / CV_PI) << " degrees" << std::endl;
        std::cout << "Angle AOC: " << angleAOC * (180.0 / CV_PI) << " degrees" << std::endl;
        std::cout << "Angle BOD: " << angleBOD * (180.0 / CV_PI) << " degrees" << std::endl;
    }

    // Draw the red block on the image
    drawContours(image, contours, 0, Scalar(0, 0, 255), 2);

    // Display the image
    namedWindow("DIP PROJECT", WINDOW_NORMAL);
    imshow("DIP PROJECT", image);

    waitKey(0);

    return 0;
}

