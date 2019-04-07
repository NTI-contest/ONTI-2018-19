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