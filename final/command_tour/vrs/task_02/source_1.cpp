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