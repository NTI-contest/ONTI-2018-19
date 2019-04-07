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