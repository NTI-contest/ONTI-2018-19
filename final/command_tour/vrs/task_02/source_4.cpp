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