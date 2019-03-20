#include <iostream>
#include <math.h>

using namespace std;

int WPT1_DD_x, WPT1_MM_x; double WPT1_SS_x;
int WPT1_DD_z, WPT1_MM_z; double WPT1_SS_z;
int WPT2_DD_x, WPT2_MM_x; double WPT2_SS_x;
int WPT2_DD_z, WPT2_MM_z; double WPT2_SS_z;
int WPT3_DD_x, WPT3_MM_x; double WPT3_SS_x;
int WPT3_DD_z, WPT3_MM_z; double WPT3_SS_z;

double R;
int A_DD_x, A_MM_x; double A_SS_x;
int A_DD_z, A_MM_z; double A_SS_z;
int B_DD_x, B_MM_x; double B_SS_x;
int B_DD_z, B_MM_z; double B_SS_z;
int O_DD_x, O_MM_x; double O_SS_x;
int O_DD_z, O_MM_z; double O_SS_z;

extern void solve();
extern double deg2rad(double deg);
extern double rad2deg(double rad);

int main()
{
   	/// get input
	cin >> R;
	cin >> WPT1_DD_z >> WPT1_MM_z >> WPT1_SS_z;
	cin >> WPT1_DD_x >> WPT1_MM_x >> WPT1_SS_x;
	cin >> WPT2_DD_z >> WPT2_MM_z >> WPT2_SS_z;
	cin >> WPT2_DD_x >> WPT2_MM_x >> WPT2_SS_x;
	cin >> WPT3_DD_z >> WPT3_MM_z >> WPT3_SS_z;
	cin >> WPT3_DD_x >> WPT3_MM_x >> WPT3_SS_x;

	/// solve problem
	solve();

	/// set output
	cout.setf(std::ios_base::fixed, std::ios_base::floatfield);
	cout.precision(10);
	cout <<  A_DD_z << " " << A_MM_z << " " << A_SS_z << " ";
	cout <<  A_DD_x << " " << A_MM_x << " " << A_SS_x << "\n";
	cout <<  B_DD_z << " " << B_MM_z << " " << B_SS_z << " ";
	cout <<  B_DD_x << " " << B_MM_x << " " << B_SS_x << "\n";
	cout <<  O_DD_z << " " << O_MM_z << " " << O_SS_z << " ";
	cout <<  O_DD_x << " " << O_MM_x << " " << O_SS_x << "\n";
	cout << "\n";

    return 0;
}

