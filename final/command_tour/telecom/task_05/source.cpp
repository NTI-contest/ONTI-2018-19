#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>

using namespace std;

int rows;
int columns;
char** field;

struct Circle{
	double X0,Y0,R;
	double CKO;
	Circle(){
		Y0 = X0 = 0.0;
		R = 0.0;
		CKO = 0.0;
	}
};

struct param_find{
	int n;
	double X, Y;
	double X2, Y2;
	double XY;
	double X3, Y3;
	double X2Y;
	double XY2;
	vector<int> pntX;
	vector<int> pntY;
	void instal(){
		n = 0;
		X=0.0;
		Y=0.0;
		X2=0.0;
		Y2=0.0;
		X3=0.0;
		Y3=0.0;
		XY = 0.0;
		X2Y = 0.0;
		XY2 = 0.0;
	}
	param_find(){
		instal();
	}
};

//Поиск связанной группы точек
int CountOne(int i, int j, param_find* param);
Circle* FindParamCircle(param_find* param);

//главная функция которой передаем имя файла с данными
void FoundCratersOnMap(const char namefile[]){

	ifstream in(namefile);

	if(!in.is_open()){
		cout<<"FILE "<<namefile<<" is not open!\n";
	}
	
	in>>rows>>columns;
	cout<<"rows = "<<rows<<", columns="<<columns<<endl;

	field = new char*[rows];
	for(int i=0; i<rows; i++)
		field[i] = new char[columns + 2];


	in.getline(field[0],columns + 2,'\n');
	for(int i=0; i<rows; i++){
		in.getline(field[i],columns + 2,'\n');
	}
	in.close();

	ofstream out("list_craters.dat");
	out<<"X0	Y0	R\n";

	vector<param_find*> param;
	int k = 0;
	int kc = 0;
	for(int i = 0; i<rows; i++)
		for(int j = 0; j<columns; j++){
			param_find* temp = new param_find;
			int n = CountOne(i,j,temp);
			if(n>50){
				param.push_back(temp);
				Circle* cir = FindParamCircle(param[k]);
				if(cir->R>20.0 && cir->CKO<2.5){
					out<<cir->X0<<'\t'<<cir->Y0<<'\t'<<cir->R<<'\n';
					kc++;
				}
				delete cir;
				k++;
			}
			else
				delete temp;
		}

	out.close();
}

//Поиск параметров окружности
Circle* FindParamCircle(param_find* param){
	Circle* circle = new Circle;
	double A,B,D,A1,D1;
	int N = param->n;
	double X = param->X;
	double Y = param->Y;
	double X2 = param->X2;
	double Y2 = param->Y2;
	double XY = param->XY;
	double X3 = param->X3;
	double Y3 = param->Y3;
	double XY2 = param->XY2;
	double X2Y = param->X2Y;
	double X0,Y0,R,CKO;

	A = -X*X/(double)(N) + X2;
	B = -X*Y/(double)(N) + XY;
	D =  X*X2/(double)(N) + X*Y2/(double)(N) - X3 - XY2;
	A1 =-Y*Y/(double)(N) + Y2;
	D1 = X2*Y/(double)(N) + Y*Y2/(double)(N) - Y3 - X2Y;

	Y0 = (-D*B + D1*A)/(B*B - A*A1)/2.0;
	X0 = (-D*A1 + D1*B)/(A*A1 - B*B)/2.0;
	R  = sqrt((X2-2.0*X0*X+X0*X0*(double)(N)+Y2-2.0*Y0*Y+Y0*Y0*(double)(N))/(double)(N));

	CKO = 0.0;
	for(int i = 0; i<N; i++){
		double dx = (double)(param->pntX[i]) - X0;
		double dy = (double)(param->pntY[i]) - Y0;
		double dr = sqrt(dx*dx + dy*dy);
		CKO += (R-dr)*(R-dr);
	}
	CKO = sqrt(CKO/(double)(N));

	circle->X0 = X0;
	circle->Y0 = Y0;
	circle->R = R;
	circle->CKO = CKO;

	return circle;
}

//Поиск связанной группы точек
int CountOne(int i, int j, param_find *param){
	if(i<0 || i>=rows || j<0 || j>=columns)
		return 0;
	if(field[i][j] != '1')
		return 0;
	else{
		field[i][j] = '2';
		double x = (double)j;
		double y = (double)i;
		param->n++;
		param->X += x;
		param->Y += y;
		param->X2 += x*x;
		param->Y2 += y*y;
		param->XY += x*y;
		param->X3 += x*x*x;
		param->Y3 += y*y*y;
		param->X2Y += x*x*y;
		param->XY2 += x*y*y;
		param->pntX.push_back(j);
		param->pntY.push_back(i);
		return 1 + CountOne(i,j-1,param) + CountOne(i-1,j-1,param) + CountOne(i-1,j,param) + CountOne(i-1,j+1,param)
				 + CountOne(i,j+1,param) + CountOne(i+1,j+1,param) + CountOne(i+1,j,param) + CountOne(i+1,j-1,param); 
	}
}
