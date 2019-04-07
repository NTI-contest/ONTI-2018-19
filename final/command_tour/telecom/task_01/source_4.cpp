#include <iostream>
#include <vector>
#include <math.h>
#include "Gears.h"
using namespace std;
void main()
{
    GearsSignal gears("gears_config.dat");
    gears.control_period();
}
