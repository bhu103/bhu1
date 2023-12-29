#include <opencv2/opencv.hpp>
#include <cmath>

using namespace cv;

int main() {
    Mat image = imread("1.png");

    if (image.empty()) {
        std::cerr << "Error: Unable to load image!" << std::endl;
        return -1;
    }

    Mat redBlock;
    inRange(image, Scalar(0, 0, 255), Scalar(0, 0, 255), redBlock);

    // Find contours in the binary image
    std::vector<std::vector<Point>> contours;
    findContours(redBlock, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

    // Assuming there is only one contour (red rectangle)
    if (!contours.empty()) {
        // Approximate the contour to get vertices
        std::vector<Point> redBlockVertices;
        approxPolyDP(contours[0], redBlockVertices, 1.0, true);

        // Print the coordinates of the red block vertices
        for (const Point& point : redBlockVertices) {
            std::cout << "Vertex: (" << point.x << ", " << point.y << ")" << std::endl;
        }
    }

    Point lightSource(0, 0);

    for (int y = 0; y < image.rows; ++y) {
        for (int x = 0; x < image.cols; ++x) {
            float lightPower = 0.45;
            float distance = lightPower * (255 - sqrt(pow(x - lightSource.x, 2) + pow(y - lightSource.y, 2)));

            Vec3b& pixel = image.at<Vec3b>(y, x);

            for (int c = 0; c < image.channels(); ++c) {
                pixel[c] = saturate_cast<uchar>(pixel[c] + distance);
            }

            if (redBlock.at<uchar>(y, x) > 0) {
                pixel = Vec3b(0, 0, 255);
            }
        }
    }

    namedWindow("DIP PROJECT", WINDOW_NORMAL);
    imshow("DIP PROJECT", image);

    waitKey(0);

    return 0;
}

