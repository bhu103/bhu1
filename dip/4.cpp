#include <opencv2/opencv.hpp>
#include <cmath>

using namespace cv;

int main() {
    Mat image = imread("1.png");

    if (image.empty()) {
        std::cerr << "Error: Unable to load image!" << std::endl;
        return -1;
    }

    cvtColor(image, image, COLOR_BGR2GRAY);

    Point lightSource(0, 0);

    Mat distanceMap(image.size(), CV_32F);
    for (int y = 0; y < image.rows; ++y) {
        for (int x = 0; x < image.cols; ++x) {
            float distance = 255 - sqrt(pow(x - lightSource.x, 2) + pow(y - lightSource.y, 2));
            distanceMap.at<float>(y, x) = distance;
        }
    }

    normalize(distanceMap, distanceMap, 0, 1, NORM_MINMAX);

    float maxBrightness = 200.0; 
    image.convertTo(image, CV_32F);  
    image += maxBrightness * distanceMap;

    image.convertTo(image, CV_8U);

    namedWindow("DIP PROJECT", WINDOW_NORMAL);
    imshow("DIP PROJECT", image);

    waitKey(0);

    return 0;
}

