#include <opencv2/opencv.hpp>

using namespace cv;

int main() {
    Mat image = imread("1.png");

    if (image.empty()) {
        std::cerr << "Error: Unable to load image!" << std::endl;
        return -1;
    }

    std::cout << "Image dimensions: " << image.rows << " x " << image.cols << std::endl;

    namedWindow("DIP PROJECT", WINDOW_NORMAL);
    imshow("DIP PROJECT", image);

    waitKey(0);

    return 0;
}

