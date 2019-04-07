#include "murAPI.hpp"

Object detect_green(cv::Mat &image) {
  static const cv::Scalar lower(50, 150, 160);
  static const cv::Scalar upper(80, 255, 255);
  Object to_ret;
  cv::Mat img = image.clone();

  cv::cvtColor(img, img, CV_BGR2HSV);
  cv::inRange(img, lower, upper, img);
  std::vector<std::vector<cv::Point>> contours;
  cv::findContours(img, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
  auto max_area = 0;
  std::vector<cv::RotatedRect> rects;
  for (std::size_t idx = 0; idx < contours.size(); ++idx) {

    if (contours.at(idx).size() < 5) {
      continue;
    }

    std::vector<cv::Point> hull;
    cv::convexHull(contours.at(idx), hull, true);
    cv::approxPolyDP(hull, hull, 24, true);

    if (hull.size() < 3UL) {
      continue;
    }

    auto ellipse = cv::fitEllipse(contours.at(idx));
    rects.push_back(ellipse);
  }

  auto min_index = 0;
  auto min_value = std::numeric_limits<int>::max();

  for (std::size_t idx = 0; idx < rects.size(); ++idx) {
    if (rects.at(idx).center.y < min_value) {
      min_index = idx;
    }
  }

  auto &rect = rects.at(min_index);
  to_ret.x = rect.center.x;
  to_ret.y = rect.center.y;
  to_ret.type = Object::RECTANGLE;
  return to_ret;
}

Object detect_yellow(cv::Mat &image) {
  static const cv::Scalar lower(0, 100, 60);
  static const cv::Scalar lower(0, 150, 210);
  static const cv::Scalar upper(85, 255, 255);
  Object to_ret;
  cv::Mat img = image.clone();

  cv::cvtColor(img, img, CV_BGR2HSV);
  cv::inRange(img, lower, upper, img);
  std::vector<std::vector<cv::Point>> contours;
  cv::findContours(img, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
  auto max_area = 0;
  std::vector<cv::RotatedRect> rects;
  for (std::size_t idx = 0; idx < contours.size(); ++idx) {

    if (contours.at(idx).size() < 5) {
      continue;
    }

    std::vector<cv::Point> hull;
    cv::convexHull(contours.at(idx), hull, true);
    cv::approxPolyDP(hull, hull, 24, true);

    if (hull.size() < 3UL) {
      continue;
    }

    auto ellipse = cv::fitEllipse(contours.at(idx));
    to_ret.x = ellipse.center.x;
    to_ret.y = ellipse.center.y;
    to_ret.angle = ellipse.angle;
    to_ret.type = Object::RECTANGLE;
  }

  auto max_index = 0;
  auto max_value = std::numeric_limits<int>::min();

  for (std::size_t idx = 0; idx < rects.size(); ++idx) {
    if (rects.at(idx).center.y > max_value) {
      max_index = idx;
    }
  }

  auto &rect = rects.at(max_index);
  to_ret.x = rect.center.x;
  to_ret.y = rect.center.y;
  return to_ret;

  return to_ret;
}

/*
Функция определения линии.
*/
Object detect_line(cv::Mat &image) {
  static const cv::Scalar lower(0, 100, 60);
  static const cv::Scalar upper(20, 255, 255);
  Object to_ret;
  cv::Mat img = image.clone();

  cv::cvtColor(img, img, CV_BGR2HSV);
  cv::inRange(img, lower, upper, img);
  std::vector<std::vector<cv::Point>> contours;
  cv::findContours(img, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
  auto max_area = 0;

  for (std::size_t idx = 0; idx < contours.size(); ++idx) {

    if (contours.at(idx).size() < 5) {
      continue;
    }

    std::vector<cv::Point> hull;
    cv::convexHull(contours.at(idx), hull, true);
    cv::approxPolyDP(hull, hull, 24, true);

    if (hull.size() < 3UL) {
      continue;
    }

    auto ellipse = cv::fitEllipse(contours.at(idx));
    to_ret.x = ellipse.center.x;
    to_ret.y = ellipse.center.y;
    to_ret.angle = ellipse.angle;
  }
  return to_ret;
}

/*
Функция определения звезды.
*/
Object detect_start(cv::Mat &image) {
  static const cv::Scalar lower(23, 200, 94);
  static const cv::Scalar upper(50, 255, 122);
  Object to_ret;
  cv::Mat img = image.clone();

  cv::cvtColor(img, img, CV_BGR2HSV);
  cv::inRange(img, lower, upper, img);
  cv::imshow("W", img);
  cv::waitKey(1);
  std::vector<std::vector<cv::Point>> contours;
  cv::findContours(img, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);

  auto max_area = 0;

  for (std::size_t idx = 0; idx < contours.size(); ++idx) {

    if (contours.at(idx).size() < 5) {
      continue;
    }

    std::vector<cv::Point> hull;
    cv::convexHull(contours.at(idx), hull, true);
    cv::approxPolyDP(hull, hull, 24, true);

    if (hull.size() > 3UL && hull.size() < 5UL) {
      to_ret.type = Object::CIRCLE;
    } else {
      to_ret.type = Object::TRIANGLE;
    }

    auto ellipse = cv::fitEllipse(contours.at(idx));
    to_ret.x = ellipse.center.x;
    to_ret.y = ellipse.center.y;
    to_ret.angle = ellipse.angle;
  }
  return to_ret;
}

void yd_p_reg(double yaw, double depth, int power) {
  double u = mur.getYaw() - yaw;
  if (u < 0.0) {
    u += 360.0;
  }
  if (u > 180.0) {
    u -= 360.0;
  }
  u *= 1.3;
  double ddepth = mur.getInputAOne() - depth;
  ddepth *= 6;
  mur.setPorts(-power + u, -power - u, -ddepth, 0);
}

void yd_p_reg_timed(double yaw, double depth, int power, long long time) {
  Timer t;
  t.start();
  while (t.elapsed() < time) {
    yd_p_reg(yaw, depth, power);
  }
}

double from_cv_angle(double angle) {
  auto new_angle = angle;
  if (new_angle > 90) {
    new_angle = (-1.0) * (180.0 - new_angle);
  }
  return new_angle;
}

void yd_p_reg_line(double depth, int power) {
  auto img = mur.getCameraOneFrame();
  auto obj = detect_line(img);
  double u = (0.0 - from_cv_angle(obj.angle)) * 1.3;
  double ddepth = (mur.getInputAOne() - depth) * 6.0;
  double u_lag = 160.0 - obj.x;
  mur.setPorts(-power + u, -power - u, -ddepth, -u_lag);
}

bool move_to_v_center(int x_val) {
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

bool move_to_hv_center_front(int x, int y) {

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

int main() {
  yd_p_reg_timed(0, 70, 30, 3000);

  auto rotate_to_180 = []() {
    auto yaw = mur.getYaw();
    yd_p_reg_timed(yaw + 180.0, 70, 30, 3000);
  };

  auto rotate_to_yellow = []() {
    auto yaw = mur.getYaw();
    yd_p_reg_timed(yaw, 30, 30, 15000);
    yd_p_reg_timed(yaw + 180.0, 70, 30, 3000);
  };

  auto line_and_bin = []() {
    for (;;) {
      auto img = mur.getCameraOneFrame();
      yd_p_reg_line(100, 15);
      auto star_obj = detect_start(img);

      if (star_obj.type == Object::NONE) {
        continue;
      }

      if (star_obj.type == Object::RECTANGLE) {
        break;
      }

      bool in_center = false;
      mur.setPorts(0, 0, 0, 0);
      while (!in_center) {
        img = mur.getCameraOneFrame();
        star_obj = detect_start(img);
        in_center = move_to_v_center(star_obj.x);
        mur.setPortC((mur.getInputAOne() - 100.0) * -6);
      }
      mur.drop();
      break;
    }
  };

  auto shoot_green_side = []() {
    for (;;) {
      auto img = mur.getCameraTwoFrame();
      yd_p_reg_line(100, 15);
      auto green_side = detect_green(img);

      if (green_side.type == Object::NONE) {
        continue;
      }

      bool in_center = false;
      mur.setPorts(0, 0, 0, 0);
      while (!in_center) {
        img = mur.getCameraTwoFrame();
        green_side = detect_green(img);
        in_center = move_to_hv_center_front(green_side.x, green_side.y);
        mur.setPortC((mur.getInputAOne() - 100.0) * -6);
      }
      mur.shoot();
      break;
    }
  };

  auto shoot_yellow_side = []() {
    for (;;) {
      auto img = mur.getCameraTwoFrame();
      yd_p_reg_line(100, 15);
      auto yellow_side = detect_yellow(img);

      if (yellow_side.type == Object::NONE) {
        continue;
      }

      bool in_center = false;
      mur.setPorts(0, 0, 0, 0);
      while (!in_center) {
        img = mur.getCameraTwoFrame();
        yellow_side = detect_yellow(img);
        in_center = move_to_hv_center_front(yellow_side.x, yellow_side.y);
        mur.setPortC((mur.getInputAOne() - 100.0) * -6);
      }
      mur.shoot();
      break;
    }
  };

  auto stop_at_yellow = []() {
    for (;;) {
      auto img = mur.getCameraOneFrame();
      yd_p_reg_line(100, 15);
      auto yellow_side = detect_yellow(img);

      if (yellow_side.type == Object::NONE) {
        continue;
      }

      bool in_center = false;
      mur.setPorts(0, 0, 0, 0);
      while (!in_center) {
        img = mur.getCameraOneFrame();
        yellow_side = detect_yellow(img);
        in_center = move_to_hv_center_front(yellow_side.x, yellow_side.y);
        mur.setPortC((mur.getInputAOne() - 100.0) * -6);
      }
      yd_p_reg_timed(mur.getYaw(), 200, 30, 30000);
      break;
    }
  };

  line_and_bin();
  line_and_bin();
  shoot_green_side();
  rotate_to_yellow();
  shoot_yellow_side();
  rotate_to_180();
  line_and_bin();
  stop_at_yellow();
}