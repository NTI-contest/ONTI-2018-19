#include <iostream>
#include <math.h>

using namespace std;

///===========================================================================
class PitotTube
{
public:
    PitotTube();
    ~PitotTube();

    void compute(double q, double rho, double a);

    double getAirspeed() { return V; }
    double getMachNumber() { return M; }

private:
    double V;
    double M;
};

PitotTube::PitotTube()
{
    V = 0.0;    M = 0.0;
}

PitotTube::~PitotTube()
{

}

void PitotTube::compute(double q, double rho, double a)
{
    V = sqrt(2.0*q/rho);
    M = V/a;
}

///===========================================================================
class Atmosisa
{
public:
    Atmosisa();
    ~Atmosisa();

    void compute(double P);

    double getHeight() { return H; }
    double getDensity() { return rho; }
    double getTemperature() { return T; }
    double getSpeedOfSound() { return a; }

private:
    const double beta = -0.0065;
    const double g = 9.81;
    const double R = 287.0;
    const double RB = 8.31;
    const double gamma = 1.4;

    const double P0 = 101325.0;
    const double rho0 = 1.225;
    const double T0 = 288.15;

    double H;
    double rho;
    double T;
    double a;
};

Atmosisa::Atmosisa()
{
    H = 0.0;    rho = rho0;  T = T0; a = 340.27;
}

Atmosisa::~Atmosisa()
{

}

void Atmosisa::compute(double P)
{
    H = T0/beta*(pow(P/P0, -beta*R/g) - 1.0);
    T = T0 + beta*H;
    rho = rho0*pow(T/T0, -g/beta/R - 1.0);
    a = sqrt(gamma*R*T);
}

///===========================================================================
Atmosisa atmosisa;
PitotTube pitotTube;

/// inputs
double Pfull = 3.5600e+04;
double Pstat = 3.5600e+04;

/// outputs
double H = 0.0;
double V = 0.0;
double M = 0.0;

void solve()
{
    atmosisa.compute(Pstat);

    pitotTube.compute(Pfull - Pstat, atmosisa.getDensity(), atmosisa.getSpeedOfSound());

    H = atmosisa.getHeight();
    V = pitotTube.getAirspeed();
    M = pitotTube.getMachNumber();
}

int main()
{
        /// get input
        std::cin >> Pfull >> Pstat;

        /// solve problem
        solve();

        /// set output
        std::cout << std::setprecision(20) << H << " " << V << " " << M << std::endl;
    return 0;
}
