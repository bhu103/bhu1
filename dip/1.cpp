#include <opencv2/opencv.hpp>

using namespace cv;

int main() {
    Mat image = imread("1.png");

    if (image.empty()) {
        std::cerr << "Error: Unable to load image!" << std::endl;
        return -1;
    }

    namedWindow("Input Image", WINDOW_NORMAL);
    imshow("Input Image", image);

    waitKey(0);

    return 0;
}

