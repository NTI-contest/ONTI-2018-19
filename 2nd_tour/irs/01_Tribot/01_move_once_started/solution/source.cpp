#include <iostream>
#include <cmath>

#define PI 3.1415926

class Vector
{
public:
	Vector(double endX, double endY)
	{
		this->x = endX;
		this->y = endY;
	}
	void setX(double endX) { this->x = endX; }
	void setY(double endY) { this->y = endY; }
	double getX() { return x; }
	double getY() { return y; }
	void add(Vector vec)
	{
		x += vec.getX();
		y += vec.getY();
	}
	void subtract(Vector vec)
	{
		x -= vec.getX();
		y -= vec.getY();
	}
	void mult(double num)
	{
		x *= num;
		y *= num;
	}
	Vector operator+(Vector vec)
	{
		Vector newVec(*this);
		newVec.add(vec);
		return newVec;
	}
	Vector operator+=(Vector vec)
	{
		add(vec);
		return *this;
	}
	Vector operator-(Vector vec)
	{
		Vector newVec(*this);
		newVec.subtract(vec);
		return newVec;
	}
	Vector operator-=(Vector vec)
	{
		subtract(vec);
		return *this;
	}
	Vector operator*(double num)
	{
		Vector newVec(*this);
		newVec.mult(num);
		return newVec;
	}
	Vector operator*=(double num)
	{
		mult(num);
		return *this;
	}
	bool operator==(int zero)
	{
		return zero == 0 && x == 0 && y == 0;
	}

private:
	double x;
	double y;
};

struct Motion
{
public:
	Motion() {}
	Motion(double m1w, double m2w, double m3w, double time)
	{
		motor1w = m1w;
		motor2w = m2w;
		motor3w = m3w;
		this->time = time;
	}

	double
		motor1w,
		motor2w,
		motor3w;
	double time;
	double radius;

	int getType()
	{
		if (time == 0) return 0;
		if (motor1w == motor2w && motor2w == motor3w) return 0;
		if (motor1w*motor2w*motor3w == 0) return 1;
		else return 2;
	}
	Vector getMotionVector()
	{
		int type = getType();
		switch (type)
		{
		case 0: return Vector(0, 0);
		case 1:
			if (motor1w == 0)
			{
				double speed = motor2w * radius;
				Vector sVec(0, -speed * cos(PI / 6));
				return sVec;
			}
			if (motor2w == 0)
			{
				double speed = motor1w * radius;
				Vector sVec(speed * pow(cos(PI / 6), 2), -speed 
					* sin(PI / 6) * cos(PI / 6));
				return sVec;
			}
			if (motor3w == 0)
			{
				double speed = motor1w * radius;
				Vector sVec(speed * pow(cos(PI / 6), 2), speed 
					* sin(PI / 6) * cos(PI / 6));
				return sVec;
			}
		case 2:
			if (motor1w == motor2w)
			{
				double speed3 = motor3w * radius;
				return Vector(motor1w*radius, speed3*sin(PI / 3));
			}
			if (motor1w == motor3w)
			{
				double speed2 = motor2w * radius;
				return Vector(motor1w*radius, -speed2 * sin(PI / 3));
			}
			if (motor2w == motor3w)
			{
				double speed1 = motor1w * radius;
				return Vector(speed1, 0);
			}
		}
	}
};

using namespace std;

int main()
{
	double d, w1, t1, w2, t2, w3, t3;
	cin >> d >> w1 >> t1 >> w2 >> t2 >> w3 >> t3;

	//split motion into simple motions by timespans
	Motion m1, m2, m3;
	m1.radius = m2.radius = m3.radius = d / 2;
	if (t1 >= t2 && t2 >= t3)
	{
		m1.motor1w = w1; m1.motor2w = w2; m1.motor3w = w3;
		m1.time = t3;
		m2.motor1w = w1; m2.motor2w = w2; m2.motor3w = 0;
		m2.time = t2 - t3;
		m3.motor1w = w1; m3.motor2w = 0; m3.motor3w = 0;
		m3.time = t1 - t2;
	}
	else if (t1 >= t3 && t3 >= t2)
	{
		m1.motor1w = w1; m1.motor2w = w2; m1.motor3w = w3;
		m1.time = t2;
		m2.motor1w = w1; m2.motor2w = 0; m2.motor3w = w3;
		m2.time = t3 - t2;
		m3.motor1w = w1; m3.motor2w = 0; m3.motor3w = 0;
		m3.time = t1 - t3;
	}
	else if (t2 >= t1 && t1 >= t3)
	{
		m1.motor1w = w1; m1.motor2w = w2; m1.motor3w = w3;
		m1.time = t3;
		m2.motor1w = w1; m2.motor2w = w2; m2.motor3w = 0;
		m2.time = t1 - t3;
		m3.motor1w = 0; m3.motor2w = w2; m3.motor3w = 0;
		m3.time = t2 - t1;
	}
	else if (t2 >= t3 && t3 >= t1)
	{
		m1.motor1w = w1; m1.motor2w = w2; m1.motor3w = w3;
		m1.time = t1;
		m2.motor1w = 0; m2.motor2w = w2; m2.motor3w = w3;
		m2.time = t3 - t1;
		m3.motor1w = 0; m3.motor2w = w2; m3.motor3w = 0;
		m3.time = t2 - t3;
	}
	else if (t3 >= t1 && t1 >= t2)
	{
		m1.motor1w = w1; m1.motor2w = w2; m1.motor3w = w3;
		m1.time = t2;
		m2.motor1w = w1; m2.motor2w = 0; m2.motor3w = w3;
		m2.time = t1 - t2;
		m3.motor1w = 0; m3.motor2w = 0; m3.motor3w = w3;
		m3.time = t3 - t1;
	}
	else if (t3 >= t2 && t2 >= t1)
	{
		m1.motor1w = w1; m1.motor2w = w2; m1.motor3w = w3;
		m1.time = t1;
		m2.motor1w = 0; m2.motor2w = w2; m2.motor3w = w3;
		m2.time = t2 - t1;
		m3.motor1w = 0; m3.motor2w = 0; m3.motor3w = w3;
		m3.time = t3 - t2;
	}

	//starting motion
	Vector result(0, 0);
	result += m1.getMotionVector() * m1.time;
	result += m2.getMotionVector() * m2.time;
	result += m3.getMotionVector() * m3.time;

	cout << result.getX() << ' ' << result.getY() << endl;
}