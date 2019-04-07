#include <murAPI.hpp>

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

int main() {
  //Берем текущий курс
  auto yaw = mur.getYaw(); 
  // Заглубляемся на 1м и идем прямо 15 секунда
  yd_p_reg_timed(yaw, 100, 30, 15000); 
  //Стреляем 
  mur.setPortD(100); 
  //Всплываем.
  yd_p_reg_timed(yaw, 0, 0, 5000); 
}