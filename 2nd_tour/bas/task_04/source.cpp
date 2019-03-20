#include <iostream>
#include <iomanip>

#include <stdlib.h>
#include <time.h>
#include <math.h>

using namespace std;

///===========================================================================
/// S point (aircraft) coordinates
double S_XEF, S_YEF, S_ZEF;

/// Aircraft orientation
double psi; 
double theta; 
double gama;   /// Euler angles
double a11, a12, a13,
       a21, a22, a23,
       a31, a32, a33;       /// Rotation matrix

/// N point coordinates
double N_XEF, N_YEF, N_ZEF;
double N_XBF, N_YBF, N_ZBF;
double N_XMCF, N_YMCF;
double N_XPCF, N_YPCF;

/// M point coordinates
double M_XEF, M_YEF, M_ZEF;

/// Camera properties
int RESX = 2592;
int RESY = 1944;
double sx = 1.4e-6;
double sy = 1.4e-6;
double F = 3.6e-3;
double WX, WY;  /// metric width and height of camera shot

extern void solve();
extern double deg2rad(double deg);
extern double rad2deg(double rad);

int main()
{
        /// get input

        cin >> N_XPCF >> N_YPCF;
        cin >> psi >> theta >> gama;
        cin >> S_XEF >> S_YEF >> S_ZEF;

        /// solve problem
        solve();

        /// set output
        cout.setf(std::ios_base::fixed, std::ios_base::floatfield);
        cout.precision(0);
        cout << round(M_XEF) << " " << round(M_ZEF) << endl << endl;

    return 0;
}

void solve()
{
    /// solve problem
    psi   = deg2rad(psi);
    theta = deg2rad(theta);
    gama  = deg2rad(gama);

    /// 1. conver pixels to metric coordinates
    N_XMCF = double(N_XPCF)*sx;
    N_YMCF = double(N_YPCF)*sy;

    /// 2. convert to body frame
    WX = sx*double(RESX);
    WY = sy*double(RESY);

    N_XBF = F;
    N_YBF = -N_XMCF + 0.5*WX;
    N_ZBF = -N_YMCF + 0.5*WY;

    /// 3. convert to earth frame, centered at projection of aircraft
    /// on horizon plane
    a11 = cos(psi)*cos(theta);
    a12 = sin(psi)*sin(gama) - cos(psi)*sin(theta)*cos(gama);
    a13 = sin(psi)*cos(gama) + cos(psi)*sin(theta)*sin(gama);

    a21 = sin(theta);
    a22 = cos(theta)*cos(gama);
    a23 = -cos(theta)*sin(gama);

    a31 = -sin(psi)*cos(theta);
    a32 = cos(psi)*sin(gama) + sin(psi)*sin(theta)*cos(gama);
    a33 = cos(psi)*cos(gama) - sin(psi)*sin(theta)*sin(gama);

    N_XEF = S_XEF + a11*N_XBF + a12*N_YBF + a13*N_ZBF;
    N_YEF = S_YEF + a21*N_XBF + a22*N_YBF + a23*N_ZBF;
    N_ZEF = S_ZEF + a31*N_XBF + a32*N_YBF + a33*N_ZBF;

    //cout << N_XEF << "\t" << N_YEF << "\t" << N_ZEF << "\n";

    /// intersect SN with (O XEF ZEF) (horizon plane)
    M_XEF = -(N_XEF - S_XEF)/(N_YEF - S_YEF)*S_YEF + S_XEF;
    M_YEF = 0.0;
    M_ZEF = -(N_ZEF - S_ZEF)/(N_YEF - S_YEF)*S_YEF + S_ZEF;
}

double deg2rad(double deg)
{
    return deg/180.0*M_PI;
}

double rad2deg(double rad)
{
    return rad*180.0/M_PI;
}