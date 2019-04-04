#include <iostream>
#include <cmath>
#include <algorithm>
#include <vector>
#include <iomanip>

#define PI 3.1415926

using namespace std;

class Point
{
public:
	Point(double x, double y) { _x = x; _y = y; }
	Point() { _x = _y = 0; }
	double getX() { return _x; }
	double getY() { return _y; }
	void add(Point p) { _x += p._x; _y += p._y; }
	void subtract(Point p) { _x -= p._x; _y -= p._y; }
	void multiply(double num) { _x *= num; _y *= num; }
	Point operator+(Point p)
	{
		Point newP(*this);
		newP.add(p);
		return newP;
	}
	Point operator-(Point p)
	{
		Point newP(*this);
		newP.subtract(p);
		return newP;
	}
	Point operator*(double num)
	{
		Point newP(*this);
		newP.multiply(num);
		return newP;
	}
	Point operator+=(Point p)
	{
		add(p);
		return *this;
	}
	Point operator-=(Point p)
	{
		subtract(p);
		return *this;
	}
	Point operator*=(double num)
	{
		multiply(num);
		return *this;
	}
	bool operator==(Point p) { return abs(_x - p._x) < 1E-2 && abs(_y - p._y) < 1E-2; }
private:
	double _x, _y;
};

class Vector
{
public:
	Vector(Point start, Point end)
	{
		_start = start;
		_end = end;
	}
	Point getStart() { return _start; }
	Point getEnd() { return _end; }
	void add(Vector vec)
	{
		double
			offsetX = vec._end.getX() - vec._start.getX(),
			offsetY = vec._end.getY() - vec._start.getY();
		_end += Point(offsetX, offsetY);
	}
	void subtract(Vector vec)
	{
		double
			offsetX = vec._end.getX() - vec._start.getX(),
			offsetY = vec._end.getY() - vec._start.getY();
		_end -= Point(offsetX, offsetY);
	}
	void multiply(double num)
	{
		Point unit = _end - _start;
		unit *= num;
		_end = _start + unit;
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
		newVec.multiply(num);
		return newVec;
	}
	Vector operator*=(double num)
	{
		multiply(num);
		return *this;
	}
	bool operator==(int zero)
	{
		return zero == 0 && _end - _start == Point(0, 0);
	}
	operator Point()
	{
		return _end - _start;
	}
	double lenght()
	{
		Point p = Point(*this);
		return sqrt(pow(p.getX(), 2) + pow(p.getY(), 2));
	}

private:
	Point _start;
	Point _end;
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
};

