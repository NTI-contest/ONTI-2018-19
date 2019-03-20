#include <iostream>
#include <math.h>

using namespace std;

///===========================================================================
/// Problem solving
double *T;
double *x;
int N;
double J = 0.0;
extern void solve();

int main()
{
        cin >> N;
        x = new double[N];
        T = new double[N];
        for (int i = 0; i < N; i++)
        {
            cin >> x[i];
        }
        for (int i = 0; i < N; i++)
        {
            cin >> T[i];
        }

        /// solve problem
        solve();

        /// set output
    	cout.setf(std::ios_base::fixed, std::ios_base::floatfield);
        cout.precision(10);
        cout << J << endl << endl;

        delete x;
        delete T;

    return 0;
}

///===========================================================================
void solve()
{
    double sumTx2 = 0.0;
    double sumTx1 = 0.0;
    double sumTx0 = 0.0;

    double sumx4 = 0.0;
    double sumx3 = 0.0;
    double sumx2 = 0.0;
    double sumx1 = 0.0;
    double sumx0 = 0.0;

    for (int i = 0; i < N; i++)
    {
        sumTx2 += T[i]*x[i]*x[i];
        sumTx1 += T[i]*x[i];
        sumTx0 += T[i];

        sumx4 += x[i]*x[i]*x[i]*x[i];
        sumx3 += x[i]*x[i]*x[i];
        sumx2 += x[i]*x[i];
        sumx1 += x[i];
        sumx0 += 1.0;
    }

    double a11 = sumx4; double a12 = sumx3; double a13 = sumx2;
    double a21 = sumx3; double a22 = sumx2; double a23 = sumx1;
    double a31 = sumx2; double a32 = sumx1; double a33 = sumx0;

    double b1 = sumTx2;  double b2 = sumTx1;  double b3 = sumTx0;

    double delta = a11*(a22*a33 - a23*a32) - a12*(a21*a33 - a23*a31) + 
        a13*(a21*a32 - a22*a31);

    double delta1 =  b1*(a22*a33 - a23*a32) - b2*(a12*a33 - a13*a32) + 
        b3*(a12*a23 - a13*a22);
    double delta2 = -b1*(a21*a33 - a23*a31) + b2*(a11*a33 - a13*a31) - 
        b3*(a11*a23 - a13*a21);
    double delta3 =  b1*(a21*a32 - a22*a31) - b2*(a11*a32 - a12*a31) + 
        b3*(a11*a22 - a12*a21);

    double a = delta1/delta;
    double b = delta2/delta;
    double c = delta3/delta;

    J = 0.0;
    for (int i = 0; i < 13; i++)
    {
        J += 0.5*pow(T[i] - a*x[i]*x[i] - b*x[i] - c, 2.0);
    }
}