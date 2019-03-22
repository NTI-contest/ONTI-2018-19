#include "murAPI.hpp"

Object detect_yellow_object(cv::Mat img)
{
    int hmin = 20, hmax = 30;
    int smin = 100, smax = 255;
    int vmin = 100, vmax = 255;

    cv::Scalar lower(hmin, smin, vmin);
    cv::Scalar upper(hmax, smax, vmax);

    cv::Mat hsv;
    cv::cvtColor(img, hsv, CV_BGR2HSV);
    cv::inRange(hsv, lower, upper, hsv);
    cv::imshow("W", hsv);
    cv::waitKey(1);
    std::vector<std::vector<cv::Point>> contours;
    cv::findContours(hsv, contours, CV_RETR_TREE, CV_CHAIN_APPROX_NONE);
    Object object_to_ret;

    for (std::size_t i = 0; i < contours.size(); i++) {
        if (contours.at(i).size() < 5) {
            continue;
        }
        if (std::fabs(cv::contourArea(contours.at(i))) < 150.0) {
            continue;
        }
        cv::RotatedRect b_ellipse = cv::fitEllipse(contours.at(i));
        object_to_ret.x = (int)b_ellipse.center.x;
        object_to_ret.y = (int)b_ellipse.center.y;
        object_to_ret.angle = b_ellipse.angle;
        object_to_ret.type = Object::RECTANGLE;
        object_to_ret.size = cv::contourArea(contours.at(i));

        return object_to_ret;
    }
    return object_to_ret;
}

Object detect_green_object(cv::Mat img)
{
    int hmin = 50, hmax = 75;
    int smin = 105, smax = 255;
    int vmin = 0, vmax = 255;

    cv::Scalar lower(hmin, smin, vmin);
    cv::Scalar upper(hmax, smax, vmax);

    cv::Mat hsv;
    cv::cvtColor(img, hsv, CV_BGR2HSV);
    cv::inRange(hsv, lower, upper, hsv);

    std::vector<std::vector<cv::Point>> contours;
    cv::findContours(hsv, contours, CV_RETR_TREE, CV_CHAIN_APPROX_NONE);
    Object object_to_ret;

    for (std::size_t i = 0; i < contours.size(); i++) {
        if (contours.at(i).size() < 5) {
            continue;
        }
        if (std::fabs(cv::contourArea(contours.at(i))) < 300.0) {
            continue;
        }
        cv::RotatedRect b_ellipse = cv::fitEllipse(contours.at(i));
        object_to_ret.x = (int)b_ellipse.center.x;
        object_to_ret.y = (int)b_ellipse.center.y;
        object_to_ret.angle = b_ellipse.angle;
        object_to_ret.type = Object::RECTANGLE;
        return object_to_ret;
    }
    return object_to_ret;
}

int is_line(cv::Mat image)
{
    int line_count = 0;
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
        line_count++;
    }
    return line_count;
}

float yaw_from_angle(float angle)
{
    float angle_new = angle;

    if (angle_new > 90.0) {
        angle_new = -1 * (180.0 - angle_new);
    }

    return angle_new;
}

void cw(bool move = false)
{
    mur.setPortA(-30);
    mur.setPortB(0);

    if (move) {
        mur.setPortB(30);
    }
}

void ccw(bool move = false)
{
    mur.setPortA(0);
    mur.setPortB(-30);

    if (move) {
        mur.setPortA(30);
    }
}
void yaw_and_depth_regulator(float yaw, float depth, int power)
{
    auto c_yaw = mur.getYaw();
    constexpr float k_depth = 6;

    auto d = std::fmod((yaw - c_yaw + 540.0f), 360.0f) - 180.0f;
    bool move = false;
    if (power == 0) {
        move = true;
    }

    if (d > 0) {
        cw(move);
    } else {
        ccw(move);
    }

    float depth_diff = mur.getInputAOne() - depth;
    depth_diff *= k_depth;
    mur.setPortC(-depth_diff);
}

bool move_to_v_center(int x_val)
{
    constexpr auto center_v = 320 / 2;
    auto center_diff = x_val - center_v;

    if (std::abs(center_diff) < 25) {
        mur.setPortD(0);
        return true;
    }

    if (center_diff < 0) {
        mur.setPortD(-15);
    }

    if (center_diff > 0) {
        mur.setPortD(15);
    }
    return false;
}

float yaw_to_180(float yaw)
{
    if (yaw < 0.0f) {
        yaw += 360.0f;
    }

    if (yaw > 180.0f) {
        yaw -= 360.0f;
    }
    return yaw;
}

bool move_to_hv_center(int x, int y)
{
    constexpr auto center_v = 320 / 2;
    constexpr auto center_h = 240 / 2;

    auto center_x_diff = x - center_v;
    auto center_y_diff = y - center_h;
    if (std::abs(center_x_diff) < 10 && std::abs(center_y_diff) < 10) {
        mur.setPortD(0);
        return true;
    }

    if (center_x_diff < 0) {
        mur.setPortD(-15);
    }

    if (center_x_diff > 0) {
        mur.setPortD(15);
    }

    if (center_y_diff < 0) {
        mur.setPortA(-15);
        mur.setPortB(-15);
    }

    if (center_y_diff > 0) {
        mur.setPortA(15);
        mur.setPortB(15);
    }

    return false;
}