class Robot
{
public:
	Robot(double originDistance, double wheelRadius)
	{
		_wheelRadius = wheelRadius;
		_originDistance = originDistance;
		_orientation = 0;
		_origin = Point(0, 0);
		_motor1 = Point(originDistance, 0);
		_motor2 = Point(originDistance * cos(PI / 6), -originDistance * sin(PI / 6));
		_motor3 = Point(-originDistance * cos(PI / 6), -originDistance * sin(PI / 6));
	}
	void startMotion(Motion motion)
	{
		if (_origin == Point(0, 0))
		{
			double tOrientation = _orientation;
			if (motion.motor1w == -motion.motor2w)
			{
				rotate(2. / 3 * PI - tOrientation);
				Vector projX(Point(0, 0), Point(motion.motor3w*motion.radius, 0));
				Vector projY(Point(0, 0), Point(0, -motion.motor1w*motion.radius*sin(PI / 3)));
				Vector res = (projX + projY)*motion.time;
				_motor1 += (Point)res;
				_motor2 += (Point)res;
				_motor3 += (Point)res;
				_origin += (Point)res;
				rotate(-2. / 3 * PI + tOrientation);
				return;
			}
			if (motion.motor1w == -motion.motor3w)
			{
				rotate(-2. / 3 * PI - tOrientation);
				Vector projX(Point(0, 0), Point(motion.motor2w*motion.radius, 0));
				Vector projY(Point(0, 0), Point(0, motion.motor1w*motion.radius*sin(PI / 3)));
				Vector res = (projX + projY)*motion.time;
				_motor1 += (Point)res;
				_motor2 += (Point)res;
				_motor3 += (Point)res;
				_origin += (Point)res;
				rotate(2. / 3 * PI + tOrientation);
				return;
			}
			if (motion.motor2w == -motion.motor3w)
			{
				Vector projX(Point(0, 0), Point(motion.motor1w*motion.radius, 0));
				Vector projY(Point(0, 0), Point(0, -motion.motor2w*motion.radius*sin(PI / 3)));
				Vector res = (projX + projY)*motion.time;
				_motor1 += (Point)res;
				_motor2 += (Point)res;
				_motor3 += (Point)res;
				_origin += (Point)res;
				return;
			}
			if (motion.motor1w == motion.motor2w)
			{
				rotate(-2. / 3 * PI - tOrientation);
				Vector proj(Point(0, 0), Point(motion.motor2w*motion.radius - motion.motor1w*motion.radius*cos(PI / 3), motion.motor1w*motion.radius*sin(PI / 3)));
				if ((proj - Vector(Point(0, 0), Point(-motion.motor3w*motion.radius*cos(PI / 6), -motion.motor3w*motion.radius*sin(PI / 6))) == 0))
				{
					_motor1 += (Point)proj;
					_motor2 += (Point)proj;
					_motor3 += (Point)proj;
					_origin += (Point)proj;
					rotate(2. / 3 * PI + tOrientation);
					return;
				}
				Vector speed1(Point(0, 0), Point(-motion.motor3w*motion.radius*cos(PI / 6), -motion.motor3w*motion.radius*sin(PI / 6)));
				double proj1 = proj.lenght();
				if (motion.motor2w < 0) proj1 *= -1;
				double proj2 = speed1.lenght();
				if (motion.motor3w < 0) proj2 *= -1;
				double d = (proj2*_originDistance - proj1 * _originDistance) / (proj1 + proj2);
				Point center = _motor3 * -(d / _originDistance);
				double angle = proj1 * motion.time / (_originDistance - d);
				_motor1 -= center;
				_motor2 -= center;
				_motor3 -= center;
				_origin -= center;
				rotate(angle);
				_motor1 += center;
				_motor2 += center;
				_motor3 += center;
				_origin += center;
				rotate(2. / 3 * PI + tOrientation);
				return;
			}
			if (motion.motor2w == motion.motor3w)
			{
				rotate(2. / 3 * PI - tOrientation);
				Vector proj(Point(0, 0), Point(motion.motor3w*motion.radius - motion.motor2w*motion.radius*cos(PI / 3), motion.motor2w*motion.radius*sin(PI/3)));
				if ((proj - Vector(Point(0, 0), Point(-motion.motor1w*motion.radius*cos(PI/6), -motion.motor1w*motion.radius*sin(PI/6))) == 0))
				{
					_motor1 += (Point)proj;
					_motor2 += (Point)proj;
					_motor3 += (Point)proj;
					_origin += (Point)proj;
					rotate(-2. / 3 * PI + tOrientation);
					return;
				}
				Vector speed1(Point(0, 0), Point(-motion.motor1w*motion.radius*cos(PI / 6), -motion.motor1w*motion.radius*sin(PI / 6)));
				double proj1 = proj.lenght();
				if (motion.motor2w < 0) proj1 *= -1;
				double proj2 = speed1.lenght();
				if (motion.motor1w < 0) proj2 *= -1;
				double d = (proj2*_originDistance - proj1 * _originDistance) / (proj1 + proj2);
				Point center = _motor1* -(d / _originDistance);
				double angle = proj1 * motion.time / (_originDistance - d);
				_motor1 -= center;
				_motor2 -= center;
				_motor3 -= center;
				_origin -= center;
				rotate(angle);
				_motor1 += center;
				_motor2 += center;
				_motor3 += center;
				_origin += center;
				rotate(-2. / 3 * PI + tOrientation);
				return;
			}
			if (motion.motor3w == motion.motor1w)
			{
				Vector proj(Point(0, 0), Point(motion.motor1w*motion.radius - motion.motor3w*motion.radius*cos(PI / 3), motion.motor3w*motion.radius*sin(PI / 3)));
				if ((proj - Vector(Point(0, 0), Point(-motion.motor2w*motion.radius*cos(PI / 6), -motion.motor2w*motion.radius*sin(PI / 6))) == 0))
				{
					_motor1 += (Point)proj;
					_motor2 += (Point)proj;
					_motor3 += (Point)proj;
					_origin += (Point)proj;
					return;
				}
				Vector speed1(Point(0, 0), Point(-motion.motor2w*motion.radius*cos(PI / 6), -motion.motor2w*motion.radius*sin(PI / 6)));
				double proj1 = proj.lenght();
				if (motion.motor3w < 0) proj1 *= -1;
				double proj2 = speed1.lenght();
				if (motion.motor2w < 0) proj2 *= -1;
				double d = (proj2*_originDistance - proj1 * _originDistance) / (proj1 + proj2);
				Point center = _motor2 * -(d / _originDistance);
				double angle = proj1 * motion.time / (_originDistance - d);
				_motor1 -= center;
				_motor2 -= center;
				_motor3 -= center;
				_origin -= center;
				rotate(angle);
				_motor1 += center;
				_motor2 += center;
				_motor3 += center;
				_origin += center;
				return;
			}
		}
		Point tOrigin = _origin;
		_motor1 -= _origin;
		_motor2 -= _origin;
		_motor3 -= _origin;
		_origin -= tOrigin;
		startMotion(motion);
		_motor1 += tOrigin;
		_motor2 += tOrigin;
		_motor3 += tOrigin;
		_origin += tOrigin;
	}
	void rotate(double angle)
	{
		double
			cosa = cos(angle),
			sina = sin(angle);

		_motor1 = Point(_motor1.getX()*cosa + _motor1.getY()*sina, -_motor1.getX()*sina + _motor1.getY()*cosa);
		_motor2 = Point(_motor2.getX()*cosa + _motor2.getY()*sina, -_motor2.getX()*sina + _motor2.getY()*cosa);
		_motor3 = Point(_motor3.getX()*cosa + _motor3.getY()*sina, -_motor3.getX()*sina + _motor3.getY()*cosa);
		_origin = Point(_origin.getX()*cosa + _origin.getY()*sina, -_origin.getX()*sina + _origin.getY()*cosa);

		_orientation += angle;
	}
	Point getOrigin() { return _origin; }

private:
	Point _origin;
	Point
		_motor1,
		_motor2,
		_motor3;
	double
		_orientation,
		_wheelRadius,
		_originDistance;
};


int main()
{
	double d, r, t, n;
	cin >> d >> r >> t >> n;

	vector<double> w1(n), w2(n), w3(n);
	for (int i = 0; i < n; i++) cin >> w1[i];
	for (int i = 0; i < n; i++) cin >> w2[i];
	for (int i = 0; i < n; i++) cin >> w3[i];

	Motion m;
	m.radius = m.radius = m.radius = d / 2;
	m.time = t / n;

	//starting motion
	Robot robot(r, m.radius);
	for (int i = 0; i < n; i++)
	{
		m.motor1w = w1[i];
		m.motor2w = w2[i];
		m.motor3w = w3[i];
		robot.startMotion(m);
	}

	cout << fixed << setprecision(3) << robot.getOrigin().getX() << ' ' << robot.getOrigin().getY() << endl;
}