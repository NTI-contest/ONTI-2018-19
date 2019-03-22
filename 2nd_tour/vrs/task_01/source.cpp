#include <murAPI.hpp>

bool is_line(cv::Mat image)
{
    cv::Mat hsv_image;
    // BGR -> HSV
    cv::cvtColor(image, hsv_image, CV_BGR2HSV);

    // Бинаризуем изображение по нижней и верхней границе красного
    cv::Mat lower_red_hue_range;
    cv::Mat upper_red_hue_range;
    cv::inRange(hsv_image, cv::Scalar(0, 100, 100), 
        cv::Scalar(10, 255, 255), lower_red_hue_range);
    cv::inRange(hsv_image, cv::Scalar(160, 100, 100), 
        cv::Scalar(179, 255, 255), upper_red_hue_range);
    cv::Mat red_hue_image;
    cv::addWeighted(lower_red_hue_range, 1.0, 
        upper_red_hue_range, 1.0, 0.0, red_hue_image);

    std::vector<std::vector<cv::Point>> contours;

    // Ищим контуры на бинаризованном изображениее
    cv::findContours(red_hue_image, contours, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE);

    for (std::size_t i = 0; i < contours.size(); i++) {
        if (std::fabs(cv::contourArea(contours.at(i))) < 800.0) {
            continue;
        }
        return true;
    }
    return false;
}

float Yaw(float angle)
{
    float angleNEW = angle;
    if (angleNEW > 90)
        angleNEW = (-1) * (180 - angleNEW);
    return angleNEW;
}

void yaw_and_depth_regulator(float yaw, float depth, int power)
{
    constexpr float k_yaw = 1.3;
    constexpr float k_depth = 6;

    float yaw_diff = mur.getYaw() - yaw;
    if (yaw_diff < 0.0f) {
        yaw_diff += 360.0f;
    }

    if (yaw_diff > 180.0f) {
        yaw_diff -= 360.0f;
    }

    yaw_diff *= k_yaw;

    float depth_diff = mur.getInputAOne() - depth;
    depth_diff *= k_depth;

    mur.setPorts(-power + yaw_diff, -power - yaw_diff, -depth_diff, 0);
}

int main()
{
    mur.addDetectorToList(Object::RECTANGLE, 0);
    mur.addDetectorToList(Object::TRIANGLE, 0);

    float yaw = 0.0f;
    int power = 10;
    float depth = 70.0f;

    auto triangle = [&yaw, &depth, &power]() {
        bool is_triangle_detected = false;

        while (!is_triangle_detected) {
            yaw_and_depth_regulator(yaw, depth, power);
            for (const auto& obj : mur.getDetectedObjectsList(0)) {
                if (obj.type == Object::TRIANGLE) {
                    yaw += Yaw(obj.angle);
                    is_triangle_detected = true;
                    break;
                }
            }
        }

        // Всплываем.
        mur.setPorts(0, 0, -55, 0);
        sleepFor(5000);
    };

    auto line = [&yaw, &depth, &power]() {
        bool is_line_detected = false;

        while (!is_line_detected) {
            yaw_and_depth_regulator(yaw, depth, power);
            for (const auto& obj : mur.getDetectedObjectsList(0)) {
                if (obj.type == Object::RECTANGLE) {
                    yaw += Yaw(obj.angle);
                    is_line_detected = true;
                    break;
                }
            }
        }
    };

    line();
    while (is_line(mur.getCameraOneFrame())) {
        yaw_and_depth_regulator(yaw, depth, power);
    }
    line();
    while (is_line(mur.getCameraOneFrame())) {
        yaw_and_depth_regulator(yaw, depth, power);
    }
    triangle();

    return 0;
}