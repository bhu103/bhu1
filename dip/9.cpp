#include <opencv2/opencv.hpp>

using namespace cv;

int main() {
    // Load input image
    Mat inputImage = imread("1.png");

    if (inputImage.empty()) {
        std::cerr << "Error: Unable to load image!" << std::endl;
        return -1;
    }

    // Get image dimensions
    int imageWidth = inputImage.cols;
    int imageHeight = inputImage.rows;

    // Create a new black image with the same dimensions
    Mat outputImage = Mat::zeros(imageHeight, imageWidth, CV_8UC3);

    // Define the color range for red in HSV format
    Scalar lower_red = Scalar(0, 100, 100);
    Scalar upper_red = Scalar(10, 255, 255);

    // Convert the input image to HSV format
    Mat hsvImage;
    cvtColor(inputImage, hsvImage, COLOR_BGR2HSV);

    // Threshold the image to get the red block
    Mat redBlock;
    inRange(hsvImage, lower_red, upper_red, redBlock);

    // Find contours in the binary image
    std::vector<std::vector<Point>> contours;
    findContours(redBlock, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

    // Assuming there is only one contour (red rectangle)
    if (!contours.empty()) {
        // Approximate the contour to get vertices
        std::vector<Point> redBlockVertices;
        approxPolyDP(contours[0], redBlockVertices, 1.0, true);

        // Apply light source effect to the red block
        Point lightSource(1, 1);

        for (const Point& vertex : redBlockVertices) {
            int x = vertex.x;
            int y = vertex.y;

            float distance = 0.45 * (255 - sqrt(pow(x - lightSource.x, 2) + pow(y - lightSource.y, 2)));

            Vec3b& pixel = inputImage.at<Vec3b>(y, x);

            for (int c = 0; c < inputImage.channels(); ++c) {
                pixel[c] = saturate_cast<uchar>(pixel[c] + distance);
            }

            // Draw the red block on the output image
            outputImage.at<Vec3b>(y, x) = Vec3b(0, 0, 255);
        }
    }

    // Display the output image
    namedWindow("Output Image", WINDOW_NORMAL);
    imshow("Output Image", outputImage);

    waitKey(0);

    return 0;
}

