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