bool move_to_hv_center_front(int x, int y)
{

    constexpr auto center_v = 320 / 2;
    constexpr auto center_h = 240 / 2;

    mur.setPortA(0);
    mur.setPortB(0);


    auto center_x_diff = x - center_v;
    auto center_y_diff = y - center_h;
    if (std::abs(center_x_diff) < 10 && std::abs(center_y_diff) < 10) {
        mur.setPortD(0);
        return true;
    }

    if (center_x_diff < 0) {
        mur.setPortD(-15);
    }

    if (center_x_diff > 0) {
        mur.setPortD(15);
    }

    if (center_y_diff < 0) {
        mur.setPortC(-15);
    }

    if (center_y_diff > 0) {
        mur.setPortC(15);
    }

    return false;
}

int main()
{
    float yaw = 0.0f;
    int power = 10;
    float depth = 70.0f;

    mur.addDetectorToList(Object::RECTANGLE, 0);
    mur.addDetectorToList(Object::TRIANGLE, 0);

    auto line = [&yaw, &depth, &power]() {
        bool is_line_detected = false;

        while (!is_line_detected) {
            yaw_and_depth_regulator(yaw, depth, power);
            for (const auto& obj : mur.getDetectedObjectsList(0)) {
                if (obj.type == Object::RECTANGLE) {
                    yaw += yaw_from_angle(obj.angle);
                    is_line_detected = true;
                    break;
                }
            }
        }
    };

    auto gate_green = [&yaw, &depth, &power]() {
        bool is_gate_centrated = false;
        while (!is_gate_centrated) {
            auto image = mur.getCameraTwoFrame();
            auto result = detect_green_object(image);
            if (move_to_v_center(result.x)) {
                is_gate_centrated = true;
            }
            yaw_and_depth_regulator(0.0, 80, 0);
        }
    };

    auto bin_green = [&yaw, &depth, &power]() {
        bool is_bin_centrated = false;
        while (!is_bin_centrated) {
            auto image = mur.getCameraOneFrame();
            auto result = detect_green_object(image);
            yaw_and_depth_regulator(yaw, depth, power);
            if (result.type == Object::NONE) {
                continue;
            }
            if (move_to_hv_center(result.x, result.y)) {
                mur.drop();
                is_bin_centrated = true;
            }
        }
    };

    auto skip_lines = [&yaw, &depth, &power](int line_count) {
        while (is_line(mur.getCameraOneFrame()) != line_count) {
            yaw_and_depth_regulator(yaw, depth, power);
        }
    };

    auto triangle = [&yaw, &depth, &power]() {
        bool is_triangle_detected = false;

        while (!is_triangle_detected) {
            yaw_and_depth_regulator(yaw, depth, power);
            for (auto&& obj : mur.getDetectedObjectsList(0)) {
                if (obj.type == Object::TRIANGLE) {
                    is_triangle_detected = true;
                    break;
                }
            }
        }
        if (is_triangle_detected) {
            mur.setPorts(0, 0, -55, 0);
            sleepFor(5000);
        }
    };

    auto find_yellow = [&yaw, &depth, &power]() {
        bool is_yellow_found = false;
        yaw_and_depth_regulator(yaw, depth, 0);
        while (!is_yellow_found) {
            auto image = mur.getCameraTwoFrame();
            auto result = detect_yellow_object(image);
            if (result.type == Object::NONE) {
                yaw += 5.0f;
   
                if (yaw > 360.0f) {
                    yaw -= 360;
                }

                while (std::fabs(yaw - mur.getYaw()) > 5) {
                    yaw_and_depth_regulator(yaw, depth, 0);
                }

                continue;
            } else if (result.type == Object::RECTANGLE) {
                is_yellow_found = true;
                break;
            }
            yaw_and_depth_regulator(yaw, depth, 0);
        }
    };

    auto move_to_yellow = [&yaw, &depth, &power]() {
        bool is_yellow_found = false;
        while (!is_yellow_found) {
            auto image = mur.getCameraTwoFrame();
            auto result = detect_yellow_object(image);
            if (result.type == Object::RECTANGLE) {
                if (result.size < 6500) {
                    yaw_and_depth_regulator(yaw, depth, 10);
                } else {
                    yaw_and_depth_regulator(yaw, depth, 0);
                    break;
                }
            }
        }
    };

    auto centrate_on_yellow = [&yaw, &depth, &power]() {
        bool is_yellow_found = false;
        yaw_and_depth_regulator(yaw, depth, 0);
        while (!is_yellow_found) {
            auto image = mur.getCameraTwoFrame();
            auto result = detect_yellow_object(image);
            if (result.type == Object::NONE) {
                continue;
            } else if (result.type == Object::RECTANGLE) {
                if (move_to_hv_center_front(result.x, result.y)) {
                    depth = mur.getInputAOne();
                    yaw = mur.getYaw();
                    is_yellow_found = true;
                    break;
                }
            }
        }
    };

    auto shoot_and_rotate = [&yaw, &depth, &power]() {
        mur.shoot();
        depth = 70;
        yaw += 180;
        if (yaw > 360) {
            yaw -= 360;
        }
    };
  gate_green();

    line();
    depth = 40;

    skip_lines(2);
    skip_lines(1);

    line();
    depth = 70;
    bin_green();
    find_yellow();
    centrate_on_yellow();
    move_to_yellow();
    centrate_on_yellow();
    shoot_and_rotate();
    skip_lines(1);
    line();
    skip_lines(0);
    triangle();

    return 0;
}