void solve()
{
    /// constants
    const double RE = 6371000.0;   // Earth radius, m

    /// waypoints

    // GF
    double WPT1_GF_x = double(WPT1_DD_x) + double(WPT1_MM_x)/60.0 + WPT1_SS_x/3600.0;
    double WPT1_GF_z = double(WPT1_DD_z) + double(WPT1_MM_z)/60.0 + WPT1_SS_z/3600.0;

    double WPT2_GF_x = double(WPT2_DD_x) + double(WPT2_MM_x)/60.0 + WPT2_SS_x/3600.0;
    double WPT2_GF_z = double(WPT2_DD_z) + double(WPT2_MM_z)/60.0 + WPT2_SS_z/3600.0;

    double WPT3_GF_x = double(WPT3_DD_x) + double(WPT3_MM_x)/60.0 + WPT3_SS_x/3600.0;
    double WPT3_GF_z = double(WPT3_DD_z) + double(WPT3_MM_z)/60.0 + WPT3_SS_z/3600.0;

    // coefs GFOC - cartesian FOC
    double LAT2M = 2.0*M_PI*RE/360.0;
    double LNG2M = 2.0*M_PI*RE*cos(deg2rad(WPT2_GF_x))/360.0;

    // Cartesian frame
    double vec21_GF_x = WPT1_GF_x - WPT2_GF_x;
    double vec21_GF_z = WPT1_GF_z - WPT2_GF_z;

    double vec23_GF_x = WPT3_GF_x - WPT2_GF_x;
    double vec23_GF_z = WPT3_GF_z - WPT2_GF_z;

    double WPT2_CF_x = 0;
    double WPT2_CF_z = 0;

    double WPT1_CF_x = WPT2_CF_x + vec21_GF_x*LAT2M;
    double WPT1_CF_z = WPT2_CF_z + vec21_GF_z*LNG2M;

    double WPT3_CF_x = WPT2_CF_x + vec23_GF_x*LAT2M;
    double WPT3_CF_z = WPT2_CF_z + vec23_GF_z*LNG2M;

    /// turn geometry
    double vec21_CF_x = WPT1_CF_x - WPT2_CF_x;
    double vec21_CF_z = WPT1_CF_z - WPT2_CF_z;

    double vec23_CF_x = WPT3_CF_x - WPT2_CF_x;
    double vec23_CF_z = WPT3_CF_z - WPT2_CF_z;

    double crossProd = (vec21_CF_z*vec23_CF_x - vec21_CF_x*vec23_CF_z);
    double dotProd   = (vec21_CF_x*vec23_CF_x + vec21_CF_z*vec23_CF_z);

    double Turn = M_PI - atan2(crossProd, dotProd);
	
	Turn = atan2(sin(Turn), cos(Turn));

    // turn lead distance, m
    double TLD = R*tan(fabs(Turn)/2.0);

    /// points A, B
    double dir21_x = vec21_CF_x/sqrt(vec21_CF_x*vec21_CF_x + vec21_CF_z*vec21_CF_z);
    double dir21_z = vec21_CF_z/sqrt(vec21_CF_x*vec21_CF_x + vec21_CF_z*vec21_CF_z);

    double dir23_x = vec23_CF_x/sqrt(vec23_CF_x*vec23_CF_x + vec23_CF_z*vec23_CF_z);
    double dir23_z = vec23_CF_z/sqrt(vec23_CF_x*vec23_CF_x + vec23_CF_z*vec23_CF_z);

    double A_CF_x = WPT2_CF_x + dir21_x*TLD;
    double A_CF_z = WPT2_CF_z + dir21_z*TLD;

    double B_CF_x = WPT2_CF_x + dir23_x*TLD;
    double B_CF_z = WPT2_CF_z + dir23_z*TLD;

    /// point O
    double A1 = dir21_x;  double B1 = dir21_z;
    double A2 = dir23_x;  double B2 = dir23_z;
    double xa = A_CF_x;   double ya = A_CF_z;
    double xb = B_CF_x;   double yb = B_CF_z;
    double C1 = A1*xa + B1*ya;
    double C2 = A2*xb + B2*yb;
    double delta  = A1*B2 - A2*B1;
    double delta1 = C1*B2 - C2*B1;
    double delta2 = A1*C2 - A2*C1;
    double O_CF_x = delta1/delta;
    double O_CF_z = delta2/delta;

    /// Answer
    double A_GF_x = WPT2_GF_x + A_CF_x/LAT2M;
    double A_GF_z = WPT2_GF_z + A_CF_z/LNG2M;

    double B_GF_x = WPT2_GF_x + B_CF_x/LAT2M;
    double B_GF_z = WPT2_GF_z + B_CF_z/LNG2M;

    double O_GF_x = WPT2_GF_x + O_CF_x/LAT2M;
    double O_GF_z = WPT2_GF_z + O_CF_z/LNG2M;

    A_DD_x = floor(A_GF_x);
    A_MM_x = floor(60.0*(A_GF_x - double(A_DD_x)));
    A_SS_x = 3600.0*(A_GF_x - double(A_DD_x) - double(A_MM_x)/60.0);

    A_DD_z = floor(A_GF_z);
    A_MM_z = floor(60.0*(A_GF_z - double(A_DD_z)));
    A_SS_z = 3600.0*(A_GF_z - double(A_DD_z) - double(A_MM_z)/60.0);

    B_DD_x = floor(B_GF_x);
    B_MM_x = floor(60.0*(B_GF_x - double(B_DD_x)));
    B_SS_x = 3600.0*(B_GF_x - double(B_DD_x) - double(B_MM_x)/60.0);

    B_DD_z = floor(B_GF_z);
    B_MM_z = floor(60.0*(B_GF_z - double(B_DD_z)));
    B_SS_z = 3600.0*(B_GF_z - double(B_DD_z) - double(B_MM_z)/60.0);

    O_DD_x = floor(O_GF_x);
    O_MM_x = floor(60.0*(O_GF_x - double(O_DD_x)));
    O_SS_x = 3600.0*(O_GF_x - double(O_DD_x) - double(O_MM_x)/60.0);

    O_DD_z = floor(O_GF_z);
    O_MM_z = floor(60.0*(O_GF_z - double(O_DD_z)));
    O_SS_z = 3600.0*(O_GF_z - double(O_DD_z) - double(O_MM_z)/60.0);
}

double deg2rad(double deg)
{
    return deg/180.0*M_PI;
}

double rad2deg(double rad)
{
    return rad*180.0/M_PI;
}