#include <opencv2/opencv.hpp>

using namespace cv;

int main() {
    Mat image = imread("1.png");

    if (image.empty()) {
        std::cerr << "Error: Unable to load image!" << std::endl;
        return -1;
    }

    Mat redMask;
    inRange(image, Scalar(0, 0, 255), Scalar(0, 0, 255), redMask);

    namedWindow("DIP PROJECT", WINDOW_NORMAL);
    imshow("DIP PROJECT", image);

    namedWindow("Red Color Mask", WINDOW_NORMAL);
    imshow("Red Color Mask", redMask);

    waitKey(0);

    return 0;
}

