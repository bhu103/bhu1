#include <opencv2/opencv.hpp>
#include <cmath>

using namespace cv;

int main() {
    Mat image = imread("1.png");

    if (image.empty()) {
        std::cerr << "Error: Unable to load image!" << std::endl;
        return -1;
    }

    Mat redBlock = image.clone();  
    inRange(image, Scalar(0, 0, 200), Scalar(0, 0, 255), redBlock);  

    Mat grayImage;
    cvtColor(image, grayImage, COLOR_BGR2GRAY);

    Point lightSource(0, 0);

    Mat distanceMap(grayImage.size(), CV_32F);
    for (int y = 0; y < grayImage.rows; ++y) {
        for (int x = 0; x < grayImage.cols; ++x) {
            float distance = 255 - sqrt(pow(x - lightSource.x, 2) + pow(y - lightSource.y, 2));
            distanceMap.at<float>(y, x) = distance;
        }
    }

    normalize(distanceMap, distanceMap, 0, 1, NORM_MINMAX);

    float maxBrightness = 200.0;
    grayImage.convertTo(grayImage, CV_32F);
    grayImage += maxBrightness * distanceMap;

    //grayImage.setTo(0, redBlock);  

    grayImage.convertTo(grayImage, CV_8UC3);
    grayImage.setTo(0,redBlock);

    namedWindow("DIP PROJECT", WINDOW_NORMAL);
    imshow("DIP PROJECT", grayImage);

    waitKey(0);

    return 0;
}

